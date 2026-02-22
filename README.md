
A personal photo memory app that identifies people in your photos using face recognition and AI. Save photos of people you know with a short note, then later point the app at any photo and it will tell you who's in it.

---

## How it works

1. **Save a memory** — run "Who is this?" on a photo, the AI identifies the person, then hit "Save" (optionally add your own note). The photo is indexed by face and stored with the AI description + your note as context.
2. **Identify someone** — tap "Who is this?", pick a photo, and the app searches your saved memories by face, then uses GPT-4.1 to narrate who it found.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI, Python, Uvicorn |
| Storage | Supabase (file storage + database) |
| AI | OpenAI GPT-4.1 (vision + structured output) |
| Face search | In-house face search service |

---

## Project structure

```
photo_talk/
├── backend/
│   ├── main.py                          # Uvicorn entry point (port 8080)
│   ├── requirements.txt
│   └── app/
│       ├── core.py                      # FastAPI app + CORS
│       ├── api/inference.py             # /upload and /search endpoints
│       ├── llm_service/                 # OpenAI GPT-4.1 client
│       ├── storage_service/             # Supabase storage + database client
│       ├── face_search_service/         # Face search API client
│       └── utils/                       # Config (env vars) + Pydantic schemas
└── frontend/
    ├── app/
    │   ├── page.tsx                     # Redirects to /login
    │   ├── login/page.tsx               # Login page
    │   └── talk/page.tsx                # Main TV UI
    └── stores/
        └── authStore.ts                 # Zustand auth store (persisted)
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- A Supabase project with:
  - Two storage buckets: `images` and `searches`
  - A table called `images` with columns: `id`, `created_at`, `user_id`, `conversation`, `photo_id`
- An OpenAI API key with access to `gpt-4.1`
- The face search service running (locally or on a server)

---

## Setup & running

### 1. Clone and set up a Python virtual environment

```bash
cd photo_talk
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
```

### 2. Configure backend environment variables

Create `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key
SUPER_BASE_PROJECT_URL=https://your-project.supabase.co
SUPER_BASE_API_KEY=your_supabase_api_key
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the backend

```bash
python main.py
```

Backend runs at `http://localhost:8080` with hot reload enabled.

### 5. Configure frontend environment variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8080
```

### 6. Install frontend dependencies

```bash
cd frontend
npm install
```

### 7. Run the frontend

```bash
npm run dev
```

Frontend runs at `http://localhost:3000` with hot module replacement enabled.

---

## Usage

1. Open `http://localhost:3000` — you'll be redirected to `/login`
2. Enter any email address (this becomes your user ID / namespace in Supabase)
3. On the main screen:
   - **Who is this?** — pick a photo to identify someone
   - **Save** — saves the current on-screen photo with the AI description + any note you typed as the memory
   - **Note field** — add extra context before saving (e.g. "Dad at Christmas 2022")

The more memories you save, the better the identification gets.

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload/{user_id}?conversation=...` | Save a photo + index the face |
| `POST` | `/search/{user_id}` | Identify who is in a photo |
