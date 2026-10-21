import argparse
import sys

from slm_reviewer.workflows.summary import summary_workflow
from slm_reviewer.vector_db import build_db

def main():
    parser = argparse.ArgumentParser(description="SLM Reviewer CLI")
    subparsers = parser.add_subparsers(dest="command")

    db_parser = subparsers.add_parser("build-db", help="Rebuild the vector database")

    summary_parser = subparsers.add_parser("summary", help="Summarize a .qmd file")
    summary_parser.add_argument("--file", type=str, required=True, help="Path to the input .qmd file")
    summary_parser.add_argument("--out", type=str, required=True, help="Path to save the generated markdown summary")
    summary_parser.add_argument("--model", type=str, required=True, help="LLM to use for synthesis")
    summary_parser.add_argument("--ctx", type=int, default=8192, help="Context window size")

    args = parser.parse_args()

    if args.command == "build-db":
        build_db()
        
    elif args.command == "summary":
        summary_workflow(
            file_path=args.file,
            output_path=args.out,
            model_name=args.model,
            num_ctx=args.ctx
        )
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()