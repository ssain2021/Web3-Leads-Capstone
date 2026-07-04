# Deployability

This project uses a reproducible local deployment path for Kaggle review.

The public demo does not require:

- API keys.
- PostgreSQL.
- Private RSS feeds.
- Paid services.

## Public Demo Deployment

From the `Web3-Leads` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
python src/cli.py build-static-demo
```

Generated artifacts:

- `data/output/demo_opportunities.csv`
- `data/output/demo_report.md`
- `data/output/demo_report.html`

Open the HTML report in a browser:

```powershell
start data\output\demo_report.html
```

## Verification

Run automated checks:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Run the public security check:

```powershell
python src/cli.py security-check
```

Expected public-release result:

```json
{
  "safe_for_public_demo": true
}
```

If local private files such as `.env`, `.env.*` backup files, or `Database_Connection.csv` are present, the security check should return `false`. That is expected during private development and should be fixed before publishing.

## Private Full Pipeline Mode

Private full runs can use:

- `.env` for provider API keys.
- `Database_Connection.csv` for PostgreSQL inserts.
- Full RSS source collection.

These files must remain local and must not be committed or uploaded to Kaggle/GitHub.

## Public Release Checklist

- Remove `.env` from the published repo.
- Remove `.env.*` backup files from the published repo.
- Remove `Database_Connection.csv` from the published repo.
- Run `python src/cli.py build-static-demo`.
- Run `python -m unittest discover -s tests -p "test_*.py"`.
- Run `python src/cli.py security-check` in a clean public copy.
- Confirm `data/output/demo_report.html` opens locally.
