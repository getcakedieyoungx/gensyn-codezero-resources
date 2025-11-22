"""
Visualization Components for Swarm Pulse

Creates interactive charts using Plotly to visualize CodeZero metrics.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


def create_difficulty_chart(difficulty_changes: List[Dict]) -> go.Figure:
    """
    Create difficulty adjustment timeline chart
    
    Args:
        difficulty_changes: List of difficulty change events
    
    Returns:
        Plotly figure
    """
    if not difficulty_changes:
        fig = go.Figure()
        fig.add_annotation(
            text="No difficulty changes recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300)
        return fig
    
    df = pd.DataFrame(difficulty_changes)
    
    # Create step chart
    fig = go.Figure()
    
    # Add line showing difficulty level over time
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['to_level'],
        mode='lines+markers',
        name='Difficulty Level',
        line=dict(color='#00D9FF', width=3, shape='hv'),
        marker=dict(size=10, symbol='diamond'),
        hovertemplate='<b>Difficulty: %{y}</b><br>Time: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Difficulty Adjustment Timeline",
        xaxis_title="Time",
        yaxis_title="Difficulty Level",
        yaxis=dict(range=[0, 6], dtick=1),
        hovermode='x unified',
        height=350,
        template='plotly_dark'
    )
    
    return fig


def create_loss_chart(policy_updates: List[Dict]) -> go.Figure:
    """
    Create loss over time chart with trend line
    
    Args:
        policy_updates: List of policy update events
    
    Returns:
        Plotly figure
    """
    if not policy_updates:
        fig = go.Figure()
        fig.add_annotation(
            text="No policy updates recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300)
        return fig
    
    df = pd.DataFrame(policy_updates)
    
    fig = go.Figure()
    
    # Add loss line
    fig.add_trace(go.Scatter(
        x=df['epoch'],
        y=df['loss'],
        mode='lines+markers',
        name='Loss',
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=6),
        hovertemplate='<b>Epoch %{x}</b><br>Loss: %{y:.4f}<extra></extra>'
    ))
    
    # Add moving average if enough data
    if len(df) >= 5:
        df['loss_ma'] = df['loss'].rolling(window=5, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df['epoch'],
            y=df['loss_ma'],
            mode='lines',
            name='Moving Avg (5)',
            line=dict(color='#FFD93D', width=2, dash='dash'),
            hovertemplate='<b>Epoch %{x}</b><br>MA: %{y:.4f}<extra></extra>'
        ))
    
    # Add colored zones
    max_loss = df['loss'].max()
    fig.add_hrect(y0=0, y1=0.01, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_hrect(y0=0.01, y1=0.05, fillcolor="yellow", opacity=0.1, line_width=0)
    fig.add_hrect(y0=0.05, y1=max_loss * 1.1, fillcolor="red", opacity=0.1, line_width=0)
    
    fig.update_layout(
        title="Learning Progress (Loss Over Time)",
        xaxis_title="Epoch",
        yaxis_title="Loss",
        hovermode='x unified',
        height=350,
        template='plotly_dark'
    )
    
    return fig


def create_reward_chart(rewards: List[Dict]) -> go.Figure:
    """
    Create reward distribution chart
    
    Args:
        rewards: List of reward events
    
    Returns:
        Plotly figure
    """
    if not rewards:
        fig = go.Figure()
        fig.add_annotation(
            text="No rewards recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300)
        return fig
    
    df = pd.DataFrame(rewards)
    df['rank_percentile'] = (1 - (df['rank'] - 1) / df['total_solvers']) * 100
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add reward bars
    fig.add_trace(
        go.Bar(
            x=df['timestamp'],
            y=df['amount'],
            name='Reward Amount',
            marker_color='#6BCF7F',
            hovertemplate='<b>Reward: %{y:.4f}</b><br>Time: %{x}<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Add rank percentile line
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['rank_percentile'],
            name='Rank Percentile',
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Rank: #%{customdata[0]}/%{customdata[1]}</b><br>Percentile: %{y:.1f}%<extra></extra>',
            customdata=df[['rank', 'total_solvers']].values
        ),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Reward Amount", secondary_y=False)
    fig.update_yaxes(title_text="Rank Percentile (%)", secondary_y=True, range=[0, 100])
    
    fig.update_layout(
        title="Reward Analysis",
        hovermode='x unified',
        height=350,
        template='plotly_dark'
    )
    
    return fig


def create_diversity_chart(rollouts: List[Dict]) -> go.Figure:
    """
    Create diversity score chart
    
    Args:
        rollouts: List of rollout events
    
    Returns:
        Plotly figure
    """
    if not rollouts:
        fig = go.Figure()
        fig.add_annotation(
            text="No rollouts recorded yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=300)
        return fig
    
    df = pd.DataFrame(rollouts)
    
    fig = go.Figure()
    
    # Add diversity score area
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['diversity_score'],
        mode='lines',
        name='Diversity Score',
        fill='tozeroy',
        line=dict(color='#A78BFA', width=2),
        fillcolor='rgba(167, 139, 250, 0.3)',
        hovertemplate='<b>Diversity: %{y:.2f}</b><br>Time: %{x}<extra></extra>'
    ))
    
    # Add threshold line at 0.6
    fig.add_hline(
        y=0.6,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Healthy Threshold (0.6)",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="Solution Diversity Score",
        xaxis_title="Time",
        yaxis_title="Diversity Score",
        yaxis=dict(range=[0, 1]),
        hovermode='x unified',
        height=350,
        template='plotly_dark'
    )
    
    return fig


def calculate_health_metrics(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Calculate overall health metrics
    
    Args:
        data: Parsed log data
    
    Returns:
        Dictionary of health metrics
    """
    metrics = {
        'avg_loss': None,
        'total_rewards': 0.0,
        'avg_rank_percentile': None,
        'avg_diversity': None,
        'updates_per_hour': 0.0,
        'health_status': 'unknown'
    }
    
    # Calculate average loss (last 10 epochs)
    if data['policy_updates']:
        recent_updates = data['policy_updates'][-10:]
        losses = [u['loss'] for u in recent_updates]
        metrics['avg_loss'] = sum(losses) / len(losses)
    
    # Calculate total rewards
    if data['rewards']:
        metrics['total_rewards'] = sum(r['amount'] for r in data['rewards'])
        
        # Calculate average rank percentile
        percentiles = [(1 - (r['rank'] - 1) / r['total_solvers']) * 100 
                      for r in data['rewards']]
        metrics['avg_rank_percentile'] = sum(percentiles) / len(percentiles)
    
    # Calculate average diversity
    if data['rollouts']:
        diversities = [r['diversity_score'] for r in data['rollouts'] 
                      if r['diversity_score'] is not None]
        if diversities:
            metrics['avg_diversity'] = sum(diversities) / len(diversities)
    
    # Calculate updates per hour
    if data['policy_updates'] and len(data['policy_updates']) >= 2:
        first_time = pd.to_datetime(data['policy_updates'][0]['timestamp'])
        last_time = pd.to_datetime(data['policy_updates'][-1]['timestamp'])
        hours = (last_time - first_time).total_seconds() / 3600
        if hours > 0:
            metrics['updates_per_hour'] = len(data['policy_updates']) / hours
    
    # Determine health status
    issues = 0
    if metrics['avg_loss'] and metrics['avg_loss'] > 0.1:
        issues += 1
    if metrics['avg_rank_percentile'] and metrics['avg_rank_percentile'] < 40:
        issues += 1
    if metrics['avg_diversity'] and metrics['avg_diversity'] < 0.5:
        issues += 1
    
    if issues == 0:
        metrics['health_status'] = 'healthy'
    elif issues == 1:
        metrics['health_status'] = 'warning'
    else:
        metrics['health_status'] = 'critical'
    
    return metrics
