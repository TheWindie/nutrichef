#!/bin/bash
# deploy.sh — první nasazení na WindieLAB host
# Spusť jako root nebo user s Docker přístupem:
#   bash deploy.sh

set -e

DEPLOY_DIR="/opt/nutrichef"
REPO="https://github.com/radimkocian/nutrichef.git"

echo "🚀 NutriChef deploy — WindieLAB"

# 1. Vytvoř adresáře
mkdir -p $DEPLOY_DIR/data/seeds
echo "  ✅ Adresáře připraveny"

# 2. Naklonuj nebo aktualizuj repo (jen docker-compose.yml + data)
if [ ! -d "$DEPLOY_DIR/.git" ]; then
    git clone --depth 1 $REPO $DEPLOY_DIR
else
    cd $DEPLOY_DIR && git pull
fi
echo "  ✅ Repo aktualizováno"

# 3. Vytvoř .env pokud neexistuje
if [ ! -f "$DEPLOY_DIR/.env" ]; then
    cp $DEPLOY_DIR/.env.example $DEPLOY_DIR/.env
    echo "  ⚠️  Zkopírován .env.example → .env — UPRAV HESLA!"
fi

# 4. Pull images z ghcr.io
cd $DEPLOY_DIR
docker compose pull

# 5. Spusť stack
docker compose up -d

echo ""
echo "🎉 NutriChef běží na http://10.20.10.87:3100"
echo "   API docs: http://10.20.10.87:3100/docs"
