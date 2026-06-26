# Troubleshooting Guide

This guide provides solutions to common issues you might encounter while using or developing the GitHub Repo Finder.

## Common Issues and Solutions

### 1. GitHub API Rate Limit Exceeded

**Issue:** You receive a `RateLimitError` or encounter unexpected `403 Forbidden` responses from the GitHub API.

**Reason:** GitHub imposes rate limits on API requests. Unauthenticated requests have a lower rate limit (60 requests per hour) compared to authenticated requests (5000 requests per hour).

**Solution:**
- **Provide a GitHub Personal Access Token (PAT):** It is highly recommended to use a PAT for authenticated requests. You can generate one [here](https://github.com/settings/tokens) with the `public_repo` scope. Set it as an environment variable or pass it via the `--token` argument:
  ```bash
  export GITHUB_TOKEN="YOUR_GITHUB_PAT"
  github-repo-finder "python" --token $GITHUB_TOKEN
  ```
- **Wait:** If you've hit the authenticated rate limit, the error message will usually indicate when the limit resets. Wait until then.
- **Reduce Request Frequency:** If you are making many requests programmatically, consider adding delays between calls or increasing caching TTL.

### 2. `RepoFinderError: Network error while calling GitHub API`

**Issue:** The tool fails with a network-related error.

**Reason:** This usually indicates a problem with your internet connection or GitHub's servers.

**Solution:**
- **Check your internet connection.**
- **Verify GitHub status:** Check [GitHub Status](https://www.githubstatus.com/) to see if there are any ongoing issues with GitHub's services.
- **Retry:** The tool has built-in retry logic, but persistent network issues might still cause failures. Try running the command again after some time.

### 3. No Repositories Found for a Valid Query

**Issue:** You search for a topic that you expect to have results, but the tool returns an empty list or very few repositories.

**Reason:** This could be due to overly restrictive search parameters, or the repositories might not meet the minimum ranking criteria.

**Solution:**
- **Broaden your query:** Try a more general search term.
- **Adjust filters:** If you are using specific filters (e.g., `stars:>=1000`, `pushed:>=2026-01-01`), try relaxing them.
- **Check for typos:** Ensure your query is spelled correctly.
- **Verify existence:** Manually search on GitHub.com to confirm if repositories for your query exist and meet your criteria.

### 4. `ModuleNotFoundError` or `ImportError`

**Issue:** When running the CLI or importing the package, you get an error like `ModuleNotFoundError: No module named 'github_repo_finder'`.

**Reason:** The Python interpreter cannot find the installed package or its modules.

**Solution:**
- **Ensure installation:** Make sure you have installed the package correctly:
  ```bash
  pip install github-repo-finder
  # or for development
  pip install -e .
  ```
- **Check virtual environment:** If you are using a virtual environment, ensure it is activated.
- **PYTHONPATH:** If you are running scripts directly from the source directory without proper installation, ensure your `PYTHONPATH` includes the project's `src` directory:
  ```bash
  export PYTHONPATH=$PYTHONPATH:$(pwd)/src
  ```

### 5. Unexpected Output Format

**Issue:** The output is not in the expected format (e.g., you asked for Markdown but got JSON).

**Reason:** This usually happens if the `--mode` argument is misused or if there's an issue with the output formatting logic.

**Solution:**
- **Verify `--mode` argument:** Double-check that you are passing the correct `--mode` argument (e.g., `--mode markdown`, `--mode json`).
- **Check `token_opt.py`:** If you are developing, review the `formatters.py` (or `token_opt.py` where formatting is currently implemented) to ensure the logic for your desired mode is correct.

### 6. Caching Issues

**Issue:** Changes to GitHub repositories are not reflected, or the cache seems stale.

**Reason:** The caching mechanism stores results for a certain Time-To-Live (TTL).

**Solution:**
- **Disable cache:** Use the `--no-cache` flag to bypass the cache for a specific search:
  ```bash
  github-repo-finder "react" --no-cache
  ```
- **Clear cache:** Manually clear the cache database. The default path is `~/.github_repo_finder/cache.db`.
  ```bash
  rm ~/.github_repo_finder/cache.db
  ```
- **Adjust TTL:** If you are developing, you can modify the `ttl_hours` parameter in `src/github_repo_finder/utils/caching.py`.

If you encounter an issue not listed here, please refer to the `CONTRIBUTING.md` for how to report bugs or open an issue on the GitHub repository.
