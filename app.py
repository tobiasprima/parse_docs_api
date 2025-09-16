from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import httpx
import os
import io
import docx

load_dotenv()

MAX_FILE_SIZE = 2 * 1024 * 1024
MCP_URL = os.getenv("MCP_URL")
if not MCP_URL:
    raise RuntimeError("MCP_URL environment variable is not set")

app = FastAPI()

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".docx", ".doc"]:
        raise HTTPException(status_code=400, detail="Only .docx or .doc files allowed")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 2MB)")
    
    try:
        text = extract_text_from_docx(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    async with httpx.AsyncClient() as client:
        response = await client.post(MCP_URL, json={"raw_text": text})

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="MCP failed to process resume")

    return {
        "filename": file.filename,
        "status": "submitted",
    }
