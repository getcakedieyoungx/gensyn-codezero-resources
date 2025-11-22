"""
Log Parser for CodeZero Node Logs

Extracts structured data from CodeZero log files including:
- Policy updates (learning progress)
- Rewards (earnings and rankings)
- Difficulty adjustments
- Rollout generation (diversity scores)
"""

import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class PolicyUpdate:
    timestamp: datetime
    epoch: int
    loss: float
    gradient_norm: float = None


@dataclass
class Reward:
    timestamp: datetime
    amount: float
    rank: int
    total_solvers: int
    problem_id: str = None


@dataclass
class DifficultyChange:
    timestamp: datetime
    from_level: int
    to_level: int
    swarm_success_rate: float = None


@dataclass
class Rollout:
    timestamp: datetime
    problem_id: str
    steps: int = None
    diversity_score: float = None


class LogParser:
    """Parse CodeZero node logs and extract structured data"""
    
    # Regex patterns for log parsing
    PATTERNS = {
        'policy_update': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Policy update.*epoch=(\d+).*loss=([\d.]+)'
        ),
        'gradient': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Gradient applied.*avg_norm=([\d.]+)'
        ),
        'reward': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Reward received.*amount=([\d.]+).*rank=(\d+)/(\d+)'
        ),
        'reward_with_id': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Reward received.*amount=([\d.]+).*problem_id=(0x[a-f0-9]+).*rank=(\d+)/(\d+)'
        ),
        'difficulty': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Difficulty adjusted: (\d+) → (\d+)'
        ),
        'difficulty_with_rate': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Difficulty adjusted: (\d+) → (\d+).*swarm_success_rate=([\d.]+)'
        ),
        'rollout': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Rollout generated.*problem_id=(0x[a-f0-9]+).*diversity_score=([\d.]+)'
        ),
        'rollout_with_steps': re.compile(
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\].*Rollout generated.*problem_id=(0x[a-f0-9]+).*steps=(\d+).*diversity_score=([\d.]+)'
        ),
    }
    
    def __init__(self):
        self.data = {
            'policy_updates': [],
            'rewards': [],
            'difficulty_changes': [],
            'rollouts': []
        }
        self._last_gradient_norm = None
    
    def parse_file(self, filepath: str) -> Dict[str, List[Any]]:
        """Parse entire log file and return structured data"""
        self.data = {
            'policy_updates': [],
            'rewards': [],
            'difficulty_changes': [],
            'rollouts': []
        }
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                self.parse_line(line.strip())
        
        return self.data
    
    def parse_line(self, line: str) -> None:
        """Parse a single log line and update data"""
        # Try policy update
        match = self.PATTERNS['policy_update'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            epoch = int(match.group(2))
            loss = float(match.group(3))
            
            self.data['policy_updates'].append(PolicyUpdate(
                timestamp=timestamp,
                epoch=epoch,
                loss=loss,
                gradient_norm=self._last_gradient_norm
            ))
            self._last_gradient_norm = None
            return
        
        # Try gradient (for next policy update)
        match = self.PATTERNS['gradient'].search(line)
        if match:
            self._last_gradient_norm = float(match.group(2))
            return
        
        # Try reward with problem_id
        match = self.PATTERNS['reward_with_id'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            amount = float(match.group(2))
            problem_id = match.group(3)
            rank = int(match.group(4))
            total = int(match.group(5))
            
            self.data['rewards'].append(Reward(
                timestamp=timestamp,
                amount=amount,
                rank=rank,
                total_solvers=total,
                problem_id=problem_id
            ))
            return
        
        # Try reward without problem_id
        match = self.PATTERNS['reward'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            amount = float(match.group(2))
            rank = int(match.group(3))
            total = int(match.group(4))
            
            self.data['rewards'].append(Reward(
                timestamp=timestamp,
                amount=amount,
                rank=rank,
                total_solvers=total
            ))
            return
        
        # Try difficulty with success rate
        match = self.PATTERNS['difficulty_with_rate'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            from_level = int(match.group(2))
            to_level = int(match.group(3))
            success_rate = float(match.group(4))
            
            self.data['difficulty_changes'].append(DifficultyChange(
                timestamp=timestamp,
                from_level=from_level,
                to_level=to_level,
                swarm_success_rate=success_rate
            ))
            return
        
        # Try difficulty without success rate
        match = self.PATTERNS['difficulty'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            from_level = int(match.group(2))
            to_level = int(match.group(3))
            
            self.data['difficulty_changes'].append(DifficultyChange(
                timestamp=timestamp,
                from_level=from_level,
                to_level=to_level
            ))
            return
        
        # Try rollout with steps
        match = self.PATTERNS['rollout_with_steps'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            problem_id = match.group(2)
            steps = int(match.group(3))
            diversity = float(match.group(4))
            
            self.data['rollouts'].append(Rollout(
                timestamp=timestamp,
                problem_id=problem_id,
                steps=steps,
                diversity_score=diversity
            ))
            return
        
        # Try rollout without steps
        match = self.PATTERNS['rollout'].search(line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            problem_id = match.group(2)
            diversity = float(match.group(3))
            
            self.data['rollouts'].append(Rollout(
                timestamp=timestamp,
                problem_id=problem_id,
                diversity_score=diversity
            ))
            return
    
    def get_data_dict(self) -> Dict[str, List[Dict]]:
        """Convert dataclasses to dictionaries for easier JSON serialization"""
        return {
            'policy_updates': [asdict(p) for p in self.data['policy_updates']],
            'rewards': [asdict(r) for r in self.data['rewards']],
            'difficulty_changes': [asdict(d) for d in self.data['difficulty_changes']],
            'rollouts': [asdict(r) for r in self.data['rollouts']]
        }
