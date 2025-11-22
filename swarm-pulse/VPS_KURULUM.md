# VPS Kurulum Rehberi - Swarm Pulse

## 🎯 Sorun Çözüldü!

Artık VPS'te çalıştırmak çok daha kolay. Log dosyasını upload etmeye gerek yok!

## ⚡ Hızlı Kurulum (VPS'te)

### 1. Tool'u İndir ve Kur

```bash
git clone https://github.com/getcakedieyoungx/gensyn-codezero-resources.git
cd gensyn-codezero-resources/swarm-pulse
pip install -r requirements.txt
```

### 2. Log Dosyasını Bul

**RL-Swarm (Docker) kullanıyorsanız (çoğu kişi):**

```bash
# 1. Script'i çalıştır
chmod +x find_log.sh
./find_log.sh

# 2. Docker loglarını dosyaya yönlendir
docker ps  # Container adını bul (örn: rl-swarm-swarm-cpu-1)
docker logs -f rl-swarm-swarm-cpu-1 > ~/rl-swarm-logs.txt &

# 3. Bu dosyayı config.ini'de kullan
# log_file_path = /home/your-user/rl-swarm-logs.txt
```

**Neden Docker logları?**
- RL-Swarm Docker container içinde çalışır
- Loglar container içinde, dışarıdan erişilemez
- Docker logs komutu ile logları dosyaya yönlendiriyoruz
- Swarm Pulse bu dosyayı okuyabilir

**Manuel yol - Yaygın konumlar:**
```bash
# rl-swarm dizinini bul
cd ~/rl-swarm

# Docker container'ları listele
docker ps

# Logları göster
docker logs -f <container-name>
```

### 3. Config Dosyasını Oluştur

```bash
cp config.ini.example config.ini
nano config.ini
```

**config.ini içeriği:**
```ini
[DEFAULT]
# CodeZero node log dosyanızın path'i
log_file_path = /path/to/your/codezero/node.log

# Otomatik başlat (true yapın)
auto_start = true

# Yenileme aralığı (saniye)
refresh_interval = 2
```

### 3. Dashboard'u Çalıştır

```bash
streamlit run app.py --server.address=0.0.0.0
```

### 4. Local Bilgisayardan Bağlan

**Yeni terminal açın (local bilgisayarınızda):**
```bash
ssh -L 8501:localhost:8501 user@your-vps-ip
```

### 5. Browser'da Aç

`http://localhost:8501` adresine git - **loglar otomatik yüklenecek!** 🎉

---

## ✅ Artık Yapmanız Gerekenler

1. ✅ VPS'te `config.ini` oluştur
2. ✅ Log dosyasının path'ini ayarla
3. ✅ `auto_start = true` yap
4. ✅ Streamlit'i çalıştır
5. ✅ SSH tunnel ile bağlan
6. ✅ Browser'da aç - **DONE!**

## 🔥 Avantajlar

- ❌ File upload yok
- ❌ Manuel log kopyalama yok
- ✅ Otomatik yükleme
- ✅ Real-time monitoring
- ✅ Tunnel üzerinden çalışır

---

**Şimdi deneyebilirsin!** VPS'te bu adımları takip et, sorun yaşarsan söyle.
