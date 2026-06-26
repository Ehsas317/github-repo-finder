from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class Repository:
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stars: int
    forks: int
    open_issues: int
    language: Optional[str]
    updated_at: datetime
    pushed_at: datetime
    created_at: datetime
    owner_login: str
    license: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    score: float = 0.0
    maintenance_score: float = 0.0
    freshness_score: float = 0.0
    health_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description,
            "html_url": self.html_url,
            "stars": self.stars,
            "forks": self.forks,
            "open_issues": self.open_issues,
            "language": self.language,
            "updated_at": self.updated_at.isoformat(),
            "pushed_at": self.pushed_at.isoformat(),
            "score": self.score,
            "license": self.license,
            "topics": self.topics
        }

    def to_compact_dict(self) -> Dict[str, Any]:
        return {
            "n": self.full_name,
            "d": self.description[:100] + "..." if self.description and len(self.description) > 100 else self.description,
            "u": self.html_url,
            "s": self.stars,
            "l": self.language,
            "up": self.pushed_at.strftime("%Y-%m-%d")
        }

@dataclass
class SearchResult:
    query: str
    repositories: List[Repository]
    total_count: int
    timestamp: datetime = field(default_factory=datetime.now)
