# 🌊 Swarm Pulse - Tek Komut Kurulum

## ⚡ Hızlı Başlangıç (1 Komut!)

```bash
# VPS'te rl-swarm dizinine git
cd ~/rl-swarm

# Swarm Pulse'u clone et
git clone https://github.com/getcakedieyoungx/gensyn-codezero-resources.git

# Setup script'i çalıştır - HER ŞEYİ YAPAR!
cd gensyn-codezero-resources/swarm-pulse
chmod +x setup.sh
./setup.sh
```

**Bu kadar! Script otomatik olarak:**
- ✅ Docker container'ı bulur
- ✅ Logları dosyaya yönlendirir
- ✅ Config dosyasını oluşturur
- ✅ Dependencies kurar
- ✅ Streamlit'i başlatır

---

## 🔗 Local Bilgisayardan Bağlan

**Yeni terminal aç (local bilgisayarında):**
```bash
ssh -L 8501:localhost:8501 user@vps-ip
```

**Browser'da aç:**
```
http://localhost:8501
```

**DONE!** 🎉

---

## 🛠️ Manuel Kurulum (İsteğe Bağlı)

Eğer setup.sh çalışmazsa:

```bash
# 1. Container adını bul
docker ps

# 2. Logları yönlendir
docker logs -f <container-name> > ~/rl-swarm-logs.txt &

# 3. Config oluştur
cp config.ini.example config.ini
nano config.ini
# log_file_path = /home/user/rl-swarm-logs.txt
# auto_start = true

# 4. Başlat
streamlit run app.py --server.address=0.0.0.0
```

---

## ❓ Sorun Giderme

**"Container bulunamadı" hatası:**
```bash
cd ~/rl-swarm
docker-compose run --rm --build -Pit swarm-cpu
# Sonra setup.sh'yi tekrar çalıştır
```

**"Permission denied" hatası:**
```bash
chmod +x setup.sh
```

**Port 8501 kullanımda:**
```bash
# Başka port kullan
streamlit run app.py --server.address=0.0.0.0 --server.port=8502
```

---

## 📝 Notlar

- Setup script her çalıştırıldığında config'i yeniden oluşturur
- Log dosyası gerçek zamanlı güncellenir
- Streamlit kapanırsa sadece `./setup.sh` tekrar çalıştır
