"""
Swarm Pulse - CodeZero Log Visualizer
Real-time monitoring dashboard for CodeZero node runners
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import time
from datetime import datetime, timedelta

from log_parser import LogParser
from log_watcher import LogWatcher, tail_file
from visualizations import (
    create_difficulty_chart,
    create_loss_chart,
    create_reward_chart,
    create_diversity_chart,
    calculate_health_metrics
)

# Page config
st.set_page_config(
    page_title="Swarm Pulse - CodeZero Monitor",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00D9FF;
    }
    .health-healthy { color: #6BCF7F; }
    .health-warning { color: #FFD93D; }
    .health-critical { color: #FF6B6B; }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'parser' not in st.session_state:
    st.session_state.parser = LogParser()
if 'data' not in st.session_state:
    st.session_state.data = None
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'log_file_path' not in st.session_state:
    st.session_state.log_file_path = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

# Header
st.title("🌊 Swarm Pulse")
st.markdown("**Real-time CodeZero Node Monitor**")

# Sidebar
with st.sidebar:
    st.header("📁 Log Source")
    
    mode = st.radio(
        "Select Mode",
        ["📂 Upload File", "🔴 Real-time Monitor"],
        label_visibility="collapsed"
    )
    
    if mode == "📂 Upload File":
        # File upload mode
        uploaded_file = st.file_uploader(
            "Upload log file",
            type=['log', 'txt'],
            help="Upload your CodeZero node log file"
        )
        
        # Sample data button
        sample_path = Path(__file__).parent / "sample_logs" / "sample_node.log"
        if sample_path.exists():
            if st.button("📋 Use Sample Data"):
                st.session_state.log_file_path = str(sample_path)
                st.session_state.data = st.session_state.parser.parse_file(str(sample_path))
                st.session_state.last_update = datetime.now()
                st.rerun()
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = Path("temp_log.txt")
            temp_path.write_bytes(uploaded_file.getvalue())
            
            st.session_state.log_file_path = str(temp_path)
            st.session_state.data = st.session_state.parser.parse_file(str(temp_path))
            st.session_state.last_update = datetime.now()
            st.success("✅ File loaded successfully!")
    
    else:
        # Real-time monitoring mode
        log_path = st.text_input(
            "Log file path",
            placeholder="/path/to/codezero/node.log",
            help="Enter the full path to your active log file"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start", type="primary", disabled=st.session_state.monitoring):
                if log_path and Path(log_path).exists():
                    st.session_state.log_file_path = log_path
                    st.session_state.monitoring = True
                    # Load historical data first
                    st.session_state.data = st.session_state.parser.parse_file(log_path)
                    st.session_state.last_update = datetime.now()
                    st.success("🟢 Monitoring started!")
                    st.rerun()
                else:
                    st.error("❌ File not found!")
        
        with col2:
            if st.button("⏸️ Stop", disabled=not st.session_state.monitoring):
                st.session_state.monitoring = False
                st.info("🔴 Monitoring stopped")
                st.rerun()
        
        # Auto-refresh settings
        if st.session_state.monitoring:
            st.markdown("---")
            refresh_interval = st.slider(
                "Auto-refresh interval (seconds)",
                min_value=1,
                max_value=10,
                value=2,
                help="How often to check for new log entries"
            )
            
            # Status indicator
            if st.session_state.last_update:
                time_ago = (datetime.now() - st.session_state.last_update).seconds
                st.markdown(f"🟢 **LIVE** | Last update: {time_ago}s ago")
            
            # Auto-refresh logic
            time.sleep(refresh_interval)
            
            # Re-parse file to get new entries
            if st.session_state.log_file_path:
                st.session_state.data = st.session_state.parser.parse_file(
                    st.session_state.log_file_path
                )
                st.session_state.last_update = datetime.now()
                st.rerun()
    
    # Export data
    if st.session_state.data:
        st.markdown("---")
        st.subheader("💾 Export")
        
        if st.button("📥 Download CSV"):
            # Convert data to CSV
            all_data = []
            for key, items in st.session_state.data.items():
                for item in items:
                    item['type'] = key
                    all_data.append(item)
            
            if all_data:
                df = pd.DataFrame(all_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download",
                    data=csv,
                    file_name=f"swarm_pulse_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# Main content
if st.session_state.data is None:
    # Welcome screen
    st.info("👈 Upload a log file or start real-time monitoring to begin")
    
    st.markdown("""
    ### 🎯 What is Swarm Pulse?
    
    Swarm Pulse helps you understand if your CodeZero node is actually learning by visualizing:
    
    - 📈 **Difficulty Adjustments** - How problem complexity changes over time
    - 📉 **Learning Progress** - Loss metrics and training trends
    - 💰 **Reward Analysis** - Earnings and performance rankings
    - 🎨 **Diversity Scores** - How unique your solutions are
    
    ### 🚀 Getting Started
    
    1. **Upload Mode**: Upload your exported log file for offline analysis
    2. **Real-time Mode**: Point to your active log file for live monitoring
    3. **Sample Data**: Try the demo with pre-loaded sample logs
    
    ### 📖 Learn More
    
    Check out the [CodeZero Log Guide](https://github.com/getcakedieyoungx/gensyn-codezero-resources) 
    to understand what each metric means.
    """)

else:
    # Calculate health metrics
    metrics = calculate_health_metrics(st.session_state.data)
    
    # Health status banner
    status_emoji = {
        'healthy': '🟢',
        'warning': '🟡',
        'critical': '🔴',
        'unknown': '⚪'
    }
    
    status_text = {
        'healthy': 'Healthy - Node is performing well!',
        'warning': 'Warning - Some metrics need attention',
        'critical': 'Critical - Multiple issues detected',
        'unknown': 'Unknown - Insufficient data'
    }
    
    health_status = metrics['health_status']
    st.markdown(f"### {status_emoji[health_status]} {status_text[health_status]}")
    
    # Metrics cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Avg Loss",
            f"{metrics['avg_loss']:.4f}" if metrics['avg_loss'] else "N/A",
            delta="Lower is better",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Total Rewards",
            f"{metrics['total_rewards']:.4f}" if metrics['total_rewards'] else "0.0000"
        )
    
    with col3:
        st.metric(
            "Avg Rank",
            f"{metrics['avg_rank_percentile']:.1f}%" if metrics['avg_rank_percentile'] else "N/A",
            delta="Top percentile"
        )
    
    with col4:
        st.metric(
            "Avg Diversity",
            f"{metrics['avg_diversity']:.2f}" if metrics['avg_diversity'] else "N/A",
            delta="> 0.6 is healthy"
        )
    
    with col5:
        st.metric(
            "Updates/Hour",
            f"{metrics['updates_per_hour']:.1f}" if metrics['updates_per_hour'] else "N/A"
        )
    
    st.markdown("---")
    
    # Charts
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Difficulty", 
        "📉 Learning", 
        "💰 Rewards", 
        "🎨 Diversity"
    ])
    
    with tab1:
        st.plotly_chart(
            create_difficulty_chart(st.session_state.data['difficulty_changes']),
            use_container_width=True
        )
        
        # Stats
        if st.session_state.data['difficulty_changes']:
            df = pd.DataFrame(st.session_state.data['difficulty_changes'])
            current_diff = df.iloc[-1]['to_level']
            changes = len(df)
            st.markdown(f"""
            **Current Difficulty:** Level {current_diff}  
            **Total Adjustments:** {changes}
            """)
    
    with tab2:
        st.plotly_chart(
            create_loss_chart(st.session_state.data['policy_updates']),
            use_container_width=True
        )
        
        # Stats
        if st.session_state.data['policy_updates']:
            df = pd.DataFrame(st.session_state.data['policy_updates'])
            current_loss = df.iloc[-1]['loss']
            total_epochs = df.iloc[-1]['epoch']
            st.markdown(f"""
            **Current Loss:** {current_loss:.4f}  
            **Total Epochs:** {total_epochs}
            """)
    
    with tab3:
        st.plotly_chart(
            create_reward_chart(st.session_state.data['rewards']),
            use_container_width=True
        )
        
        # Stats
        if st.session_state.data['rewards']:
            df = pd.DataFrame(st.session_state.data['rewards'])
            total_rewards = df['amount'].sum()
            avg_rank = df['rank'].mean()
            st.markdown(f"""
            **Total Earned:** {total_rewards:.4f}  
            **Average Rank:** #{avg_rank:.1f}
            """)
    
    with tab4:
        st.plotly_chart(
            create_diversity_chart(st.session_state.data['rollouts']),
            use_container_width=True
        )
        
        # Stats
        if st.session_state.data['rollouts']:
            df = pd.DataFrame(st.session_state.data['rollouts'])
            avg_div = df['diversity_score'].mean()
            total_rollouts = len(df)
            st.markdown(f"""
            **Average Diversity:** {avg_div:.2f}  
            **Total Rollouts:** {total_rollouts}
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Made with ❤️ for the Gensyn community | 
    <a href='https://github.com/getcakedieyoungx/gensyn-codezero-resources' target='_blank'>GitHub</a> | 
    <a href='https://docs.gensyn.ai' target='_blank'>Gensyn Docs</a>
</div>
""", unsafe_allow_html=True)
