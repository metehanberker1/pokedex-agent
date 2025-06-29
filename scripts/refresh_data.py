#!/usr/bin/env python
"""CLI wrapper so a cron job can run `python scripts/refresh_data.py --force`."""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.etl import load_all


def main():
    """Main entry point for the refresh script."""
    parser = argparse.ArgumentParser(description="Refresh PokéAPI data in local database")
    parser.add_argument("--force", action="store_true", help="Overwrite existing DB")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    try:
        load_all(force=args.force)
        print("✅ Data refresh completed successfully!")
    except Exception as e:
        print(f"❌ Error refreshing data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 