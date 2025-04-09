#!/bin/bash
set -e

echo "🛠️ Sunray telepítő script indul..."
echo "📍 Célkönyvtár: ~/sunray"

# 1. Csomagok
echo "📦 Függőségek telepítése (cmake, build-essential, git)..."
sudo apt update
sudo apt install -y git cmake build-essential

# 2. Repo klónozása
if [ ! -d "$HOME/sunray" ]; then
  echo "📥 Klónozás: adamant666/Worx → ~/sunray"
  git clone https://github.com/adamant666/Worx.git ~/sunray
else
  echo "📁 A ~/sunray már létezik – frissítés..."
  cd ~/sunray
  git pull
fi

# 3. Fordítás
cd ~/sunray/alfred

if [ ! -f config.h ]; then
  echo "📄 config.h létrehozása a config_Worx.h alapján..."
  cp ../config_Worx.h config.h
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
  echo "❌ Fordítási hiba! Ellenőrizd a config.h tartalmát."
  exit 1
fi

# 4. Indítás opcionálisan
read -p "🚀 Elindítod most a Sunray programot? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  ./sunray
fi
