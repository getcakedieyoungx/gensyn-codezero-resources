# 🌊 Swarm Pulse

**Real-time Log Visualizer for Gensyn's CodeZero**

A lightweight Python tool that helps CodeZero node runners understand if they're actually learning by visualizing key metrics in real-time.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## 🎯 Features

- **📈 Real-time Monitoring** - Watch your node's performance live with auto-refreshing charts
- **📊 Difficulty Tracking** - Visualize how problem complexity adjusts based on swarm performance
- **📉 Learning Progress** - Track loss metrics and policy updates over time
- **💰 Reward Analysis** - Monitor earnings and performance rankings
- **🎨 Diversity Scores** - See how unique your solutions are compared to the swarm
- **🏥 Health Dashboard** - Get instant feedback on your node's overall performance

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/getcakedieyoungx/gensyn-codezero-resources.git
cd gensyn-codezero-resources/swarm-pulse

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Option 1: File Upload Mode

1. Export your CodeZero node logs to a file
2. Click "Upload File" in the sidebar
3. Select your log file
4. View your metrics!

### Option 2: Real-time Monitoring

1. Select "Real-time Monitor" mode
2. Enter the path to your active log file (e.g., `/var/log/codezero/node.log`)
3. Click "Start"
4. Watch your charts update live!

### Option 3: Try the Demo

Click "📋 Use Sample Data" to explore the tool with pre-loaded sample logs.

## 📊 What Gets Visualized

### Difficulty Adjustment Timeline
Shows how the network dynamically adjusts problem difficulty based on swarm success rate. Unlike traditional mining (difficulty only increases), CodeZero adjusts in both directions to keep the swarm in optimal learning conditions.

### Learning Progress (Loss)
Tracks your node's loss metric over time. Lower is better:
- 🟢 **< 0.01** - Highly optimized
- 🟡 **0.01 - 0.05** - Getting competent  
- 🔴 **> 0.1** - Still learning basics

### Reward Analysis
Displays your earnings and performance rank over time. CodeZero uses **GRPO (Group Relative Policy Optimization)**, so rewards are relative to other solvers.

### Diversity Score
Measures how unique your solutions are. Higher diversity (> 0.6) means you're contributing novel approaches that help the entire swarm learn faster.

## 🔍 Understanding Your Logs

Not sure what your log messages mean? Check out the comprehensive guide:

👉 **[How to Read Your CodeZero Logs](https://github.com/getcakedieyoungx/gensyn-codezero-resources/blob/main/codezero_log_guide.md)**

## 🏥 Health Status

The dashboard automatically calculates your node's health based on:

- **🟢 Healthy** - All metrics looking good!
- **🟡 Warning** - Some metrics need attention
- **🔴 Critical** - Multiple issues detected

## 💾 Exporting Data

Click "📥 Download CSV" in the sidebar to export all parsed metrics for further analysis.

## 🛠️ Technical Details

### Log Format

Swarm Pulse parses CodeZero logs with the following patterns:

```
[YYYY-MM-DD HH:MM:SS] INFO: Policy update received (epoch=N, loss=X.XXXX)
[YYYY-MM-DD HH:MM:SS] INFO: Reward received (amount=X.XXXX, rank=N/M)
[YYYY-MM-DD HH:MM:SS] INFO: Difficulty adjusted: N → M (swarm_success_rate=X.XX)
[YYYY-MM-DD HH:MM:SS] DEBUG: Rollout generated (problem_id=0xXXXX, diversity_score=X.XX)
```

### Architecture

```
swarm-pulse/
├── app.py              # Streamlit dashboard
├── log_parser.py       # Regex-based log parsing
├── log_watcher.py      # Real-time file monitoring
├── visualizations.py   # Plotly chart generation
└── sample_logs/        # Demo data
```

## 🤝 Contributing

Found a bug or want to add a feature? PRs welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Resources

- [Gensyn Official Docs](https://docs.gensyn.ai)
- [CodeZero Documentation](https://docs.gensyn.ai/codezero)
- [Gensyn Discord](https://discord.gg/gensyn)
- [CodeZero Log Guide](https://github.com/getcakedieyoungx/gensyn-codezero-resources)

## 📝 License

MIT License - feel free to use this tool for your own nodes!

## 🙏 Acknowledgments

Built with ❤️ for the Gensyn community. Special thanks to the CodeZero team for building such an innovative cooperative AI network.

---

**Remember:** In CodeZero, we learn faster when we share notes. 🤝🤖
