from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import io, re, cv2, os, requests
import numpy as np
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from services.hybrid_model_loader import predict_specialist_and_treatment
from umls_client import UMLSClient, map_symptom_to_conditions, get_drugs_for_condition
import platform
load_dotenv()
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@tool
def analyze_symptom_tool(text: str) -> str:
    """Predicts the specialist and treatment from input text."""
    text = text.lower()
    specialist, treatment = predict_specialist_and_treatment(text)
    return f"Specialist: {specialist}, Treatment: {treatment}"

@tool
def drug_recommendation_tool(symptom: str) -> str:
    """Gets drugs based on symptom using UMLS and OpenFDA."""
    umls_api_key = os.getenv("UMLS_API_KEY")
    umls_client = UMLSClient(umls_api_key)
    conditions = map_symptom_to_conditions(symptom, umls_client)
    all_drugs = set()
    for condition in conditions:
        drugs = get_drugs_for_condition(condition)
        all_drugs.update(drugs)
    return {
    "conditions": conditions,
    "recommended_drugs": list(all_drugs)
    }
llm = OpenAI(temperature=0)
tools = [analyze_symptom_tool, drug_recommendation_tool]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

class MedicineRequest(BaseModel):
    extracted_text: str

def get_medicine_list(limit=100):
    url = f"https://api.fda.gov/drug/label.json?limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        medicines = set()
        for entry in data.get("results", []):
            if "openfda" in entry and "brand_name" in entry["openfda"]:
                medicines.update([name.lower() for name in entry["openfda"]["brand_name"]])
        return list(medicines)
    except Exception as e:
        print(f"Error fetching medicines: {e}")
        return []

def identify_medicines(extracted_text, medicine_list):
    extracted_text_lower = extracted_text.lower()
    return [med for med in medicine_list if re.search(r'\b' + re.escape(med) + r'\b', extracted_text_lower)]

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        img_np = np.array(img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        extracted_text = pytesseract.image_to_string(thresh)
        response = analyze_symptom_tool.run(extracted_text)
        specialist = ""
        treatment = ""
        if "Specialist:" in response and "Treatment:" in response:
            parts = response.split("Treatment:")
            specialist = parts[0].replace("Specialist:", "").strip()
            treatment = parts[1].strip()
        medicine_list = get_medicine_list(limit=100)
        matched_medicines = identify_medicines(extracted_text, medicine_list)
        return {"extracted_text": extracted_text, "specialist": specialist, "treatment":treatment,"matched_medicines": matched_medicines}
    except Exception as e:
        return {"error": str(e)}

@app.post("/suggest-medicines")
async def get_drugs(payload: MedicineRequest):
    return drug_recommendation_tool.run(payload.extracted_text)

@app.post("/agent-response")
async def langchain_agent_endpoint(input_text: str = Body(...)):
    try:
        result = agent.run(input_text)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}
