import sys
import argparse
import json
from .core.engine import RepoFinderEngine
from .utils.errors import RepoFinderError

def main():
    parser = argparse.ArgumentParser(description="GitHub Repo Finder - Discover the best repositories.")
    parser.add_argument("query", help="Search query (e.g., 'machine learning', 'python web framework')")
    parser.add_argument("--limit", type=int, default=10, help="Number of results to return")
    parser.add_argument("--mode", choices=["markdown", "detailed", "json", "compact", "llm"], 
                        default="markdown", help="Output format")
    parser.add_argument("--token", help="GitHub Personal Access Token")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")

    args = parser.parse_args()

    try:
        engine = RepoFinderEngine(github_token=args.token, use_cache=not args.no_cache)
        result = engine.find_repositories(args.query, limit=args.limit, output_mode=args.mode)
        
        if args.mode in ["json", "compact", "llm"]:
            print(json.dumps(result["content"], indent=2))
        else:
            print(f"\n# Search Results for: {args.query}")
            print(f"Found {result['total_available']} total repositories. Showing top {result['count']}.\n")
            print(result["content"])
            
    except RepoFinderError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
