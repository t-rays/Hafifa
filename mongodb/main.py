"""Run a w3resource-style exercise by number."""

import argparse
import importlib.util
import sys
from pathlib import Path

from connection import get_database

ROOT = Path(__file__).resolve().parent


def _load_run(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "run"):
        raise AttributeError(f"{module_path.name} must define run(db)")
    return module.run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MongoDB onboarding exercises.")
    parser.add_argument(
        "number",
        type=int,
        help="w3resource exercise number (e.g. 1–20, 54, 61)",
    )
    parser.add_argument(
        "--solution",
        action="store_true",
        help="Run reference solution instead of your exercise file",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max documents to print (default 5; use 0 for all)",
    )
    args = parser.parse_args()

    folder = "solutions" if args.solution else "exercises"
    path = ROOT / folder / f"exercise_{args.number:02d}.py"
    if not path.is_file():
        print(f"No file: {path}", file=sys.stderr)
        sys.exit(1)

    db = get_database()
    run = _load_run(path)
    result = run(db)

    if result is None:
        print("(run returned None)")
        return

    if isinstance(result, (list, tuple)):
        items = result
    else:
        items = list(result)

    total = len(items)
    show = items if args.limit == 0 else items[: args.limit]
    for doc in show:
        print(doc)
    if args.limit and total > args.limit:
        print(f"... ({total - args.limit} more; use --limit 0 to print all)")


if __name__ == "__main__":
    main()
