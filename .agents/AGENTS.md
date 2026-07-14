# Admission Pilot - Agent Rules

## Implementation Plans
Whenever you generate or complete an implementation plan for a new phase of this project, you must automatically save a copy of that plan as a markdown file in the `c:\Users\chira\Desktop\Admission Pilot\Implementation Docs` directory. Do this proactively without waiting for the user to request it.

## Documentation Updates
You must proactively update the project's root `README.md` file after every significant step or phase completion to reflect the latest project state, architecture, or features. Do this without waiting for the user to ask.

## Scope & Change Discipline
- Only modify files directly relevant to the current task. Do not refactor, rename, or "clean up" unrelated code in the same pass.
- If a fix reveals a larger architectural issue, stop and propose the larger change separately rather than expanding scope silently.
- Prefer the smallest diff that correctly solves the problem.

## Testing
- Any new function, endpoint, or component must be accompanied by corresponding unit/integration tests.
- Run the existing test suite before declaring a task complete; do not mark work "done" if tests fail.
- Do not delete or weaken existing tests to make them pass — fix the underlying issue instead.
- Flag any drop in test coverage introduced by your changes.

## Security & Secrets
- Never hardcode API keys, passwords, tokens, or connection strings in source files. Use environment variables or a secrets manager, and reference `.env.example` for required keys.
- Never commit `.env` files or credentials to version control.
- Sanitize and validate all user input, especially anything touching database queries, file paths, or shell commands.
- Flag any third-party dependency with known vulnerabilities before adding it.

## Dependency Management
- Check `package.json`/`requirements.txt`/equivalent before adding a new dependency — avoid introducing a new library if an existing one already covers the need.
- Pin dependency versions explicitly rather than using open-ended ranges for anything security-sensitive.
- Justify any new dependency in the commit message or PR description.

## Error Handling & Logging
- Never swallow exceptions silently; log with enough context to debug (what operation, what input, what failed).
- User-facing error messages should be clear and actionable; internal error details (stack traces, DB errors) should not leak to end users.
- Use structured logging levels (debug/info/warn/error) consistently rather than ad-hoc print statements.

## Database & Migrations
- Any schema change must go through a migration file — never modify the database schema manually or via ad-hoc scripts.
- Migrations must be reversible where feasible; include a rollback path.
- Never run destructive migrations (drop table/column) against production-like data without explicit confirmation.

## Code Style & Readability
- Follow the linter/formatter config already present in the repo (ESLint/Prettier, Black/Ruff, etc.) rather than introducing a personal style.
- Prefer descriptive names over comments explaining what code does; use comments to explain *why*, not *what*.
- Keep functions small and single-purpose; flag files that are growing unmanageably large.

## Communication & Confirmation
- Ask for explicit confirmation before: deleting files, dropping database tables, force-pushing, rotating credentials, or making irreversible changes.
- If a requirement is ambiguous, state your assumption explicitly and proceed, rather than blocking on a question — but flag the assumption clearly so it can be corrected.
- Summarize what changed and why at the end of each significant task, not just that it's "done."

## Performance & Resource Use
- Avoid introducing N+1 queries, unbounded loops over large datasets, or unnecessary re-renders/re-computation.
- Flag any change likely to materially affect load time, memory use, or API response time.

## Accessibility & UX (if frontend work is in scope)
- Ensure interactive elements are keyboard-navigable and have appropriate ARIA labels.
- Maintain sufficient color contrast and responsive layout behavior consistent with the rest of the app.

## CI/CD
- Do not disable or skip CI checks to force a merge.
- Any change to build/deploy configuration should be called out explicitly, since it affects the whole team.