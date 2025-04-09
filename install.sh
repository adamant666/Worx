#!/bin/bash
set -e

echo "🛠️ Sunray telepítő script indul..."
echo "📍 Célkönyvtár: ~/sunray"

# 1. Alapcsomagok telepítése
echo "📦 Függőségek telepítése (cmake, build-essential, git)..."
sudo apt update
sudo apt install -y git cmake build-essential

# 2. Klónozás ~/sunray könyvtárba
if [ ! -d "$HOME/sunray" ]; then
  echo "📥 Klónozás: adamant666/Worx → ~/sunray"
  git clone https://github.com/adamant666/Worx.git ~/sunray
else
  echo "📁 A ~/sunray könyvtár már létezik – frissítem a repót..."
  cd ~/sunray
  git pull
fi

# 3. Fordítás
cd ~/sunray/alfred

if [ ! -f config.h ]; then
  echo "📄 config.h létrehozása a config_alfred.h alapján..."
  cp config_alfred.h config.h
else
  echo "✅ config.h már létezik – kihagyva a másolást."
fi

echo "🏗️ Build mappa létrehozása és fordítás..."
mkdir -p build
cd build

cmake .. && make -j$(nproc)

if [ $? -eq 0 ]; then
  echo "✅ Fordítás sikeres!"
else
  echo "❌ Fordítási hiba! Ellenőrizd a config.h beállításait."
  exit 1
fi

# 4. Opcionális futtatás
read -p "🚀 Szeretnéd most elindítani a Sunray programot? [y/N] " -n 1 -r
echo    # új sor
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "▶️ Indítás..."
  ./sunray
else
  echo "⏭️ Indítás kihagyva."
fi
