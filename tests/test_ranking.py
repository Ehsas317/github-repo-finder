import pytest
from datetime import datetime, timedelta, timezone
from github_repo_finder.core.models import Repository
from github_repo_finder.core.ranking import RankingEngine

@pytest.fixture
def ranking_engine():
    return RankingEngine()

@pytest.fixture
def sample_repo():
    now = datetime.now(timezone.utc)
    return Repository(
        name="test-repo",
        full_name="user/test-repo",
        description="A test repository",
        html_url="https://github.com/user/test-repo",
        stars=1000,
        forks=50,
        open_issues=5,
        language="Python",
        updated_at=now,
        pushed_at=now - timedelta(days=2),
        created_at=now - timedelta(days=100),
        owner_login="user"
    )

def test_score_stars(ranking_engine):
    assert ranking_engine._score_stars(2000) == 5.0
    assert ranking_engine._score_stars(750) == 4.0
    assert ranking_engine._score_stars(250) == 3.0
    assert ranking_engine._score_stars(10) == 0.5

def test_score_recency(ranking_engine):
    now = datetime.now(timezone.utc)
    assert ranking_engine._score_recency(now - timedelta(days=3)) == 5.0
    assert ranking_engine._score_recency(now - timedelta(days=45)) == 3.0
    assert ranking_engine._score_recency(now - timedelta(days=200)) == 0.5

def test_calculate_score(ranking_engine, sample_repo):
    score = ranking_engine.calculate_score(sample_repo)
    assert 0 <= score <= 5.0
    assert score > 4.0  # Should be high for a repo with 1000 stars and recent activity

def test_rank_repositories(ranking_engine, sample_repo):
    bad_repo = Repository(
        name="bad-repo",
        full_name="user/bad-repo",
        description="A bad repository",
        html_url="https://github.com/user/bad-repo",
        stars=10,
        forks=0,
        open_issues=1000,
        language="Python",
        updated_at=datetime.now(timezone.utc),
        pushed_at=datetime.now(timezone.utc) - timedelta(days=300),
        created_at=datetime.now(timezone.utc) - timedelta(days=400),
        owner_login="user"
    )
    
    ranked = ranking_engine.rank_repositories([bad_repo, sample_repo])
    assert ranked[0].full_name == "user/test-repo"
    assert ranked[1].full_name == "user/bad-repo"
