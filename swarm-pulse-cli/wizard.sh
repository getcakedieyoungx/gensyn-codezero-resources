#!/bin/bash
# Swarm Pulse Wizard 🧙‍♂️
# Automatically detects your setup and configures monitoring

echo "🧙‍♂️ Swarm Pulse Wizard başlatılıyor..."
echo ""

# 1. Docker Kontrolü
if command -v docker &> /dev/null; then
    CONTAINER=$(docker ps --filter "name=rl-swarm" --format "{{.Names}}" | head -n1)
    if [ ! -z "$CONTAINER" ]; then
        echo "🐳 Docker container bulundu: $CONTAINER"
        echo "   Monitor başlatılıyor..."
        ./monitor.py --container "$CONTAINER"
        exit 0
    fi
fi

# 2. Screen Kontrolü
if command -v screen &> /dev/null; then
    # Screen sessionlarını bul
    SCREENS=$(screen -ls | grep -E "\.swarm|\.codezero" | awk '{print $1}')
    
    if [ ! -z "$SCREENS" ]; then
        SESSION=$(echo "$SCREENS" | head -n1)
        NAME=$(echo "$SESSION" | cut -d. -f2)
        
        echo "🖥️  Screen session bulundu: $NAME ($SESSION)"
        
        LOG_FILE="$HOME/gensyn-monitor.log"
        
        # Screen logging'i aktif et
        echo "   📝 Logging aktif ediliyor -> $LOG_FILE"
        screen -S "$SESSION" -X logfile "$LOG_FILE"
        screen -S "$SESSION" -X log on
        
        # Biraz bekle log oluşsun
        echo "   ⏳ Log verisi bekleniyor..."
        sleep 2
        
        if [ -f "$LOG_FILE" ]; then
            echo "   ✅ Log dosyası oluşturuldu!"
            echo "   Monitor başlatılıyor..."
            ./monitor.py --log-file "$LOG_FILE"
            exit 0
        else
            echo "   ⚠️  Log dosyası oluşturulamadı. İzinleri kontrol edin."
        fi
    fi
fi

# 3. Manuel Log Arama
echo "🔍 Otomatik algılama başarısız. Log dosyası aranıyor..."
LOG_FILE=$(find ~ -name "node.log" -o -name "output.log" -mtime -1 2>/dev/null | head -n1)

if [ ! -z "$LOG_FILE" ]; then
    echo "📁 Olası log dosyası bulundu: $LOG_FILE"
    read -p "   Bu dosyayı kullanmak ister misiniz? (E/h) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ee]$ ]]; then
        ./monitor.py --log-file "$LOG_FILE"
        exit 0
    fi
fi

echo ""
echo "❌ Otomatik kurulum yapılamadı."
echo "Lütfen manuel başlatın:"
echo "   ./monitor.py --log-file /path/to/your/log.txt"
