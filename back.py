from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from detector_CNN import predict
import uuid
import shutil
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


app = FastAPI(
    title="NoMoreDeepfake API",
    description="Vue 프론트엔드에서 이미지를 업로드하여 분석하는 백엔드",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[               # 개발 단계에서는 "*" 도 가능
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://coder.ac",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    multipart/form-data 로 전송된 단일 파일을 받아 저장하고
    파일의 URL 및 메타데이터를 JSON 으로 반환.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 허용됩니다.")

    ext = Path(file.filename).suffix or ".dat"
    saved_name = f"{uuid.uuid4().hex}{ext}"
    saved_path = UPLOAD_DIR / saved_name

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print('uploads/' + saved_name)
    prediction = predict('uploads/' + saved_name, show=False)
    print("Prediction Completed")
    print(prediction)

    file_url = f"/files/{saved_name}"
    return JSONResponse(
        {
            "filename": file.filename,
            "stored_as": saved_name,
            "url": file_url,
            "content_type": file.content_type,
            "size": saved_path.stat().st_size,
            "isDeepfake": (prediction > 0.5),
            "reliability": prediction
        }
    )

@app.get("/health", tags=["Utility"])
async def health_check():
    return {"status": "ok"}
