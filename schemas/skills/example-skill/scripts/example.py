#!/usr/bin/env python3
"""Example skill script demonstrating the standard CLI pattern."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Example skill script")
    parser.add_argument("input", help="Input to process")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    result = {"input": args.input, "processed": True, "message": f"Processed: {args.input}"}

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Output written to {args.output}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
