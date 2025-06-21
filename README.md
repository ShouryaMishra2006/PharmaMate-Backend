# Pharm-ate
Your AI-powered pharmacy and diagnostic companion.
# Problem Statement
Pharmacies and healthcare systems often face inefficiencies in prescription management, medicine recommendations, and specialist referrals, leading to delays and errors in patient care. Additionally, children, elderly, and illiterate patients struggle to find the right specialist, while doctor unavailability can cause further delays.

PharmAssist AI aims to solve these challenges by:

--> Automatically matching handwritten prescriptions to medicines.

--> Recommending specialists based on symptoms and patient history.

--> Providing safe medicine recommendations for minor illnesses.

--> Ensuring accessibility for illiterate, elderly, and disabled patients.

--> Handling doctor unavailability by suggesting online consultations.

--> Offering AI-powered drug safety checks and dosage reminders.

--> Tracking patient history for personalized recommendations and safety (from allergies, past prescriptions ).

# Key Features & Approach

✅ Prescription Matching & Order Creation –

Uses OCR & NLP to extract handwritten prescriptions and generate medicine orders.

✅ Specialist Recommendation –

AI-based symptom analysis to suggest the right doctor, with voice input for accessibility.

✅ Doctor Availability & Telemedicine –

Checks real-time doctor availability and suggests online consultations if unavailable.

✅ AI-Driven Medicine Suggestions –

Provides OTC medicine recommendations, checks drug interactions, and sets dosage reminders.

✅ History Tracking & Personalized Care – 

Stores patient history for smart recommendations and alerts for medication conflicts.

✅ Smart UI & Multilingual Support – 

Supports voice-based interactions, image input, and multiple languages for easy access.


# Tech Stack

🔹 Frontend: React.js 

🔹 Backend: FastAPI (Python), Node.js (Express.js)

🔹 Database: MongoDB

🔹 AI/ML Models: TensorFlow/Keras (OCR & NLP), BERT (Symptom Analysis)

🔹 Cloud & APIs: Google Cloud (Speech-to-Text, Translation), OpenFDA (Drug Safety), Telemedicine APIs


# Environment Setup

Before running the project, ensure you have the necessary dependencies installed. Follow these steps:

🔹 Prerequisites

Install Node.js (for frontend & backend) → https://nodejs.org/en

Install Python (for FastAPI backend & AI models) → https://www.python.org/downloads/

Install MongoDB (for database) → https://www.mongodb.com/try/download/community

Set up a Google Cloud API Key (for Speech-to-Text & Translation) →  

Go to Google Cloud Console.

Click on Select a project → New Project.

Enter the Project Name (e.g., PharmaMate) and Create.

Go to APIs & Services > Library, and enable the following APIs:

Cloud Vision API (for OCR on handwritten prescriptions)

Cloud Natural Language API (for symptom and prescription text analysis)

Cloud Speech-to-Text API (for voice assistant features)

Cloud Translation API (for multilingual support)

Click Enable for each API.

Go to APIs & Services > Credentials.

Click + Create Credentials → API Key.

Copy the generated key and store it safely.

Now, Create the OpenFDA Key from this -> https://open.fda.gov/apis/

# Clone the Repository

git clone https://github.com/ShouryaMishra2006/PharmaMate.git

cd PharmaMate

# Python Backend (FastAPI) Setup

cd backend-python

python -m venv env


source env/bin/activate   # (Windows: env\Scripts\activate)

pip install -r requirements.txt

uvicorn main:app --reload

Runs the FastAPI server for OCR & NLP processing.

API runs on http://127.0.0.1:8000

# Node.js Backend (Express.js) Setup

cd backend-node

npm install

node server.js

Runs the Express.js server for authentication & prescription management.

API runs on http://localhost:5000


# Frontend (React.js) Setup

cd frontend

npm install

npm run dev 

Starts the React.js frontend.

Accessible at http://localhost:3000

# Database Setup (MongoDB)

Start the MongoDB service:

mongod --dbpath /your/data/path

Create .env file inside backend-node and backend-python with:

MONGO_URI=mongodb://localhost:27017/pharmamate

GOOGLE_API_KEY=your_google_cloud_key

OPENFDA_API_KEY=your_openfda_key

# Running the AI Model

Install dependencies inside backend-python:

pip install tensorflow keras transformers

Run BERT-based symptom analysis & OCR model:

python ai_model.py

# Usage Instructions

--> Login/Register to access personalized recommendations.

--> Upload a handwritten prescription for automatic medicine matching.

--> Input symptoms to get specialist recommendations.

--> Track medical history & receive medicine reminders.

# API Documentation

FastAPI:

https://fastapi.tiangolo.com/tutorial/

Explore Node.js API routes in backend-node/routes.
