# Resume Parser — Backend README

## What this service is

A small FastAPI backend that accepts a `.docx` resume upload at `/upload-resume`, extracts plain text, parse it to JSON format and forwards them to the MCP resume-parsing service (configured via `MCP_URL` in `.env`). The backend returns a submission status (during development it also returns the parsed result for debugging).

---

# Prerequisites

* Python 3.11+ (the project uses 3.11 in CI/Dockerfile examples)
* `pip` available (or `conda` if you prefer)
* A running MCP server that exposes the resume parsing REST endpoint (see **MCP\_URL** below)
* A `.docx` file containing a resume (one test file named `resume.docx` recommended)

---

# Quick setup (venv)

```bash
# create and activate a venv
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

# Quick setup (conda)

```bash
conda create -n resume-parser-api python=3.11 -y
conda activate resume-parser-api
```

---

# Install Python dependencies

From the project root (where `requirements.txt` lives):

```bash
pip install -r requirements.txt
```

---

# Environment variables

Create a `.env` file in the project root (same directory as `app.py`) with at least this:

```env
# URL of the MCP REST wrapper that accepts resume text
MCP_URL=http://127.0.0.1:9000/parse_resume
```

---

# Run the backend

Start the FastAPI backend (development):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

* The backend exposes `/upload-resume` for file uploads.
* Check logs in the console. If MCP is reachable and responds, you will see successful MCP calls logged.

---

# Test uploading a resume (curl)

Place a sample `resume.docx` in your project root, then run:

```bash
curl -X POST "http://localhost:8000/upload-resume" \
  -F "file=@resume.docx;type=application/vnd.openxmlformats-officedocument.wordprocessingml.document"
```

Expected: HTTP 200 with JSON `{"filename": "resume.docx", "status": "submitted", }`. If MCP is unavailable, you'll get a `502 Bad Gateway` with an error message.

---

# Minimal programmatic way to create a `.docx` resume for testing

If you need to create a `resume.docx` quickly with Python, use `python-docx`:

```python
from docx import Document

d = Document()
d.add_heading('John Doe', level=1)
d.add_paragraph('( +02 ) 215-442-221 | johndoe123123@gmail.com | Kuwait')
d.add_heading('SUMMARY OF QUALIFICATIONS', level=2)
d.add_paragraph('Passionate junior software engineer skilled in backend and cloud development...')
# add other sections similarly

d.save('resume.docx')
```

(This is useful when you want to generate many test resumes programmatically.)

---