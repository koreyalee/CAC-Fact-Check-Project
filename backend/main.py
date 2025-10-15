# backend/main.py

import os
import uuid
import json # <-- Added for parsing AI responses
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import whisper
from dotenv import load_dotenv
import google.generativeai as genai
from serpapi import GoogleSearch # <-- Added for SerpApi

# --- App Initialization ---
app = FastAPI()

# --- Load Environment Variables ---
load_dotenv()

# --- Configure API Clients ---
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY") # <-- Load SerpApi key
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring API keys: {e}")

# --- Initialize the Generative Model ---
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

# --- Initialize In-Memory Cache for SerpApi ---
search_cache = {}
# -----------------------------------------------

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
    # This function remains unchanged
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
        # Check for file existence robustly
        possible_files = [f for f in os.listdir(temp_dir) if f.startswith(audio_filename_base)]
        if not possible_files: raise HTTPException(status_code=500, detail="Failed to download audio from URL.")
        audio_filepath = os.path.join(temp_dir, possible_files[0])
        print(f"Transcribing audio file: {audio_filepath}...")
        result = model.transcribe(audio_filepath, fp16=False)
        transcript = result["text"]
        print("Transcription complete.")
        return {"transcript": transcript}
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        files_to_remove = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.startswith(audio_filename_base)]
        for file_path in files_to_remove:
             if os.path.exists(file_path):
                os.remove(file_path)


# In backend/main.py, replace the entire function

@app.post("/api/fact-check")
async def fact_check_transcript(request: FactCheckRequest):
    transcript = request.transcript
    
    # --- STEP 1: Identify claims (this part is unchanged) ---
    claim_identification_prompt = f"""
    Analyze the following transcript and identify the 3 to 5 most significant, verifiable factual claims.
    Return your response as a simple JSON array of strings. Example: ["Claim one.", "Claim two."].
    Transcript: --- {transcript} ---
    """
    try:
        print("Step 1: Identifying claims with Gemini...")
        response = gemini_model.generate_content(claim_identification_prompt)
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        claims = json.loads(cleaned_text)
    except Exception as e:
        print(f"Error identifying claims: {e}")
        raise HTTPException(status_code=500, detail="Failed to identify claims from transcript.")

    # --- UPGRADE #1: Define our list of reputable sources ---
    REPUTABLE_SITES = [
        "reuters.com", "apnews.com", "bbc.com", "npr.org", "pbs.org",
        "nytimes.com", "wsj.com", "washingtonpost.com", "theguardian.com",
        "factcheck.org", "politifact.com", "snopes.com",
        "*.gov", "*.edu" # Use wildcards for any government or educational institution
    ]
    # --- End of Upgrade #1 ---

    verified_claims = []
    for claim in claims:
        # --- UPGRADE #2: Build a powerful, site-restricted search query ---
        site_query = " OR ".join([f"site:{site}" for site in REPUTABLE_SITES])
        search_query = f"{claim} {site_query}"
        # --- End of Upgrade #2 ---

        results = None
        if claim in search_cache and search_cache[claim].get("query") == search_query:
            print(f"CACHE HIT for claim: '{claim}'")
            results = search_cache[claim]["data"]
        else:
            print(f"CACHE MISS for claim: '{claim}'. Calling SerpApi with restricted search...")
            try:
                search_params = { "q": search_query, "api_key": SERPAPI_API_KEY, "engine": "google" }
                search = GoogleSearch(search_params)
                results = search.get_dict()
                # Also cache the query used, so we don't get a false hit if the sites change
                search_cache[claim] = {"query": search_query, "data": results}
            except Exception as e:
                print(f"Error calling SerpApi: {e}")
                results = {}
        
        organic_results = results.get("organic_results", [])
        top_source_url = "No reputable source found."
        source_context = "No reputable source found among trusted domains."

        if organic_results:
            top_result = organic_results[0]
            top_source_url = top_result.get("link")
            snippet = top_result.get("snippet", "")
            source_context = f"Source URL: {top_source_url}\nSource Snippet: {snippet}"
            print(f"Found reputable source: {top_source_url}")
        else:
            print("No reputable search results found for the claim.")

        # Verification step remains the same, but now uses better context
        verification_prompt = f"""
        You are a fact-checker. Determine the verdict for the claim based ONLY on the provided source context.
        Claim: "{claim}"
        Source Context: --- {source_context} ---
        Provide a verdict ("True", "False", or "Misleading") and a brief, neutral explanation (1-2 sentences).
        Format as a JSON object with keys "verdict" and "explanation".
        """
        try:
            print(f"Verifying claim with context...")
            verification_response = gemini_model.generate_content(verification_prompt)
            verification_data = json.loads(verification_response.text.strip().replace("```json", "").replace("```", "").strip())
            verified_claims.append({ "claim": claim, "verdict": verification_data.get("verdict", "Uncertain"), "explanation": verification_data.get("explanation", "Could not determine verdict from source."), "source": top_source_url })
        except Exception as e:
            print(f"Error during claim verification: {e}")
            verified_claims.append({ "claim": claim, "verdict": "Uncertain", "explanation": "Error during AI verification.", "source": top_source_url })

    # --- UPGRADE #3: A more sophisticated final analysis prompt ---
    print("Step 3: Generating final, nuanced analysis...")
    results_summary_for_ai = json.dumps(verified_claims, indent=2)
    final_analysis_prompt = f"""
    You are a discerning media analyst. Based on the following list of fact-checked claims, provide a holistic analysis of the video's reliability.

    Consider these factors:
    - **Significance:** Are the true claims minor details while the false claims are central to the video's main argument?
    - **Severity:** Is a "False" claim a simple mistake or a harmful piece of misinformation?
    - **Context:** Does the video use technically true facts to paint a misleading overall picture?

    Provide an overall accuracy score (0-100) that reflects this nuanced analysis, not just a simple average. Also, write a one-sentence summary explaining your reasoning.
    Return your response as a JSON object with keys "score" and "summary".

    Fact-Check Results:
    {results_summary_for_ai}
    """
    # --- End of Upgrade #3 ---

    final_analysis_response = gemini_model.generate_content(final_analysis_prompt)
    final_analysis = json.loads(final_analysis_response.text.strip().replace("```json", "").replace("```", "").strip())

    final_result = { "overall_analysis": final_analysis, "fact_checks": verified_claims }
    return final_result