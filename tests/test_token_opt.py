import pytest
from datetime import datetime
from github_repo_finder.core.models import Repository
from github_repo_finder.utils.token_opt import TokenOptimizer

@pytest.fixture
def sample_repos():
    now = datetime.now()
    r1 = Repository(
        name="repo1", full_name="user/repo1", description="desc1",
        html_url="url1", stars=100, forks=10, open_issues=1,
        language="Python", updated_at=now, pushed_at=now, created_at=now,
        owner_login="user"
    )
    r2 = Repository(
        name="repo1", full_name="user/repo1", description="desc1",
        html_url="url1", stars=100, forks=10, open_issues=1,
        language="Python", updated_at=now, pushed_at=now, created_at=now,
        owner_login="user"
    )
    return [r1, r2]

def test_deduplicate(sample_repos):
    unique = TokenOptimizer.deduplicate(sample_repos)
    assert len(unique) == 1

def test_compress_results_compact(sample_repos):
    compressed = TokenOptimizer.compress_results(sample_repos[:1], mode="compact")
    assert "n" in compressed[0]
    assert "s" in compressed[0]
    assert "full_name" not in compressed[0]

def test_format_as_markdown(sample_repos):
    md = TokenOptimizer.format_as_markdown(sample_repos[:1])
    assert "user/repo1" in md
    assert "100★" in md
