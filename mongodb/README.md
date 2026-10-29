# MongoDB — Onboarding (§5.2)

Part of the [main onboarding plan](../README.md) **Databases** section.

## Learning

1. Work through the [MongoDB Getting Started tutorial](https://www.mongodb.com/docs/manual/tutorial/getting-started/) (interactive / local or Atlas is fine).
2. Complete **five** exercises from [w3resource MongoDB exercises](https://www.w3resource.com/mongodb-exercises/) using the `restaurants` collection (same schema as on that site).

Implement each exercise in **PyMongo** under `exercises/`.

## What you actually need

| Piece | Required? | Notes |
|--------|-----------|--------|
| **PyMongo** (`pip install -r requirements.txt`) | Yes | Talks to MongoDB; it is not a database by itself. |
| **A running MongoDB** | Yes | Local (Docker, Homebrew, etc.) or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) free tier. |
| **`restaurants` data** | Yes | Same w3resource dataset; load once per database. |
| **Docker + `setup.sh`** | No | One convenient way: start Mongo on `27017` and import. Use something else if you prefer. |

### Option A — Homebrew MongoDB (no Docker)

Install and start the server once:

```bash
brew tap mongodb/brew
brew trust mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Recent Homebrew versions refuse to install from an untrusted tap until you run `brew trust mongodb/brew`.

Optional shell client: `brew install mongosh`

Load the exercise data with PyMongo (from `mongodb/`, venv active).

Use localhost unless you intentionally set Atlas:

```bash
source .venv/bin/activate
unset MONGODB_URI
python scripts/import_data.py
```

If you previously exported a broken Atlas URI (empty user/password), `unset MONGODB_URI` fixes
`ConfigurationError: A DNS label is empty`.
python -c "from connection import get_database; print(get_database().restaurants.count_documents({}))"
```

Expect **3772** documents. Default URI is `mongodb://127.0.0.1:27017` (no env vars needed).

Stop the server when you are done:

```bash
brew services stop mongodb-community
```

### Option B — MongoDB Atlas (no Docker, no local `mongod`)

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Add your IP under **Network Access**, create a database user under **Database Access**.
3. Copy the connection string (SRV), then:

```bash
export MONGODB_URI="mongodb+srv://USER:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority"
cd mongodb && source .venv/bin/activate
python scripts/import_data.py
```

Same exercises; only the URI changes.

### Option C — Docker (optional)

Requirements: [Docker](https://www.docker.com/), `curl`, and `unzip`.

```bash
chmod +x mongodb/scripts/setup.sh
./mongodb/scripts/setup.sh
```

Downloads the dataset, starts MongoDB on port `27017`, and runs `mongoimport`.

Stop:

```bash
docker compose -f mongodb/docker-compose.yml down
```

### Python environment

```bash
cd mongodb
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

If `python3 -m venv` fails on **ensurepip** (common with **macOS 26** and/or **Python 3.14**), use [uv](https://github.com/astral-sh/uv) instead:

```bash
cd mongodb
rm -rf .venv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Connection settings (defaults shown):

- `MONGODB_URI` — default `mongodb://127.0.0.1:27017`
- `MONGO_DB` — default `onboarding_mongodb`

## Exercises in this branch

Files follow [w3resource numbering](https://www.w3resource.com/mongodb-exercises/) in order. Complete any **five** for onboarding; working through **1 → 20** is a good path before aggregation (54, 61).

| # | Topic |
|---|--------|
| 01 | All documents |
| 02 | Projection: `restaurant_id`, `name`, `borough`, `cuisine` |
| 03 | Same fields, exclude `_id` |
| 04 | Add `address.zipcode`, exclude `_id` |
| 05 | Filter: borough `Bronx` |
| 06 | Bronx, `.limit(5)` |
| 07 | Bronx, `.skip(5).limit(5)` |
| 08 | Grade score &gt; 90 (`$elemMatch`) |
| 09 | Grade score between 80 and 100 |
| 10 | `address.coord` &lt; -95.754168 (w3resource wording) |
| 11–20 | Filters, regex, `$in` / `$nin`, sort (see docstrings in each file) |
| 54 | Count restaurants per borough (`$group`) |
| 61 | Average grade score per cuisine (`$unwind` + `$group`) |

Edit `exercises/exercise_XX.py` and implement `run(db)`. Then:

```bash
cd mongodb
python main.py 5
python main.py 54 --limit 0
```

Check against w3resource (“Click me to see the solution”) or run the reference implementation:

```bash
python main.py 5 --solution
```

## Submitting

1. Stay on branch `exercise/mongodb`.
2. Open a PR to your fork when ready and ask your supervisor for CR (same flow as other exercises).
3. In the PR description, note which five w3resource numbers you completed if you change the set.
