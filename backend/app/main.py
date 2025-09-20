from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv
import openai

#  Load environment variables 
load_dotenv()  # Loads variables from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API key not found. Set OPENAI_API_KEY in .env or environment variables.")

openai.api_key = OPENAI_API_KEY

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

# -------- Helper function: generate makeup recommendations --------
def get_makeup_recommendations(traits):
    prompt = f"""
    Given the following facial traits of a celebrity:
    Gender: {traits['Gender']}
    Age range: {traits['AgeRange']['Low']}-{traits['AgeRange']['High']}
    Emotions: {', '.join(traits['Emotions'])}
    Smile: {traits['Smile']}
    Eyeglasses: {traits['Eyeglasses']}
    Sunglasses: {traits['Sunglasses']}
    Beard: {traits['Beard']}
    Mustache: {traits['Mustache']}

    Suggest a list of makeup products (type, brand, shade) suitable for these traits.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

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
        image_bytes = image_file.read()
        try:
            # Detect Celebrities
            celeb_response = rekognition_client.recognize_celebrities(Image={'Bytes': image_file})

            # Detect Facial Traits
            traits_response = rekognition_client.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])
            
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Extract celebrity names and traits
    results = []

    # Process each detected face
    for face in traits_response.get("FaceDetails", []):
        traits_info = {
            "Gender": face['Gender']['Value'],
            "AgeRange": face['AgeRange'],
            "Emotions": [e['Type'] for e in face['Emotions'] if e['Confidence'] > 50],
            "Smile": face['Smile']['Value'],
            "Eyeglasses": face['Eyeglasses']['Value'],
            "Sunglasses": face['Sunglasses']['Value'],
            "Beard": face['Beard']['Value'],
            "Mustache": face['Mustache']['Value'],
            "EyesOpen": face['EyesOpen']['Value'],
            "MouthOpen": face['MouthOpen']['Value'],
            "Pose": face['Pose']
        }
        results.append(traits_info)

    # Generate AI-based makeup recommendations
        traits_info['makeup_recommendations'] = get_makeup_recommendations(traits_info)

        results.append(traits_info)

    return {"file": file.filename, "faces": results}