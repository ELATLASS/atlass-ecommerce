# Branch template for dev branch

## Purpose
This branch is used for development and testing. Changes are merged to `main` via PR after CI passes.

## Workflow
1. Create feature branches from `dev`
2. Push to `dev` for testing
3. Create PR `dev` → `main` for production
4. CI runs automatically on both branches

## Guidelines
- Write clear commit messages
- Keep commits focused
- Test locally before pushing
- Use conventional commit format: `feat:`, `fix:`, `docs:`, `refactor:`
