from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

app = FastAPI()

# Allow all origins (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/upload")
async def upload_text(content: str = Form(...)):
    slug = uuid.uuid4().hex[:8]
    path = os.path.join(STORAGE_DIR, f"{slug}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"url": f"/s/{slug}"}

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    slug = uuid.uuid4().hex[:8]
    extension = os.path.splitext(file.filename)[1]
    filename = f"{slug}{extension}"
    path = os.path.join(STORAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"url": f"/s/{slug}"}

@app.get("/s/{slug}")
async def serve_content(slug: str):
    # Try both .txt and common file types
    for ext in ["", ".txt", ".jpg", ".png", ".pdf"]:
        path = os.path.join(STORAGE_DIR, f"{slug}{ext}")
        if os.path.exists(path):
            # For .txt, serve plain text
            if path.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    return PlainTextResponse(f.read())
            return FileResponse(path)
    raise HTTPException(status_code=404, detail="Not found")
