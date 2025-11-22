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
    def __init__(self, container_name=None):
        self.container_name = container_name or self.find_container()
        self.metrics = {
            'loss': deque(maxlen=20),
            'rewards': deque(maxlen=20),
            'difficulty': 0,
            'diversity': deque(maxlen=10),
            'last_update': None,
            'total_rewards': 0.0,
            'epochs': 0
        }
        
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
    
    def get_docker_logs(self, lines=50):
        """Get recent Docker logs"""
        if not self.container_name:
            return []
        
        try:
            result = subprocess.run(
                ['docker', 'logs', '--tail', str(lines), self.container_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.split('\n')
        except:
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
        header = Panel(
            f"[bold cyan]🌊 Swarm Pulse CLI[/bold cyan] | Status: {emoji} {status.upper()}",
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
        if not self.container_name:
            console.print("[red]❌ RL-Swarm container not found![/red]")
            console.print("[yellow]Start your node first:[/yellow]")
            console.print("  cd ~/rl-swarm && docker-compose run --rm --build -Pit swarm-cpu")
            sys.exit(1)
        
        console.print(f"[green]✅ Monitoring container: {self.container_name}[/green]")
        console.print("[dim]Loading initial data...[/dim]\n")
        
        # Initial load
        logs = self.get_docker_logs(100)
        self.parse_logs(logs)
        
        # Live update
        with Live(self.create_dashboard(), refresh_per_second=1, console=console) as live:
            try:
                while True:
                    # Get new logs
                    logs = self.get_docker_logs(20)
                    self.parse_logs(logs)
                    
                    # Update display
                    live.update(self.create_dashboard())
                    
                    time.sleep(2)
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Monitoring stopped[/yellow]")

if __name__ == "__main__":
    monitor = CodeZeroMonitor()
    monitor.run()
