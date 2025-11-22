import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Page Config
st.set_page_config(
    page_title="Gensyn Node Watcher",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
EXPLORER_API = "https://gensyn-testnet.explorer.alchemy.com/api"
GENSYN_CONTRACT = "0xFaD7C5e93f28257429569B854151A1B8DCD404c2"

# Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #464b5d;
    }
    .status-online {
        color: #00ff00;
        font-weight: bold;
    }
    .status-offline {
        color: #ff4b4b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def get_transactions(address):
    """Fetch transactions from Blockscout"""
    try:
        url = f"{EXPLORER_API}?module=account&action=txlist&address={address}&sort=desc"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == '1':
            return data['result']
        return []
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

def analyze_activity(address, txs):
    """Analyze transactions for node activity"""
    if not txs:
        return None
    
    df = pd.DataFrame(txs)
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
    
    # Filter outgoing to contract (Node Activity)
    # Note: We assume any outgoing tx to the contract is activity
    activity_txs = df[
        (df['from'].str.lower() == address.lower()) & 
        (df['to'].str.lower() == GENSYN_CONTRACT.lower())
    ]
    
    last_active = activity_txs['timeStamp'].max() if not activity_txs.empty else None
    total_txs = len(activity_txs)
    
    # Determine status (Active if last tx < 20 mins ago)
    is_online = False
    if last_active:
        time_diff = datetime.now() - last_active
        if time_diff.total_seconds() < 1200:  # 20 mins
            is_online = True
            
    return {
        'last_active': last_active,
        'total_txs': total_txs,
        'is_online': is_online,
        'history': activity_txs
    }

def main():
    st.title("🔗 Gensyn Node Watcher")
    st.markdown("Monitor your node health directly from the blockchain. No logs required.")
    
    # Sidebar
    st.sidebar.header("Configuration")
    address = st.sidebar.text_input("Wallet Address (EOA)", placeholder="0x...")
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=True)
    
    if not address:
        st.info("👈 Please enter your Wallet Address in the sidebar to start.")
        return

    # Main Content
    if auto_refresh:
        time.sleep(1)
        st.rerun()
        
    with st.spinner("Fetching on-chain data..."):
        txs = get_transactions(address)
        data = analyze_activity(address, txs)
    
    if not data:
        st.warning("No transactions found for this address.")
        return

    # Status Banner
    status_color = "green" if data['is_online'] else "red"
    status_text = "ONLINE 🟢" if data['is_online'] else "OFFLINE 🔴"
    last_seen = data['last_active'].strftime("%Y-%m-%d %H:%M:%S") if data['last_active'] else "Never"
    
    st.markdown(f"""
        <div style="padding: 20px; background-color: rgba({('0,255,0' if data['is_online'] else '255,0,0')}, 0.1); border-radius: 10px; border: 1px solid {status_color}; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0; color: {status_color};">{status_text}</h2>
            <p style="margin:5px 0 0 0; opacity: 0.8;">Last Seen: {last_seen}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Submissions", data['total_txs'])
    with col2:
        # Placeholder for rewards (need token txs for accurate count)
        st.metric("Estimated Rewards", "Coming Soon") 
    with col3:
        time_since = "N/A"
        if data['last_active']:
            diff = datetime.now() - data['last_active']
            mins = int(diff.total_seconds() / 60)
            time_since = f"{mins} mins ago"
        st.metric("Time Since Last Tx", time_since)

    # Activity Chart
    if not data['history'].empty:
        st.subheader("Activity History")
        hist = data['history'].copy()
        hist['date'] = hist['timeStamp'].dt.floor('H') # Group by hour
        hourly_counts = hist.groupby('date').size().reset_index(name='count')
        
        fig = px.bar(hourly_counts, x='date', y='count', title="Submissions per Hour")
        fig.update_layout(xaxis_title="Time", yaxis_title="Submissions")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Raw Transactions"):
            st.dataframe(data['history'][['timeStamp', 'hash', 'blockNumber']].head(50))

if __name__ == "__main__":
    main()
