from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import os

app = FastAPI()

BASE_DIR = Path(os.getcwd())

@app.get("/", response_model=List[str])
def list_files():
    files = []
    for path in BASE_DIR.rglob("*"):
        if path.is_file():
            rel_path = path.relative_to(BASE_DIR)
            files.append(f"/download/{rel_path}")
    return files

@app.get("/download/{file_path:path}")
def download_file(file_path: str):
    abs_path = BASE_DIR / file_path
    if not abs_path.exists() or not abs_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(abs_path)
