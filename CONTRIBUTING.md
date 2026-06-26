# Contributing to GitHub Repo Finder

We welcome contributions to the GitHub Repo Finder project! By contributing, you help us make this tool more robust, efficient, and useful for everyone.

## How to Contribute

### 1. Fork the Repository

Start by forking the `Ehsas317/github-repo-finder` repository to your GitHub account.

### 2. Clone Your Fork

Clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/github-repo-finder.git
cd github-repo-finder
```

### 3. Create a New Branch

Create a new branch for your feature or bug fix. Use a descriptive name:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 4. Set Up Your Development Environment

Install the project dependencies, including development dependencies:

```bash
pip install -e .[dev]
```

### 5. Make Your Changes

Implement your feature or fix the bug. Ensure your code adheres to the project's coding standards.

### 6. Run Tests

Before submitting a pull request, make sure all tests pass and add new tests for your changes:

```bash
pytest tests/
```

### 7. Lint and Format Your Code

We use `black` for code formatting and `isort` for import sorting. Please run them before committing:

```bash
black .
isort .
```

### 8. Commit Your Changes

Commit your changes with a clear and concise commit message. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification if possible (e.g., `feat: add new feature`, `fix: resolve bug`).

```bash
git commit -m "feat: Add new filtering option"
```

### 9. Push to Your Fork

Push your changes to your forked repository on GitHub:

```bash
git push origin feature/your-feature-name
```

### 10. Create a Pull Request

Go to the original `Ehsas317/github-repo-finder` repository on GitHub and open a new pull request from your branch. Provide a detailed description of your changes.

## Code of Conduct

We expect all contributors to adhere to our Code of Conduct. Please be respectful and considerate in all your interactions.

## Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly by contacting [email protected] instead of opening a public issue.

Thank you for contributing to the GitHub Repo Finder!
