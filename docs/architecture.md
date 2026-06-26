# Architecture of GitHub Repo Finder

## Overview

The GitHub Repo Finder is designed with a modular and layered architecture to ensure scalability, maintainability, and extensibility. It aims to provide a robust solution for discovering and ranking GitHub repositories, optimized for both human and LLM consumption.

## High-Level Design

The system is composed of several key components:

1.  **Core Library (`src/github_repo_finder/core`)**: Contains the fundamental logic for interacting with the GitHub API, ranking repositories, and defining data models.
2.  **Utilities (`src/github_repo_finder/utils`)**: Provides common functionalities such as caching, token optimization, and custom error handling.
3.  **Interfaces**: Includes the Command-Line Interface (CLI) and the Model Context Protocol (MCP) server, allowing various ways to interact with the core logic.
4.  **Documentation & Examples**: Comprehensive guides and practical examples to facilitate understanding and usage.
5.  **Configuration & Schemas**: Defines system settings and data validation rules.
6.  **CI/CD Workflows**: Automates testing, linting, and deployment processes.

## Detailed Component Breakdown

### 1. Core Library

-   **`models.py`**: Defines data structures for `Repository` and `SearchResult` using Python dataclasses. Includes methods for converting repository data into various output formats (e.g., `to_dict`, `to_compact_dict`).
-   **`search.py`**: Encapsulates the logic for interacting with the GitHub REST API. It handles API requests, retries with exponential backoff, rate limit management, and parsing raw API responses into `Repository` objects.
-   **`ranking.py`**: Implements the sophisticated ranking algorithm. It calculates a composite score for each repository based on stars, recency of updates, forks, and activity health, using configurable weights.
-   **`engine.py`**: Acts as the orchestrator, integrating the search, ranking, and caching components. It provides the main `find_repositories` method, which handles the end-to-end process from query to formatted results.

### 2. Utilities

-   **`caching.py`**: Manages a persistent cache (SQLite-based) for GitHub API responses. This reduces redundant API calls, saves tokens, and improves response times. It supports Time-To-Live (TTL) based expiration.
-   **`token_opt.py`**: Focuses on optimizing token usage, especially crucial for LLM interactions. It provides methods for deduplicating repositories, compressing results into compact or LLM-friendly formats, and formatting output as Markdown.
-   **`errors.py`**: Defines custom exception classes for specific error conditions, such as `GitHubAPIError` and `RateLimitError`, allowing for more granular error handling.

### 3. Interfaces

-   **`cli.py`**: The command-line interface for the tool, built using `argparse`. It allows users to perform searches with various parameters and output modes directly from their terminal.
-   **`mcp.py`**: The Model Context Protocol server implementation. It exposes the core functionality as tools (`search_repositories`, `get_trending`) that can be invoked by LLMs, adhering to the MCP specification.

## Data Flow

1.  A user (or LLM) initiates a search query via the CLI or MCP server.
2.  The `RepoFinderEngine` first checks the cache for existing results.
3.  If not cached, the `GitHubSearchClient` queries the GitHub API.
4.  Raw API responses are parsed into `Repository` objects.
5.  The `RankingEngine` calculates scores and ranks the repositories.
6.  `TokenOptimizer` deduplicates and formats the results according to the requested output mode.
7.  Results are optionally cached for future use.
8.  The formatted results are returned to the user/LLM.

## Reliability and Token Optimization

-   **Retry Logic**: Implemented in `search.py` to handle transient network issues and API rate limits.
-   **Caching**: Central to token optimization, reducing repeated API calls.
-   **Deduplication**: Prevents redundant information, saving tokens and improving result quality.
-   **Output Modes**: `compact` and `llm` modes in `token_opt.py` are specifically designed to minimize the amount of data sent to LLMs, thereby reducing token consumption.

This architecture ensures a robust, efficient, and user-friendly GitHub repository discovery experience.
