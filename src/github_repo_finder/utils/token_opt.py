import json
from typing import List, Dict, Any
from ..core.models import Repository

class TokenOptimizer:
    @staticmethod
    def estimate_tokens(text: str) -> int:
        # Rough estimation: 1 token ~= 4 characters for English
        return len(text) // 4

    @staticmethod
    def deduplicate(repos: List[Repository]) -> List[Repository]:
        seen = set()
        unique_repos = []
        for repo in repos:
            if repo.full_name not in seen:
                seen.add(repo.full_name)
                unique_repos.append(repo)
        return unique_repos

    @staticmethod
    def compress_results(repos: List[Repository], mode: str = "llm") -> List[Dict[str, Any]]:
        if mode == "compact":
            return [repo.to_compact_dict() for repo in repos]
        elif mode == "llm":
            # Strip very verbose fields that LLMs don't usually need for discovery
            results = []
            for repo in repos:
                d = repo.to_dict()
                # Keep essential info only
                essential = {
                    "name": d["full_name"],
                    "desc": d["description"],
                    "url": d["html_url"],
                    "stars": d["stars"],
                    "lang": d["language"],
                    "pushed": d["pushed_at"][:10]
                }
                results.append(essential)
            return results
        return [repo.to_dict() for repo in repos]

    @staticmethod
    def format_as_markdown(repos: List[Repository], detailed: bool = False) -> str:
        lines = []
        for i, repo in enumerate(repos, 1):
            if detailed:
                lines.append(f"### {i}. [{repo.full_name}]({repo.html_url})")
                lines.append(f"- **Stars:** {repo.stars} | **Language:** {repo.language} | **Updated:** {repo.pushed_at.strftime('%Y-%m-%d')}")
                lines.append(f"- **Description:** {repo.description}")
                lines.append(f"- **Score:** {repo.score} (Health: {repo.health_score}, Freshness: {repo.freshness_score})")
                lines.append("")
            else:
                lines.append(f"{i}. **{repo.full_name}** ({repo.stars}★) - {repo.description[:80]}... [Link]({repo.html_url})")
        
        return "\n".join(lines)
