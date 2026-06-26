import json
import os
from typing import Dict, Any, List
from .core.engine import RepoFinderEngine

# Simple MCP Server Implementation
# In a real-world scenario, this would use the mcp-python-sdk
# For this project, we provide a clean interface that can be easily wrapped.

class MCPServer:
    def __init__(self, token: str = None):
        self.engine = RepoFinderEngine(github_token=token or os.environ.get("GITHUB_TOKEN"))

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "search_repositories",
                "description": "Find the best GitHub repositories for a given topic with ranking and filtering.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The topic or keywords to search for."},
                        "limit": {"type": "integer", "description": "Number of results (default 10)."},
                        "mode": {"type": "string", "enum": ["markdown", "detailed", "json", "compact", "llm"], "default": "llm"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_trending",
                "description": "Get trending repositories on GitHub.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "language": {"type": "string", "description": "Filter by programming language."},
                        "since": {"type": "string", "enum": ["daily", "weekly", "monthly"], "default": "daily"}
                    }
                }
            }
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name == "search_repositories":
            query = arguments.get("query")
            limit = arguments.get("limit", 10)
            mode = arguments.get("mode", "llm")
            
            result = self.engine.find_repositories(query, limit=limit, output_mode=mode)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result["content"]) if mode != "markdown" else result["content"]
                    }
                ]
            }
        
        elif name == "get_trending":
            # Implementation for trending would go here, 
            # likely using a different search query like 'created:>YYYY-MM-DD'
            lang = arguments.get("language", "")
            q = f"created:>{(os.environ.get('DATE') or '2026-06-01')} {lang}".strip()
            result = self.engine.find_repositories(q, limit=10, output_mode="llm")
            return {
                "content": [{"type": "text", "text": json.dumps(result["content"])}]
            }
        
        raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    # Example usage for MCP stdio interface
    import sys
    # This is a placeholder for the actual MCP loop
    print("GitHub Repo Finder MCP Server started.", file=sys.stderr)
