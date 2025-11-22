#!/usr/bin/env python3
"""
Swarm Pulse CLI - Terminal-based CodeZero Monitor
Real-time node health monitoring in your terminal
"""

import subprocess
import re
import time
from datetime import datetime
from collections import deque
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
import sys

console = Console()

class CodeZeroMonitor:
    def __init__(self, log_file=None, container_name=None):
        self.log_file = log_file
        self.container_name = container_name
        self.mode = None
        
        # Determine monitoring mode
        if log_file:
            self.mode = "file"
            self.log_position = 0
        elif container_name:
            self.mode = "docker"
            self.container_name = container_name
        else:
            # Auto-detect
            self.container_name = self.find_container()
            if self.container_name:
                self.mode = "docker"
            else:
                # Try to find log file
                self.log_file = self.find_log_file()
                if self.log_file:
                    self.mode = "file"
                    self.log_position = 0
        
        self.metrics = {
            'loss': deque(maxlen=20),
            'rewards': deque(maxlen=20),
            'difficulty': 0,
            'diversity': deque(maxlen=10),
            'last_update': None,
            'total_rewards': 0.0,
            'epochs': 0
        }
    
    def find_log_file(self):
        """Find log file in common locations"""
        import os
        common_paths = [
            os.path.expanduser("~/rl-swarm/output.log"),
            os.path.expanduser("~/rl-swarm/logs/node.log"),
            os.path.expanduser("~/.codezero/logs/node.log"),
            os.path.expanduser("~/codezero/logs/node.log"),
            "/var/log/codezero/node.log",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
        
    def find_container(self):
        """Find rl-swarm container"""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=rl-swarm', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                check=True
            )
            containers = result.stdout.strip().split('\n')
            return containers[0] if containers and containers[0] else None
        except:
            return None
    
    def get_logs(self, lines=50):
        """Get logs based on mode"""
        if self.mode == "docker":
            return self.get_docker_logs(lines)
        elif self.mode == "file":
            return self.get_file_logs(lines)
        return []
    
    def get_file_logs(self, lines=50):
        """Read logs from file (tail -f style)"""
        if not self.log_file:
            return []
        
        try:
            with open(self.log_file, 'r') as f:
                # Seek to last position
                f.seek(self.log_position)
                new_lines = f.readlines()
                self.log_position = f.tell()
                
                # If first read, get last N lines
                if not new_lines and self.log_position == 0:
                    f.seek(0)
                    all_lines = f.readlines()
                    new_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                    self.log_position = f.tell()
                
                return [line.strip() for line in new_lines]
        except Exception as e:
            return []
    
    def parse_logs(self, logs):
        """Parse logs and update metrics"""
        for line in logs:
            # Policy update
            match = re.search(r'epoch=(\d+).*loss=([\d.]+)', line)
            if match:
                self.metrics['epochs'] = int(match.group(1))
                self.metrics['loss'].append(float(match.group(2)))
                self.metrics['last_update'] = datetime.now()
            
            # Reward
            match = re.search(r'amount=([\d.]+)', line)
            if match:
                reward = float(match.group(1))
                self.metrics['rewards'].append(reward)
                self.metrics['total_rewards'] += reward
            
            # Difficulty
            match = re.search(r'Difficulty adjusted: \d+ → (\d+)', line)
            if match:
                self.metrics['difficulty'] = int(match.group(1))
            
            # Diversity
            match = re.search(r'diversity_score=([\d.]+)', line)
            if match:
                self.metrics['diversity'].append(float(match.group(1)))
    
    def get_health_status(self):
        """Calculate health status"""
        if not self.metrics['loss']:
            return "unknown", "⚪"
        
        avg_loss = sum(self.metrics['loss']) / len(self.metrics['loss'])
        avg_diversity = sum(self.metrics['diversity']) / len(self.metrics['diversity']) if self.metrics['diversity'] else 0
        
        issues = 0
        if avg_loss > 0.1:
            issues += 1
        if avg_diversity < 0.5:
            issues += 1
        
        if issues == 0:
            return "healthy", "🟢"
        elif issues == 1:
            return "warning", "🟡"
        else:
            return "critical", "🔴"
    
    def create_dashboard(self):
        """Create terminal dashboard"""
        layout = Layout()
        
        # Header
        status, emoji = self.get_health_status()
        mode_text = f"Docker: {self.container_name}" if self.mode == "docker" else f"File: {self.log_file}"
        header = Panel(
            f"[bold cyan]🌊 Swarm Pulse CLI[/bold cyan] | {mode_text}\nStatus: {emoji} {status.upper()}",
            style="bold white on blue"
        )
        
        # Metrics table
        metrics_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        metrics_table.add_column("Metric", style="cyan", width=20)
        metrics_table.add_column("Value", style="green", width=30)
        
        # Current metrics
        current_loss = self.metrics['loss'][-1] if self.metrics['loss'] else 0
        avg_loss = sum(self.metrics['loss']) / len(self.metrics['loss']) if self.metrics['loss'] else 0
        avg_diversity = sum(self.metrics['diversity']) / len(self.metrics['diversity']) if self.metrics['diversity'] else 0
        
        metrics_table.add_row("📊 Current Loss", f"{current_loss:.4f}")
        metrics_table.add_row("📉 Avg Loss (20)", f"{avg_loss:.4f}")
        metrics_table.add_row("💰 Total Rewards", f"{self.metrics['total_rewards']:.4f} GENSYN")
        metrics_table.add_row("🎯 Difficulty", f"Level {self.metrics['difficulty']}")
        metrics_table.add_row("🎨 Avg Diversity", f"{avg_diversity:.2f}")
        metrics_table.add_row("⚡ Epochs", f"{self.metrics['epochs']}")
        
        # Loss trend
        loss_chart = self.create_sparkline(list(self.metrics['loss']), "Loss Trend")
        
        # Rewards trend
        reward_chart = self.create_sparkline(list(self.metrics['rewards']), "Recent Rewards")
        
        # Footer
        last_update = self.metrics['last_update'].strftime("%H:%M:%S") if self.metrics['last_update'] else "Never"
        footer = Panel(
            f"[dim]Container: {self.container_name or 'Not found'} | Last Update: {last_update} | Press Ctrl+C to exit[/dim]",
            style="dim"
        )
        
        # Combine
        layout.split_column(
            Layout(header, size=3),
            Layout(metrics_table, size=10),
            Layout(loss_chart, size=5),
            Layout(reward_chart, size=5),
            Layout(footer, size=3)
        )
        
        return layout
    
    def create_sparkline(self, data, title):
        """Create ASCII sparkline chart"""
        if not data:
            return Panel(f"[dim]{title}: No data[/dim]")
        
        # Normalize data
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Sparkline characters
        chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        
        # Create sparkline
        sparkline = ""
        for val in data:
            normalized = (val - min_val) / range_val
            char_idx = min(int(normalized * len(chars)), len(chars) - 1)
            sparkline += chars[char_idx]
        
        # Color based on trend
        if len(data) >= 2:
            trend = "↗" if data[-1] > data[-2] else "↘" if data[-1] < data[-2] else "→"
        else:
            trend = "→"
        
        text = f"{title} {trend}\n{sparkline}\n[dim]Min: {min_val:.4f} | Max: {max_val:.4f} | Current: {data[-1]:.4f}[/dim]"
        
        return Panel(text, border_style="cyan")
    
    def run(self):
        """Main monitoring loop"""
        if not self.mode:
            console.print("[red]❌ No log source found![/red]")
            console.print("\n[yellow]Options:[/yellow]")
            console.print("  1. Start rl-swarm with Docker:")
            console.print("     cd ~/rl-swarm && docker-compose run --rm --build -Pit swarm-cpu")
            console.print("\n  2. Specify log file manually:")
            console.print("     ./monitor.py --log-file /path/to/your/log.txt")
            console.print("\n  3. Run rl-swarm in screen/tmux and redirect output:")
            console.print("     screen -S codezero")
            console.print("     python run_rl_swarm.py 2>&1 | tee ~/codezero.log")
            sys.exit(1)
        
        if self.mode == "docker":
            console.print(f"[green]✅ Monitoring Docker container: {self.container_name}[/green]")
        else:
            console.print(f"[green]✅ Monitoring log file: {self.log_file}[/green]")
        
        console.print("[dim]Loading initial data...[/dim]\n")
        
        # Initial load
        logs = self.get_logs(100)
        self.parse_logs(logs)
        
        # Live update
        with Live(self.create_dashboard(), refresh_per_second=1, console=console) as live:
            try:
                while True:
                    # Get new logs
                    logs = self.get_logs(20)
                    self.parse_logs(logs)
                    
                    # Update display
                    live.update(self.create_dashboard())
                    
                    time.sleep(2)
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Monitoring stopped[/yellow]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Swarm Pulse CLI - CodeZero Node Monitor')
    parser.add_argument('--log-file', '-f', help='Path to log file (for screen/tmux users)')
    parser.add_argument('--container', '-c', help='Docker container name')
    args = parser.parse_args()
    
    monitor = CodeZeroMonitor(log_file=args.log_file, container_name=args.container)
    monitor.run()
