import pytest
import os
import tempfile
from github_repo_finder.utils.caching import CacheManager

@pytest.fixture
def temp_cache():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    cache = CacheManager(db_path=path)
    yield cache
    if os.path.exists(path):
        os.remove(path)

def test_cache_set_get(temp_cache):
    temp_cache.set("test_key", {"data": "value"})
    assert temp_cache.get("test_key") == {"data": "value"}

def test_cache_expiration(temp_cache):
    temp_cache.ttl = -1  # Force expiration
    temp_cache.set("expired_key", "some_data")
    assert temp_cache.get("expired_key") is None

def test_cache_clear(temp_cache):
    temp_cache.set("key1", "val1")
    temp_cache.set("key2", "val2")
    temp_cache.clear()
    assert temp_cache.get("key1") is None
    assert temp_cache.get("key2") is None
