#!/bin/bash
set -e

echo "🛠️ Sunray telepítő script indul..."

# 1. Alapcsomagok telepítése
echo "📦 Függőségek telepítése (cmake, build-essential, git)..."
sudo apt update
sudo apt install -y git cmake build-essential

# 2. Repo klónozása (ha nem létezne)
if [ ! -d "$HOME/Worx" ]; then
  echo "📥 Klónozás: adamant666/Worx → ~/Worx"
  git clone https://github.com/adamant666/Worx.git ~/Worx
else
  echo "🔄 Repo már létezik, frissítés..."
  cd ~/Worx
  git pull
fi

# 3. Fordítás
cd ~/Worx/alfred
if [ ! -f config.h ]; then
  echo "📄 config.h létrehozása az alapértelmezett config_alfred.h alapján..."
  cp config_alfred.h config.h
fi

echo "🏗️ Build könyvtár létrehozása és fordítás..."
mkdir -p build
cd build
cmake ..
make -j$(nproc)

echo ""
echo "✅ Telepítés és fordítás kész!"
echo "👉 Az indításhoz futtasd: ~/Worx/alfred/build/sunray"
