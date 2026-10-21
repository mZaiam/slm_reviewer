import argparse
import sys
import os
from dotenv import load_dotenv

from slm_reviewer.workflows.suggestion import suggestion_app 

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="SLM Reviewer Agentic Workflows")
    subparsers = parser.add_subparsers(dest="command", help="Available workflows")

    # Command: suggest
    suggest_parser = subparsers.add_parser("suggest", help="Run the topic suggestion workflow")
    suggest_parser.add_argument("--topic", type=str, required=True, help="The main topic to suggest subtopics for")
    suggest_parser.add_argument("--n", type=int, default=3, help="Number of suggestions to generate")

    # Command: synthesize
    synth_parser = subparsers.add_parser("synthesize", help="Synthesize a .qmd file")
    synth_parser.add_argument("--file", type=str, required=True, help="Path to the .qmd file")

    args = parser.parse_args()

    if args.command == "suggest":
        print(f"Running suggestion workflow for topic: {args.topic}")
        # initial_state = {"topic": args.topic, "suggestions_count": 0}
        # suggestion_app.invoke(initial_state)

    elif args.command == "synthesize":
        print(f"Synthesizing {args.file}...")
        # Add synthesis workflow trigger here

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()