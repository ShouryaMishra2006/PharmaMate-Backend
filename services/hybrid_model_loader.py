import os
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import spacy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'symptoms_specialists.csv')
specialist_df = pd.read_csv(csv_path)
MODEL_REPO = "shouryamishra55/Hybrid-Pharma-Model"

tokenizer = BertTokenizer.from_pretrained(MODEL_REPO)
model = BertForSequenceClassification.from_pretrained(MODEL_REPO)

spacy_model_path = os.path.join(BASE_DIR, 'spacy_ner_model')
nlp = spacy.load(spacy_model_path)
specialists = specialist_df['Specialist'].unique()
id2specialist = {i: s for i, s in enumerate(specialists)}

def predict_specialist_and_treatment(text):
    print("in prediction model")
    doc = nlp(text)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "SYMPTOM"]
    if not symptoms:
        symptoms = [text]  

    symptoms_text = ", ".join(symptoms)
    print(symptoms)

    inputs = tokenizer(symptoms_text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    with torch.no_grad():
        output = model(**inputs)
        predicted_index = output.logits.argmax(dim=1).item()

    predicted_specialist = id2specialist[predicted_index]
    print("Predicted specialist:", predicted_specialist)

    matched_specialist = None
    matched_treatment = None

    for _, row in specialist_df.iterrows():
        csv_symptoms = [s.strip().lower() for s in row["Symptoms"].split(",")]
        for symptom in symptoms:
            if symptom.lower() in csv_symptoms:
                matched_specialist = row["Specialist"]
                matched_treatment = row["Treatments"]
                break
        if matched_specialist:
            break

    if matched_specialist:
        validated_specialist = matched_specialist
        suggested_treatment = matched_treatment
    else:
        validated_specialist = predicted_specialist
        fallback_rows = specialist_df[specialist_df["Specialist"] == predicted_specialist]
        suggested_treatment = fallback_rows["Treatments"].iloc[0] if not fallback_rows.empty else "No treatment found"

    if len(validated_specialist) < 7:#to remove the unpredictable behaviour of model output
        validated_specialist = "General Physician"

    print(validated_specialist)
    print(suggested_treatment)
    return validated_specialist, suggested_treatment
