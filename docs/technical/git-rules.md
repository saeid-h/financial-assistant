# Git Rules and Commit Conventions

**Project**: Financial Assistant  
**Created**: 2025-10-19  
**Status**: Active

## Purpose

This document defines the git workflow, branch strategy, and commit conventions for the Financial Assistant project to ensure clear history, traceability, and collaboration.

## Branch Strategy

### Main Branches

- **main**: Production-ready code, always stable
- **develop**: Integration branch for features (optional for single-developer project)

### Feature Branches

- Create feature branches from main: `feature/<pbi-id>-<short-description>`
- Example: `feature/1-project-setup`, `feature/4-categorization`

### Task Branches (Optional)

For complex PBIs with multiple tasks:
- `task/<task-id>-<short-description>`
- Example: `task/1-1-database-schema`

## Commit Message Format

### Standard Format

```
<task-id> <brief description>

<optional detailed description>

<optional footer>
```

### Examples

**Task Completion:**
```
1-3 Setup Flask application with routing

- Created app.py with application factory
- Added home route and template
- Configured static file serving
```

**Bug Fix:**
```
4-2 Fix categorization rule matching logic

Pattern matching was case-sensitive, causing missed matches.
Updated to use case-insensitive comparison.
```

**Documentation:**
```
docs Update README with installation instructions

Added step-by-step setup guide for new developers.
```

### Commit Type Prefixes (Optional)

For non-task commits:
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `fix:` - Bug fixes not tied to tasks
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

## Commit Guidelines

### Do's

1. **Reference Task IDs**: Always include task ID in task-related commits
2. **Atomic Commits**: Each commit should represent one logical change
3. **Clear Messages**: Write descriptive commit messages explaining "what" and "why"
4. **Present Tense**: Use present tense ("Add feature" not "Added feature")
5. **Test Before Commit**: Ensure code compiles and tests pass
6. **Sync Regularly**: Pull from remote before starting work

### Don'ts

1. **No Huge Commits**: Avoid commits with dozens of file changes
2. **No Generic Messages**: Avoid "fixes", "updates", "changes"
3. **No Broken Code**: Never commit code that doesn't run
4. **No Secrets**: Never commit passwords, API keys, or sensitive data
5. **No Generated Files**: Don't commit files that can be generated (see .gitignore)

## Workflow

### Standard Workflow

```bash
# 1. Start new feature
git checkout main
git pull origin main
git checkout -b feature/2-csv-import

# 2. Make changes and commit
git add <files>
git commit -m "2-1 Implement CSV parser with pandas"

# 3. Push to remote
git push origin feature/2-csv-import

# 4. When feature complete, merge to main
git checkout main
git merge feature/2-csv-import
git push origin main

# 5. Delete feature branch
git branch -d feature/2-csv-import
git push origin --delete feature/2-csv-import
```

### Quick Add-Commit-Push (git acp)

For rapid development, create an alias:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias git-acp='git add -A && git commit -m "$1" && git push'

# Usage
git-acp "1-2 Add database initialization script"
```

## Pull Request Guidelines (If Using PR Workflow)

### PR Title Format
```
[<task-id>] <Task Description>
```

Example: `[1-3] Setup Flask application with routing`

### PR Description Template

```markdown
## Task
Link to task: docs/delivery/<pbi-id>/<task-id>.md

## Changes
- Brief bullet list of changes

## Testing
- How was this tested?
- Any manual testing steps?

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No linter errors
```

## Protected Branches

- **main**: Requires passing tests (configure when setting up CI/CD)
- Direct commits to main allowed for single-developer project
- Consider branch protection when adding collaborators

## Merge Strategy

- **Prefer**: Merge commits (preserves history)
- **Alternative**: Squash and merge for cleaning up messy feature branches
- **Avoid**: Rebase on shared branches

## Tags and Releases

### Version Tags

When completing phases or major milestones:

```bash
git tag -a v1.0.0 -m "Phase 1 MVP - Core functionality complete"
git push origin v1.0.0
```

### Tag Format

- `v<major>.<minor>.<patch>` following Semantic Versioning
- Examples:
  - `v1.0.0` - Phase 1 MVP complete
  - `v1.1.0` - Phase 2 enhanced features
  - `v1.1.1` - Bug fix release

## Special Files

### Always Commit

- Source code (.py files)
- Tests
- Documentation (.md files)
- Configuration templates
- requirements.txt
- .gitignore

### Never Commit (See .gitignore)

- Virtual environment (venv/, .venv/)
- Database files (*.db, *.sqlite)
- IDE files (.vscode/, .idea/)
- Logs (*.log)
- Cache (__pycache__/, *.pyc)
- Sensitive data (.env, secrets.yaml)
- User data (data/ directory with actual statements)

## Commit Frequency

- **Minimum**: At least one commit per task completion
- **Recommended**: Multiple commits per task showing logical progression
- **Maximum**: No hard limit, but keep commits atomic

## Reverting Changes

### Undo Last Commit (Not Pushed)
```bash
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
```

### Revert Pushed Commit
```bash
git revert <commit-hash>
git push origin main
```

## Best Practices

1. **Commit Often**: Small, frequent commits are better than large, infrequent ones
2. **Review Before Commit**: Use `git diff` to review changes
3. **Write for Others**: Assume someone else will read your commit history
4. **Link to Tasks**: Always reference task IDs for traceability
5. **Keep History Clean**: Use meaningful commit messages
6. **Backup Remote**: Push to remote repository regularly

## Git Commands Quick Reference

```bash
# Status and info
git status                    # Check working directory status
git log --oneline            # View commit history
git diff                     # See unstaged changes

# Basic workflow
git add <file>               # Stage specific file
git add -A                   # Stage all changes
git commit -m "message"      # Commit with message
git push                     # Push to remote

# Branching
git branch                   # List branches
git checkout -b <branch>     # Create and switch to branch
git merge <branch>           # Merge branch into current

# Remote
git remote -v                # View remotes
git pull origin main         # Pull from remote
git push origin <branch>     # Push to remote branch

# Undoing
git reset HEAD <file>        # Unstage file
git checkout -- <file>       # Discard changes to file
git revert <commit>          # Revert commit
```

## Questions and Updates

If you have questions about these git rules or suggestions for improvements, discuss with the project owner (Saeed).

---

**Note**: These rules prioritize clarity and traceability. Follow them consistently for maintainable project history.

