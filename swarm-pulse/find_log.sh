#!/bin/bash
# CodeZero Log Finder
# Bu script CodeZero node log dosyasını bulur

echo "🔍 CodeZero log dosyası aranıyor..."
echo ""

# Yaygın log konumları
COMMON_PATHS=(
    "$HOME/.codezero/logs/node.log"
    "$HOME/codezero/logs/node.log"
    "/var/log/codezero/node.log"
    "/opt/codezero/logs/node.log"
    "$HOME/.local/share/codezero/logs/node.log"
    "./logs/node.log"
    "./node.log"
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

echo "❌ Yaygın konumlarda log dosyası bulunamadı."
echo ""
echo "Manuel arama yapılıyor..."
echo ""

# Find komutu ile ara (son 24 saatte değişmiş .log dosyaları)
echo "Son 24 saatte değişmiş .log dosyaları:"
find $HOME -name "*.log" -mtime -1 -type f 2>/dev/null | grep -i "codezero\|node" | head -10

echo ""
echo "💡 İpucu: CodeZero node'unuzu nasıl çalıştırdığınızı kontrol edin."
echo "   Genellikle log dosyası node'un çalıştığı dizinde veya ~/.codezero/ altındadır."
echo ""
echo "🔍 Manuel arama için:"
echo "   find / -name '*node*.log' 2>/dev/null | grep codezero"
