# 🌊 Swarm Pulse CLI

**Terminal-based CodeZero Node Monitor** - `htop` tarzı, terminalden izle!

## ⚡ Hızlı Başlangıç (Wizard 🧙‍♂️)

En kolayı! Script sizin için her şeyi ayarlar (Docker veya Screen):

```bash
# 1. İndir
git clone https://github.com/getcakedieyoungx/gensyn-codezero-resources.git
cd gensyn-codezero-resources/swarm-pulse-cli

# 2. Çalıştır
chmod +x install.sh wizard.sh monitor.py
./install.sh
./wizard.sh
```

**Wizard ne yapar?**
- 🐳 **Docker:** Container'ı bulur ve bağlanır
- 🖥️ **Screen:** Çalışan session'ı bulur (`swarm` veya `codezero`), loglamayı açar ve bağlanır
- 📁 **Dosya:** Sistemdeki log dosyalarını tarar

---

## 🚀 Manuel Kullanım

## 📊 Özellikler

- ✅ **Gerçek Zamanlı Monitoring** - 2 saniyede bir güncellenir
- ✅ **Docker Otomatik Bulma** - Container'ı otomatik bulur
- ✅ **Health Status** - 🟢 Healthy / 🟡 Warning / 🔴 Critical
- ✅ **Sparkline Charts** - Loss ve reward trendleri
- ✅ **Terminal-based** - SSH üzerinden çalışır, browser gerekmez!

## 🎯 Gösterilen Metrikler

- 📊 Current Loss
- 📉 Average Loss (son 20)
- 💰 Total Rewards
- 🎯 Difficulty Level
- 🎨 Average Diversity
- ⚡ Epoch Count
- 📈 Loss Trend (sparkline)
- 💵 Reward Trend (sparkline)

## 🚀 Kullanım

### Docker Kullanıcıları (Otomatik)

```bash
# Container'ı otomatik bulur
./monitor.py
```

### Screen/Tmux Kullanıcıları (Manuel)

**Seçenek 1: Log dosyasını belirt**
```bash
# rl-swarm'ı screen'de çalıştır ve log'a yaz
screen -S codezero
python run_rl_swarm.py 2>&1 | tee ~/codezero.log

# Başka terminalde monitor'u başlat
./monitor.py --log-file ~/codezero.log
```

**Seçenek 2: Mevcut log dosyasını kullan**
```bash
# Log dosyasını bul
find ~ -name "*.log" -mtime -1

# Monitor'u başlat
./monitor.py --log-file /path/to/your/log.txt
```

### Belirli Container İzle

```bash
./monitor.py --container rl-swarm-swarm-cpu-1
```

**Çıkmak için:** `Ctrl+C`

## 📸 Örnek Görünüm

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 Swarm Pulse CLI | Status: 🟢 HEALTHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Current Loss       0.0345
📉 Avg Loss (20)      0.0378
💰 Total Rewards      0.1234 GENSYN
🎯 Difficulty         Level 4
🎨 Avg Diversity      0.67
⚡ Epochs             142

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loss Trend ↘
▇▆▅▅▄▄▃▃▂▂▁▁▂▂▃▃▄▄▅▅
Min: 0.0320 | Max: 0.0450 | Current: 0.0345
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Container: rl-swarm-swarm-cpu-1 | Last Update: 23:45:12 | Press Ctrl+C to exit
```

## 🛠️ Gereksinimler

- Python 3.6+
- Docker (rl-swarm çalışıyor olmalı)
- `rich` library (otomatik kurulur)

## ❓ Sorun Giderme

**"Container not found":**
```bash
# rl-swarm'ı başlat
cd ~/rl-swarm
docker-compose run --rm --build -Pit swarm-cpu

# Sonra monitor'u tekrar çalıştır
./monitor.py
```

**"Permission denied":**
```bash
chmod +x monitor.py install.sh
```

## 🎯 Avantajlar

- ❌ Browser gerekmez
- ❌ Port forwarding gerekmez
- ❌ Streamlit gerekmez
- ✅ SSH üzerinden çalışır
- ✅ Minimal resource kullanımı
- ✅ Hızlı ve basit

---

**Made with ❤️ for the Gensyn community**
