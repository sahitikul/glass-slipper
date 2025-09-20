from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os

app = FastAPI(title="GlassSlipper.ai")

# Allow frontend to call backend
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Rekognition setup (make sure AWS credentials are in environment)
rekognition_client = boto3.client('rekognition', region_name='us-east-2')

# -------- Upload image & detect celebrities --------
@app.post("/upload/demo_user")
async def upload_image(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Call Amazon Rekognition
    with open(file_path, "rb") as image_file:
        try:
            response = rekognition_client.recognize_celebrities(Image={'Bytes': image_file.read()})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Extract celebrity names
    results = []
    for celeb in response.get("CelebrityFaces", []):
        results.append({"name": celeb["Name"], "confidence": celeb["Confidence"]})

    return {"file": file.filename, "celebrities": results}
