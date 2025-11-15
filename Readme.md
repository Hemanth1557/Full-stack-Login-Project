# Full-Stack Login App Setup Guide

## PHASE 0 — Prerequisites (install once)

**Why:** Without these tools, VS Code and the app won't run.

### Install Python 3.10+
- **Check:** `python --version` (or `py --version` on Windows)

### Install Node.js LTS (18+ recommended)
- **Check:** `node -v` and `npm -v`

### Install VS Code

### Extensions recommended in VS Code:
- Python (Microsoft)
- Pylance (Microsoft)
- ESLint (Microsoft)
- Prettier (optional)

### Optional tools to test APIs:
- curl (comes with macOS/Linux; on Windows use Git Bash or Windows Terminal)
- Postman (optional but convenient)

## PHASE 1 — Open the project correctly in VS Code

**Why:** Opening the folder sets your working directory, relative paths, and makes terminals consistent.

1. Unzip the project to a simple path (for example: `C:\Work\fullstack-login` or `~/Work/fullstack-login`).

2. Open VS Code → File → Open Folder → select the unzipped fullstack-login folder.

3. Confirm the structure in the VS Code Explorer:
```
fullstack-login/
├─ backend/
│  └─ app/ (main.py, auth.py, models.py, database.py, config.py)
├─ frontend/
│  └─ src/ (Login.tsx, App.tsx, index.tsx, index.css)
├─ .env (we will copy this to backend shortly)
└─ README.md (optional)
```

**Mental model to remember:** you will run the backend from the backend folder and the frontend from the frontend folder, each in its own terminal.

## PHASE 2 — Create and activate a Python virtual environment (backend)

**Why:** Keeps your Python packages isolated per project. This is standard practice.

1. In VS Code, open a terminal: View → Terminal.

2. Navigate to backend:
   - **Windows:** `cd backend`
   - **macOS/Linux:** `cd backend`

3. Create a virtual environment:
   - **Windows:** `python -m venv venv` (or `py -m venv venv`)
   - **macOS/Linux:** `python3 -m venv venv`

4. Activate it:
   - **Windows PowerShell:** `.\venv\Scripts\Activate.ps1`
   - **Windows CMD:** `venv\Scripts\activate.bat`
   - **macOS/Linux:** `source venv/bin/activate`

5. Confirm you see `(venv)` prefix in the terminal prompt.

## PHASE 3 — Install backend dependencies

**Why:** FastAPI, SQLAlchemy, uvicorn, etc. are required to run the server.

Still inside backend with venv active:
```bash
pip install -r requirements.txt
```

**What this does:**
- `fastapi`: web framework
- `uvicorn`: development server
- `sqlalchemy`: database access
- `python-dotenv`: reads .env variables
- `passlib[bcrypt]`: password hashing

## PHASE 4 — Understand the backend's "contract" (API)

**Why:** Frontend talks to backend through URLs ("endpoints"). Knowing them helps you test and debug.

**Endpoints provided:**
- `POST /register?email=...&password=...`
- `POST /login?email=...&password=...`

**Simplification for first project:** parameters are sent as query strings. Later you can switch to JSON bodies with Pydantic models.

## PHASE 5 — Fix CORS to match your frontend port (important)

**Why:** Browsers block requests from different origins by default. CORS explicit allowlist is required.

1. Open `backend/app/main.py` in VS Code.

2. Find:
```python
allow_origins=["http://localhost:5173"],
```

3. Replace it with:
```python
allow_origins=["http://localhost:3000", "http://localhost:5173"],
```

This allows both Create React App (3000) and Vite (5173). It removes confusion.

4. Save the file.

## PHASE 6 — Ensure environment variables load where the backend runs

**Why:** python-dotenv loads .env from the working directory. You will run uvicorn from the backend folder, so .env must be available there.

In a terminal from the project root, copy .env into the backend folder:

- **Windows CMD:**
  ```cmd
  copy .env backend\.env
  ```

- **Windows PowerShell:**
  ```powershell
  Copy-Item .env backend\.env
  ```

- **macOS/Linux:**
  ```bash
  cp .env backend/.env
  ```

Open `backend/.env` (the copy you just made) and confirm it has:
```
DATABASE_URL=sqlite:///./users.db
SECRET_KEY=your_secret_key_here
```

**What this means:**
- SQLite file will be created in the backend working directory as `users.db` the first time you run the server.

## PHASE 7 — Start the backend server and verify it

**Why:** You want to see that the API is alive before touching the frontend.

1. In the backend terminal (venv active), run:
```bash
uvicorn app.main:app --reload
```

You should see a line with `Uvicorn running on http://127.0.0.1:8000` (or similar).

2. Open your browser and go to:
   - API root: `http://localhost:8000`
   - Interactive docs (Swagger): `http://localhost:8000/docs`

3. Create the first user (seed data) using curl or Swagger:

   **Option A — curl:**
   ```bash
   curl -X POST "http://localhost:8000/register?email=test@example.com&password=secret123"
   ```

   **Option B — Swagger UI:**
   - Go to `http://localhost:8000/docs`
   - Expand `POST /register`
   - Click "Try it out"
   - Enter email and password in the query fields
   - Execute → expect "User created successfully"

4. Check the database exists:
   - A file named `users.db` should now be present inside the backend directory.

   **Optional:** Verify the row using sqlite CLI.
   - **macOS/Linux:**
     ```bash
     sqlite3 users.db "SELECT id, email FROM users;"
     ```
   - **Windows** (with sqlite3 installed) or use "DB Browser for SQLite".

   If you see your email, the DB is connected and working.

## PHASE 8 — Install and run the frontend

**Why:** This is the login page the user will actually see and use.

1. Open a NEW terminal in VS Code (do not close the backend terminal). Keep backend running.

2. Navigate to frontend:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

4. Start the React app:
```bash
npm start
```

Your browser should open `http://localhost:3000` automatically.

**What is happening:**
- React renders `Login.tsx`.
- When you click "Login," it sends a POST request to `http://localhost:8000/login` with your email and password as query params.

## PHASE 9 — Perform an end-to-end login test

**Why:** This proves the full flow—frontend → backend → database → response.

In the React page (`http://localhost:3000`):
1. Enter the same email and password you registered (e.g., `test@example.com` / `secret123`).
2. Click "Login."

**Expected result:**
- If correct: "Login successful"
- If wrong: "Login failed"

If you see "Login successful," your full stack is working.

## PHASE 10 — What each part is doing (and why)

### Frontend (React + TS + Tailwind)
- **Login.tsx:** collects email/password and calls backend using axios.
- **Why Tailwind:** faster styling with utility classes; no CSS file hunting.
- **Why TypeScript:** catches mistakes as you type.

### Frontend service (axios call inside the component)
- **Why separate service (later):** centralize API calls and error handling.

### Backend (FastAPI)
- **main.py:** routes (/register, /login) and CORS
- **auth.py:** hashing and verification (never store plain passwords)
- **models.py:** table definition (User)
- **database.py:** DB engine/session
- **config.py:** reads environment variables

### Database (SQLite)
- **Why:** single-file DB—no server to install; perfect for learning.
- `users.db` is created automatically when the table is first used.

### Configs (.env)
- **Why:** store paths, secrets, keys outside code.
- If you hardcode them, you will leak secrets and suffer when environments change.

## TROUBLESHOOTING (read this carefully)

### CORS error in browser console:
- **Symptom:** "CORS policy" message when clicking Login.
- **Fix:** In `backend/app/main.py` ensure `allow_origins` includes `"http://localhost:3000"`. Restart uvicorn.

### 404 or 405 on /login or /register:
- Use POST, not GET.
- Check URL is `http://localhost:8000/login` (or `/register`) with query params.
- **Example:** `curl -X POST "http://localhost:8000/login?email=test@example.com&password=secret123"`

### Backend starts but .env not loading:
- Ensure `.env` is present in `backend/` (Phase 6) and you started uvicorn from inside backend (critical).
- You should see `users.db` created inside backend after registering a user.

### Frontend doesn't start or opens a different port:
- CRA default is 3000. If 3000 is busy, it may offer 3001.
- If another port is used, add it to `allow_origins` in `backend/app/main.py`.

### Password correct but still "Login failed":
- Ensure you actually ran `/register` once to insert a user.
- Typos: re-register with exact email/password, then test again.

### Module not found errors (backend):
Re-activate venv and re-install:
- **Windows PowerShell:** `.\venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source venv/bin/activate`
- Then: `pip install -r requirements.txt`

### Node not recognized (frontend):
- Re-install Node.js LTS, then open a new terminal and run `node -v`.

## A mental model you can carry for life

1. Prepare tools (Python, Node, VS Code).
2. Run backend first; verify with /docs; seed real data.
3. Run frontend; ensure CORS allows your frontend origin.
4. Click a button; watch a network request; read the API response.
5. If it fails, check console/network tab and server logs; fix the smallest broken link.

**This exact loop is how professionals build and debug full-stack systems.**