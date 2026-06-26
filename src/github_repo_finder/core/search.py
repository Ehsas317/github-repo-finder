import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .models import Repository, SearchResult
from ..utils.errors import GitHubAPIError, RateLimitError

class GitHubSearchClient:
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-repo-finder"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 30) -> SearchResult:
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page
        }
        
        response = self._make_request(url, params)
        data = response.json()
        
        repos = []
        for item in data.get("items", []):
            repos.append(self._parse_repository(item))
            
        return SearchResult(
            query=query,
            repositories=repos,
            total_count=data.get("total_count", 0)
        )

    def _make_request(self, url: str, params: Dict[str, Any], retries: int = 3) -> requests.Response:
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    return response
                
                if response.status_code == 403:
                    if "X-RateLimit-Remaining" in response.headers and response.headers["X-RateLimit-Remaining"] == "0":
                        reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                        sleep_duration = max(reset_time - time.time(), 1)
                        if attempt < retries - 1:
                            time.sleep(sleep_duration)
                            continue
                        raise RateLimitError(f"GitHub API rate limit exceeded. Resets at {datetime.fromtimestamp(reset_time)}")
                
                raise GitHubAPIError(f"GitHub API returned status {response.status_code}: {response.text}")
                
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise GitHubAPIError(f"Network error while calling GitHub API: {str(e)}")
        
        raise GitHubAPIError("Max retries exceeded for GitHub API")

    def _parse_repository(self, item: Dict[str, Any]) -> Repository:
        return Repository(
            name=item["name"],
            full_name=item["full_name"],
            description=item.get("description"),
            html_url=item["html_url"],
            stars=item["stargazers_count"],
            forks=item["forks_count"],
            open_issues=item["open_issues_count"],
            language=item.get("language"),
            updated_at=self._parse_date(item["updated_at"]),
            pushed_at=self._parse_date(item["pushed_at"]),
            created_at=self._parse_date(item["created_at"]),
            owner_login=item["owner"]["login"],
            license=item.get("license", {}).get("name") if item.get("license") else None,
            topics=item.get("topics", [])
        )

    def _parse_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
