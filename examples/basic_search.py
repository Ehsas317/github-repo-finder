from github_repo_finder.core.engine import RepoFinderEngine
import os

def run_example():
    # Initialize the engine
    # It will use the GITHUB_TOKEN environment variable if available
    token = os.environ.get("GITHUB_TOKEN")
    engine = RepoFinderEngine(github_token=token)

    # Search for "fastapi" repositories
    query = "fastapi"
    print(f"Searching for repositories related to: {query}...")
    
    result = engine.find_repositories(query, limit=5, output_mode="markdown")

    print("\n--- Search Results (Markdown) ---")
    print(result["content"])

    # Search with a more compact output
    print(f"\nSearching for repositories related to: {query} (Compact Mode)...")
    compact_result = engine.find_repositories(query, limit=3, output_mode="compact")
    
    print("\n--- Search Results (Compact JSON) ---")
    import json
    print(json.dumps(compact_result["content"], indent=2))

if __name__ == "__main__":
    run_example()
