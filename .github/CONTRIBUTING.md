# Contributing to Atlass Corp

## Branch Strategy
- `main` — production-ready code only
- `dev` — development branch
- Feature branches: `feature/short-description`

## Commit Convention
Use semantic commits:
```
feat: add new feature
fix: fix a bug
docs: update documentation
refactor: refactor code
test: add/update tests
chore: maintenance tasks
```

## Pull Request Process
1. Create a feature branch from `dev`
2. Make your changes
3. Run tests and linting
4. Open a PR to `dev`
5. Get at least 1 approval
6. Merge to `dev`, then `dev` → `main` via release PR
