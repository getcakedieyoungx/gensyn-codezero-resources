# 🔗 Gensyn Node Watcher (On-Chain)

Bu araç, Gensyn nodunuzun durumunu **Blockchain üzerinden** takip eder.
Log dosyası, SSH veya kurulum gerektirmez. Sadece cüzdan adresinizi (EOA) girmeniz yeterlidir.

## 🚀 Hemen Kullan (Kurulumsuz)

Bu aracı kendi bilgisayarında veya VPS'inde çalıştırmak zorunda değilsin!
Aşağıdaki butona tıklayarak **Streamlit Cloud** üzerinde ücretsiz olarak yayınlayabilirsin.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=getcakedieyoungx/gensyn-codezero-resources&branch=master&mainModule=node-watcher/watcher.py)

1. Butona tıkla.
2. GitHub ile giriş yap.
3. "Deploy" de.
4. **Bitti!** Artık sana özel bir web siten var (örn: `gensyn-watcher.streamlit.app`).

---

## 💻 Yerel Kurulum (İstersen)

Eğer kendi bilgisayarında çalıştırmak istersen:

```bash
pip install -r requirements.txt
streamlit run watcher.py
```
