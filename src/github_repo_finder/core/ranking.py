from datetime import datetime, timezone
from typing import List
from .models import Repository

class RankingEngine:
    def __init__(self, 
                 star_weight: float = 0.40, 
                 recency_weight: float = 0.30, 
                 fork_weight: float = 0.15, 
                 health_weight: float = 0.15):
        self.star_weight = star_weight
        self.recency_weight = recency_weight
        self.fork_weight = fork_weight
        self.health_weight = health_weight

    def rank_repositories(self, repos: List[Repository]) -> List[Repository]:
        for repo in repos:
            repo.score = self.calculate_score(repo)
        
        return sorted(repos, key=lambda x: x.score, reverse=True)

    def calculate_score(self, repo: Repository) -> float:
        star_score = self._score_stars(repo.stars)
        recency_score = self._score_recency(repo.pushed_at)
        fork_score = self._score_forks(repo.forks)
        health_score = self._score_health(repo.open_issues)
        
        repo.health_score = health_score
        repo.freshness_score = recency_score
        
        total = (
            (star_score * self.star_weight) +
            (recency_score * self.recency_weight) +
            (fork_score * self.fork_weight) +
            (health_score * self.health_weight)
        )
        return round(total, 2)

    def _score_stars(self, stars: int) -> float:
        if stars >= 1000: return 5.0
        if stars >= 500: return 4.0
        if stars >= 100: return 3.0
        if stars >= 50: return 2.0
        if stars >= 20: return 1.0
        return 0.5

    def _score_recency(self, pushed_at: datetime) -> float:
        now = datetime.now(timezone.utc)
        if pushed_at.tzinfo is None:
            pushed_at = pushed_at.replace(tzinfo=timezone.utc)
            
        days_ago = (now - pushed_at).days
        
        if days_ago <= 7: return 5.0
        if days_ago <= 30: return 4.0
        if days_ago <= 60: return 3.0
        if days_ago <= 90: return 2.0
        if days_ago <= 180: return 1.0
        return 0.5

    def _score_forks(self, forks: int) -> float:
        if forks >= 50: return 5.0
        if forks >= 20: return 4.0
        if forks >= 10: return 3.0
        if forks >= 5: return 2.0
        if forks >= 1: return 1.0
        return 0.5

    def _score_health(self, open_issues: int) -> float:
        if open_issues < 10: return 5.0
        if open_issues <= 50: return 4.0
        if open_issues <= 100: return 3.0
        if open_issues <= 500: return 2.0
        return 1.0
