#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$ROOT/data"
DB_NAME="${MONGO_DB:-onboarding_mongodb}"
COLLECTION="${MONGO_COLLECTION:-restaurants}"
ZIP_URL="https://www.w3resource.com/mongodb-exercises/restaurants.zip"

mkdir -p "$DATA_DIR"

if [[ ! -f "$DATA_DIR/restaurants.json" ]]; then
  echo "Downloading w3resource restaurants dataset..."
  curl -fsSL "$ZIP_URL" -o "$DATA_DIR/restaurants.zip"
  unzip -o "$DATA_DIR/restaurants.zip" -d "$DATA_DIR"
  rm -f "$DATA_DIR/restaurants.zip"
fi

echo "Starting MongoDB (Docker)..."
docker compose -f "$ROOT/docker-compose.yml" up -d

echo "Waiting for MongoDB..."
for _ in $(seq 1 30); do
  if docker compose -f "$ROOT/docker-compose.yml" exec -T mongo mongosh --quiet --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "Importing restaurants collection into db '$DB_NAME'..."
docker compose -f "$ROOT/docker-compose.yml" exec -T mongo mongoimport \
  --db "$DB_NAME" \
  --collection "$COLLECTION" \
  --drop \
  --file /dev/stdin <"$DATA_DIR/restaurants.json"

echo "Done. Connect with:"
echo "  mongosh \"mongodb://127.0.0.1:27017/$DB_NAME\""
echo "Run exercises (PyMongo):"
echo "  cd mongodb && python -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt && python main.py 2"
