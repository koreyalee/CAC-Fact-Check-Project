# backend/main.py

import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import whisper
from dotenv import load_dotenv
import google.generativeai as genai

# --- App Initialization ---
app = FastAPI()

# --- Load Environment Variables ---
load_dotenv()

# --- Configure API Clients ---
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# --- Initialize the Generative Model ---
gemini_model = genai.GenerativeModel('gemini-2.5-pro')
# -----------------------------

# --- CORS Middleware ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------

# --- Load Whisper Model ---
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded.")
# -------------------------

# --- Pydantic Models ---
class VideoRequest(BaseModel):
    video_url: str

class FactCheckRequest(BaseModel):
    transcript: str
# -------------------------

# --- API Routes ---

@app.get("/")
def read_root():
    return {"message": "Hello from the FastAPI backend!"}


@app.post("/api/transcribe")
async def transcribe_video(request: VideoRequest):
    # This function remains unchanged from the last working version
    video_url = request.video_url
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    audio_filename_base = f"{uuid.uuid4()}"
    audio_filepath = os.path.join(temp_dir, f"{audio_filename_base}.m4a")
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': os.path.join(temp_dir, f"{audio_filename_base}.%(ext)s"), 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a',}],}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from {video_url}...")
            ydl.download([video_url])
            print("Download complete.")
        if not os.path.exists(audio_filepath):
            possible_files = [f for f in os.listdir(temp_dir) if f.startswith(audio_filename_base)]
            if not possible_files: raise HTTPException(status_code=500, detail="Failed to download audio from URL.")
            audio_filepath = os.path.join(temp_dir, possible_files[0])
        print(f"Transcribing audio file: {audio_filepath}...")
        result = model.transcribe(audio_filepath, fp16=False)
        transcript = result["text"]
        print("Transcription complete.")
        return {"transcript": transcript}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        files_to_remove = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.startswith(audio_filename_base)]
        for file_path in files_to_remove:
             if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up audio file: {file_path}")


@app.post("/api/fact-check")
async def fact_check_transcript(request: FactCheckRequest):
    transcript = request.transcript
    
    # NEW, MORE ROBUST PROMPT
    prompt = f"""

    Follow these instructions with extreme care:
    1.  Read the entire transcript provided below.
    2.  Determine an overall accuracy score (0-100) and write a one-sentence summary.
    3.  Identify the 3 to 5 most significant, verifiable factual claims.
    4.  For each claim, provide a verdict ("True", "False", or "Misleading") and a brief explanation.
    5.  For each claim, you MUST provide a real, working, high-quality URL as a source.
    
    *** SOURCE CRITERIA (VERY IMPORTANT) ***
    - The URL must be from a highly reputable domain (e.g., major news outlets like Reuters/AP, government sites, university studies, scientific journals).
    - The URL must lead directly to a page that SUPPORTS your verdict.
    - DO NOT invent or guess URLs. A fake URL is worse than no URL.
    - **If, and only if, you cannot find a real, verifiable URL that meets these criteria, you MUST return the string "No verifiable source found." in the "source" field.**

    6.  Format your entire response as a single, valid JSON object. Do not include any text or markdown formatting before or after the JSON object.

    Here is the required JSON format:
    {{
      "overall_analysis": {{
        "score": <number between 0 and 100>,
        "summary": "Your one-sentence summary here."
      }},
      "fact_checks": [
        {{
          "claim": "The specific claim being checked.",
          "verdict": "True | False | Misleading",
          "explanation": "A concise explanation of the verdict.",
          "source": "https://www.real-source.com/article" OR "No verifiable source found."
        }}
      ]
    }}

    Now, analyze this transcript:

    ---
    {transcript}
    ---
    """
    try:
        print("Sending transcript to Gemini for full analysis...")
        response = gemini_model.generate_content(prompt)
        
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        print("Received full analysis from Gemini.")
        return {"analysis_result": cleaned_response_text}

    except Exception as e:
        print(f"An error occurred while calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get a response from the AI model. Error: {str(e)}")