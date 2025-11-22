#!/bin/bash
# CodeZero Log Finder (RL-Swarm Edition)
# Bu script CodeZero/RL-Swarm log dosyasını bulur

echo "🔍 CodeZero (RL-Swarm) log dosyası aranıyor..."
echo ""

# İlk olarak rl-swarm dizinini kontrol et
if [ -d "$HOME/rl-swarm" ]; then
    echo "✅ rl-swarm dizini bulundu: $HOME/rl-swarm"
    echo ""
    
    # Docker container çalışıyor mu kontrol et
    if command -v docker &> /dev/null; then
        echo "🐳 Docker kontrol ediliyor..."
        
        # Çalışan rl-swarm container'ları bul
        CONTAINERS=$(docker ps --filter "name=rl-swarm" --format "{{.Names}}" 2>/dev/null)
        
        if [ ! -z "$CONTAINERS" ]; then
            echo "✅ Çalışan RL-Swarm container bulundu!"
            echo ""
            echo "📋 Docker loglarını görmek için:"
            echo "   docker logs -f $(echo $CONTAINERS | head -n1)"
            echo ""
            echo "💡 Swarm Pulse için Docker loglarını dosyaya kaydet:"
            echo "   docker logs -f $(echo $CONTAINERS | head -n1) > ~/rl-swarm-logs.txt"
            echo ""
            echo "Sonra config.ini'de şunu kullan:"
            echo "   log_file_path = $HOME/rl-swarm-logs.txt"
            echo ""
            echo "⚠️  Not: Bu dosya gerçek zamanlı güncellenecek!"
            exit 0
        else
            echo "⚠️  Çalışan RL-Swarm container bulunamadı."
            echo "   Container'ı başlatmak için:"
            echo "   cd ~/rl-swarm"
            echo "   docker-compose run --rm --build -Pit swarm-cpu"
        fi
    fi
    
    # rl-swarm dizininde log dosyası ara
    echo ""
    echo "📁 rl-swarm dizininde log dosyaları aranıyor..."
    find "$HOME/rl-swarm" -name "*.log" -type f 2>/dev/null | head -5
fi

echo ""
echo "🔍 Diğer yaygın konumlar kontrol ediliyor..."

# Yaygın log konumları
COMMON_PATHS=(
    "$HOME/rl-swarm/logs/node.log"
    "$HOME/rl-swarm/output.log"
    "$HOME/.codezero/logs/node.log"
    "$HOME/codezero/logs/node.log"
    "/var/log/codezero/node.log"
)

# Her konumu kontrol et
for path in "${COMMON_PATHS[@]}"; do
    if [ -f "$path" ]; then
        echo "✅ Log dosyası bulundu!"
        echo "📁 Path: $path"
        echo ""
        echo "Config dosyanıza ekleyin:"
        echo "log_file_path = $path"
        exit 0
    fi
done

echo ""
echo "💡 Önerilen Çözüm (RL-Swarm için):"
echo ""
echo "1. Docker loglarını dosyaya yönlendir:"
echo "   docker logs -f rl-swarm-swarm-cpu-1 > ~/rl-swarm-logs.txt &"
echo ""
echo "2. Config.ini'de bu dosyayı kullan:"
echo "   log_file_path = $HOME/rl-swarm-logs.txt"
echo ""
echo "3. Swarm Pulse'u başlat:"
echo "   streamlit run app.py"
echo ""
echo "🔍 Manuel arama için:"
echo "   docker ps  # Container adını bul"
echo "   docker logs -f <container-name>  # Logları göster"

