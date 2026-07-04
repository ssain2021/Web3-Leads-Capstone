# Security Notes

## Public Repo Rules

- Do not commit `.env`.
- Do not commit `.env.*` backup files.
- Do not commit `Database_Connection.csv`.
- Do not commit real API keys, passwords, private feed lists, or paid-service tokens.
- Use sample data for Kaggle judging and public demos.

## Implemented Controls

- `.gitignore` excludes `.env`, `.env.*` backup files, `Database_Connection.csv`, runtime data, caches, and logs.
- `.env.example` documents required environment variables without secrets.
- Public demo mode requires no credentials.
- `src/security.py` provides executable public-demo security checks.
- `python src/cli.py security-check` reports whether the public demo is safe to publish.
- The security check verifies required `.gitignore` patterns, sensitive file absence, obvious inline secret assignments, sample-data safety, and read-only MCP posture.
- Working core scripts now write outputs inside `Web3-Leads/data`.
- Database schema/table names are checked against a safe identifier pattern before SQL interpolation in the adapted matcher/dedupe scripts.

## Security Check Output

Expected result:

```json
{
  "safe_for_public_demo": true
}
```

The full report includes one row for each check:

- `required_gitignore_patterns`
- `sensitive_files_absent`
- `no_obvious_inline_secrets`
- `public_demo_sample_data`
- `mcp_server_read_only`

## Remaining Production Hardening

- Replace direct SQL string interpolation with `psycopg2.sql.Identifier` everywhere before production deployment.
- Add automated secret scanning in CI.
- Add rate limiting and robots/terms-of-service review for large-scale feed collection.
- Use least-privilege database credentials for any deployed mode.
