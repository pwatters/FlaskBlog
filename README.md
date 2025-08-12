# FlaskBlog

A super-simple blogging app built with Flask and SQLite.

## Features
- List posts, view a post
- Create, edit, delete posts (guarded by a simple token)
- Search by title/body
- SQLite database (file: `flaskblog.sqlite3`)

## Quickstart

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your secrets (optional but recommended):**
   ```bash
   export SECRET_KEY="replace-me"
   export ADMIN_TOKEN="replace-me"
   ```
   On Windows (PowerShell):
   ```powershell
   setx SECRET_KEY "replace-me"
   setx ADMIN_TOKEN "replace-me"
   ```
   The `ADMIN_TOKEN` is required for creating/editing/deleting posts. Provide it as a query parameter, e.g. `/create?token=YOURTOKEN`.

4. **Initialise the database (first run only):**
   ```bash
   flask --app app.py init-db
   ```

5. **Run the dev server:**
   ```bash
   flask --app app.py run --debug
   ```
   Navigate to http://127.0.0.1:5000/

## Admin actions
- Create: `/create?token=YOURTOKEN`
- Edit: `/edit/<id>?token=YOURTOKEN`
- Delete: form button on list/detail pages (token submitted as hidden field)

## Notes
- This app is intentionally minimal (no user accounts). Swap the token-guard for real auth later (e.g., Flask-Login).
- To reset the DB, stop the app and delete `flaskblog.sqlite3`, then re-run the `init-db` command.