class RepoFinderError(Exception):
    """Base exception for github-repo-finder"""
    pass

class GitHubAPIError(RepoFinderError):
    """Raised when the GitHub API returns an error"""
    pass

class RateLimitError(GitHubAPIError):
    """Raised when GitHub API rate limit is exceeded"""
    pass

class ConfigurationError(RepoFinderError):
    """Raised when there is a configuration issue"""
    pass

class TokenLimitError(RepoFinderError):
    """Raised when token usage would exceed limits"""
    pass
