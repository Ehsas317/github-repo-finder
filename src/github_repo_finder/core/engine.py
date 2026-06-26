from typing import List, Optional, Dict, Any
from .search import GitHubSearchClient
from .ranking import RankingEngine
from .models import Repository, SearchResult
from ..utils.caching import CacheManager
from ..utils.token_opt import TokenOptimizer

class RepoFinderEngine:
    def __init__(self, github_token: Optional[str] = None, use_cache: bool = True):
        self.client = GitHubSearchClient(github_token)
        self.ranker = RankingEngine()
        self.cache = CacheManager() if use_cache else None
        self.optimizer = TokenOptimizer()

    def find_repositories(self, query: str, limit: int = 10, output_mode: str = "markdown") -> Dict[str, Any]:
        cache_key = f"search:{query}:{limit}"
        
        # 1. Check Cache
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return self._prepare_output(cached_result, output_mode)

        # 2. Search
        search_result = self.client.search_repositories(query, per_page=max(limit * 2, 30))
        
        # 3. Rank
        ranked_repos = self.ranker.rank_repositories(search_result.repositories)
        
        # 4. Deduplicate & Limit
        unique_repos = self.optimizer.deduplicate(ranked_repos)
        top_repos = unique_repos[:limit]
        
        # Update search result with ranked/filtered repos
        search_result.repositories = top_repos
        
        # 5. Save to Cache
        if self.cache:
            self.cache.set(cache_key, search_result)
            
        return self._prepare_output(search_result, output_mode)

    def _prepare_output(self, result: SearchResult, mode: str) -> Dict[str, Any]:
        repos = result.repositories
        
        if mode == "json":
            content = [r.to_dict() for r in repos]
        elif mode == "compact":
            content = self.optimizer.compress_results(repos, mode="compact")
        elif mode == "llm":
            content = self.optimizer.compress_results(repos, mode="llm")
        else:
            content = self.optimizer.format_as_markdown(repos, detailed=(mode == "detailed"))
            
        return {
            "query": result.query,
            "count": len(repos),
            "total_available": result.total_count,
            "content": content,
            "mode": mode
        }
