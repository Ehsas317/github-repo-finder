# API Reference

This document provides a reference for the programmatic interfaces of the GitHub Repo Finder.

## Python Package (`github_repo_finder`)

The core functionality of the GitHub Repo Finder is exposed through its Python package. You can import and use its components directly in your Python applications.

### `RepoFinderEngine`

The `RepoFinderEngine` class is the primary entry point for searching and ranking repositories.

```python
from github_repo_finder.core.engine import RepoFinderEngine
from github_repo_finder.core.models import Repository, SearchResult

# Initialize the engine (optional: provide a GitHub token and disable cache)
engine = RepoFinderEngine(github_token="YOUR_GITHUB_TOKEN", use_cache=True)

# Find repositories
results = engine.find_repositories(
    query="python web framework", 
    limit=5, 
    output_mode="json" # or "markdown", "detailed", "compact", "llm"
)

print(results)
```

#### `RepoFinderEngine(github_token: Optional[str] = None, use_cache: bool = True)`

-   **`github_token`** (`Optional[str]`): Your GitHub Personal Access Token. Recommended for higher rate limits. If `None`, unauthenticated requests will be made.
-   **`use_cache`** (`bool`): Whether to use the internal SQLite-based cache. Defaults to `True`.

#### `find_repositories(query: str, limit: int = 10, output_mode: str = "markdown") -> Dict[str, Any]`

Searches for GitHub repositories, ranks them, and returns the results in the specified format.

-   **`query`** (`str`): The search query (e.g., "machine learning", "javascript frontend").
-   **`limit`** (`int`): The maximum number of repositories to return. Defaults to 10.
-   **`output_mode`** (`str`): The desired format for the output content. 
    -   `"markdown"`: Human-readable Markdown list.
    -   `"detailed"`: More verbose Markdown with scoring details.
    -   `"json"`: Raw JSON representation of `Repository` objects.
    -   `"compact"`: Token-optimized JSON with abbreviated keys.
    -   `"llm"`: Token-optimized JSON specifically for LLM consumption.
-   **Returns** (`Dict[str, Any]`): A dictionary containing the search query, count of returned repositories, total available repositories, the formatted content, and the output mode.

### `GitHubSearchClient`

Low-level client for direct interaction with the GitHub Search API.

```python
from github_repo_finder.core.search import GitHubSearchClient

client = GitHubSearchClient(token="YOUR_GITHUB_TOKEN")
search_result = client.search_repositories("react hooks", sort="updated", per_page=50)

for repo in search_result.repositories:
    print(f"{repo.full_name}: {repo.stars} stars")
```

#### `GitHubSearchClient(token: Optional[str] = None)`

-   **`token`** (`Optional[str]`): GitHub Personal Access Token.

#### `search_repositories(query: str, sort: str = "stars", order: str = "desc", per_page: int = 30) -> SearchResult`

Performs a raw search against the GitHub API.

-   **`query`** (`str`): The search query.
-   **`sort`** (`str`): Field to sort results by (e.g., "stars", "forks", "updated"). Defaults to "stars".
-   **`order`** (`str`): Order of results ("asc" or "desc"). Defaults to "desc".
-   **`per_page`** (`int`): Number of results per page. Defaults to 30.
-   **Returns** (`SearchResult`): An object containing the query, list of `Repository` objects, and total count.

### `RankingEngine`

Provides the logic for scoring and ranking repositories.

```python
from github_repo_finder.core.ranking import RankingEngine
from github_repo_finder.core.models import Repository
from datetime import datetime, timezone

ranker = RankingEngine()

repo = Repository(
    name="example", full_name="user/example", description="", html_url="",
    stars=1500, forks=100, open_issues=5, language="Python",
    updated_at=datetime.now(timezone.utc), pushed_at=datetime.now(timezone.utc) - timedelta(days=5),
    created_at=datetime.now(timezone.utc), owner_login="user"
)

score = ranker.calculate_score(repo)
print(f"Repository score: {score}")

# Rank a list of repositories
# ranked_repos = ranker.rank_repositories([repo1, repo2, ...])
```

#### `RankingEngine(star_weight: float = 0.40, recency_weight: float = 0.30, fork_weight: float = 0.15, health_weight: float = 0.15)`

-   **`star_weight`**, **`recency_weight`**, **`fork_weight`**, **`health_weight`** (`float`): Weights for each scoring criterion. Defaults are 0.40, 0.30, 0.15, 0.15 respectively.

#### `calculate_score(repo: Repository) -> float`

Calculates the composite score for a single `Repository` object.

-   **`repo`** (`Repository`): The repository to score.
-   **Returns** (`float`): The calculated score.

#### `rank_repositories(repos: List[Repository]) -> List[Repository]`

Calculates scores for a list of repositories and returns them sorted by score in descending order.

-   **`repos`** (`List[Repository]`): A list of `Repository` objects.
-   **Returns** (`List[Repository]`): The list of repositories, sorted by score.

### `CacheManager`

Manages the SQLite-based cache for API responses.

```python
from github_repo_finder.utils.caching import CacheManager

cache = CacheManager(db_path="/tmp/my_cache.db", ttl_hours=1)

cache.set("my_data_key", {"some": "data"})
retrieved_data = cache.get("my_data_key")
print(retrieved_data)

cache.delete("my_data_key")
cache.clear() # Clears all cache entries
```

#### `CacheManager(db_path: str = "~/.github_repo_finder/cache.db", ttl_hours: int = 24)`

-   **`db_path`** (`str`): Path to the SQLite database file. Defaults to `~/.github_repo_finder/cache.db`.
-   **`ttl_hours`** (`int`): Time-To-Live for cache entries in hours. Defaults to 24.

#### `get(key: str) -> Optional[Any]`

Retrieves a value from the cache. Returns `None` if the key is not found or has expired.

#### `set(key: str, value: Any)`

Stores a key-value pair in the cache.

#### `delete(key: str)`

Deletes a specific key from the cache.

#### `clear()`

Clears all entries from the cache.

### `TokenOptimizer`

Provides utilities for token estimation, deduplication, and result compression.

```python
from github_repo_finder.utils.token_opt import TokenOptimizer
from github_repo_finder.core.models import Repository
from datetime import datetime

# Assuming 'repos' is a list of Repository objects
# unique_repos = TokenOptimizer.deduplicate(repos)

# compressed_llm = TokenOptimizer.compress_results(repos, mode="llm")
# print(compressed_llm)

# markdown_output = TokenOptimizer.format_as_markdown(repos, detailed=False)
# print(markdown_output)
```

#### `estimate_tokens(text: str) -> int`

Provides a rough estimation of tokens for a given text string.

#### `deduplicate(repos: List[Repository]) -> List[Repository]`

Removes duplicate repositories from a list based on `full_name`.

#### `compress_results(repos: List[Repository], mode: str = "llm") -> List[Dict[str, Any]]`

Compresses a list of `Repository` objects into a token-optimized dictionary format.

-   **`mode`** (`str`): `"compact"` or `"llm"`.

#### `format_as_markdown(repos: List[Repository], detailed: bool = False) -> str`

Formats a list of `Repository` objects into a Markdown string.

-   **`detailed`** (`bool`): If `True`, includes more details in the Markdown output.

## Model Context Protocol (MCP) Server

The MCP server allows LLMs to interact with the GitHub Repo Finder. It exposes two tools:

### `search_repositories(query: str, limit: int = 10, mode: str = "llm")`

Find the best GitHub repositories for a given topic with ranking and filtering.

-   **`query`** (`str`): The topic or keywords to search for.
-   **`limit`** (`int`): Number of results (default 10).
-   **`mode`** (`str`): Output format. Can be `markdown`, `detailed`, `json`, `compact`, or `llm` (default `llm`).

### `get_trending(language: str = "", since: str = "daily")`

Get trending repositories on GitHub.

-   **`language`** (`str`): Filter by programming language.
-   **`since`** (`str`): Timeframe for trending. Can be `daily`, `weekly`, or `monthly` (default `daily`).
