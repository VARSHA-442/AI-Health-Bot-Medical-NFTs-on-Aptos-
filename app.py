import pickle
import speech_recognition as sr
import streamlit as st
import time
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import google.generativeai as genai
import random
import json
import string
from datetime import datetime
from utils.metagenerator import upload_metadata

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCNcDqBuahNOVuu7m20r--UKshLYz9uEnk")

# Custom utility imports
from utils.encrypter import generate_encrypted_file
from utils.pinata_uploader import upload_to_pinata

# Ensure necessary NLTK data is downloaded
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define symptom list
symptom_list=['anxiety and nervousness', 'depression', 'shortness of breath', 'depressive or psychotic symptoms', 'sharp chest pain', 'dizziness', 'insomnia', 'abnormal involuntary movements', 'chest tightness', 'palpitations', 'irregular heartbeat', 'breathing fast', 'hoarse voice', 'sore throat', 'difficulty speaking', 'cough', 'nasal congestion', 'throat swelling', 'diminished hearing', 'lump in throat', 'throat feels tight', 'difficulty in swallowing', 'skin swelling', 'retention of urine', 'groin mass', 'leg pain', 'hip pain', 'suprapubic pain', 'blood in stool', 'lack of growth', 'emotional symptoms', 'elbow weakness', 'back weakness', 'pus in sputum', 'symptoms of the scrotum and testes', 'swelling of scrotum', 'pain in testicles', 'flatulence', 'pus draining from ear', 'jaundice', 'mass in scrotum', 'white discharge from eye', 'irritable infant', 'abusing alcohol', 'fainting', 'hostile behavior', 'drug abuse', 'sharp abdominal pain', 'feeling ill', 'vomiting', 'headache', 'nausea', 'diarrhea', 'vaginal itching', 'vaginal dryness', 'painful urination', 'involuntary urination', 'pain during intercourse', 'frequent urination', 'lower abdominal pain', 'vaginal discharge', 'blood in urine', 'hot flashes', 'intermenstrual bleeding', 'hand or finger pain', 'wrist pain', 'hand or finger swelling', 'arm pain', 'wrist swelling', 'arm stiffness or tightness', 'arm swelling', 'hand or finger stiffness or tightness', 'wrist stiffness or tightness', 'lip swelling', 'toothache', 'abnormal appearing skin', 'skin lesion', 'acne or pimples', 'dry lips', 'facial pain', 'mouth ulcer', 'skin growth', 'eye deviation', 'diminished vision', 'double vision', 'cross-eyed', 'symptoms of eye', 'pain in eye', 'eye moves abnormally', 'abnormal movement of eyelid', 'foreign body sensation in eye', 'irregular appearing scalp', 'swollen lymph nodes', 'back pain', 'neck pain', 'low back pain', 'pain of the anus', 'pain during pregnancy', 'pelvic pain', 'impotence', 'infant spitting up', 'vomiting blood', 'regurgitation', 'burning abdominal pain', 'restlessness', 'symptoms of infants', 'wheezing', 'peripheral edema', 'neck mass', 'ear pain', 'jaw swelling', 'mouth dryness', 'neck swelling', 'knee pain', 'foot or toe pain', 'bowlegged or knock-kneed', 'ankle pain', 'bones are painful', 'knee weakness', 'elbow pain', 'knee swelling', 'skin moles', 'knee lump or mass', 'weight gain', 'problems with movement', 'knee stiffness or tightness', 'leg swelling', 'foot or toe swelling', 'heartburn', 'smoking problems', 'muscle pain', 'infant feeding problem', 'recent weight loss', 'problems with shape or size of breast', 'underweight', 'difficulty eating', 'scanty menstrual flow', 'vaginal pain', 'vaginal redness', 'vulvar irritation', 'weakness', 'decreased heart rate', 'increased heart rate', 'bleeding or discharge from nipple', 'ringing in ear', 'plugged feeling in ear', 'itchy ear(s)', 'frontal headache', 'fluid in ear', 'neck stiffness or tightness', 'spots or clouds in vision', 'eye redness', 'lacrimation', 'itchiness of eye', 'blindness', 'eye burns or stings', 'itchy eyelid', 'feeling cold', 'decreased appetite', 'excessive appetite', 'excessive anger', 'loss of sensation', 'focal weakness', 'slurring words', 'symptoms of the face', 'disturbance of memory', 'paresthesia', 'side pain', 'fever', 'shoulder pain', 'shoulder stiffness or tightness', 'shoulder weakness', 'arm cramps or spasms', 'shoulder swelling', 'tongue lesions', 'leg cramps or spasms', 'abnormal appearing tongue', 'ache all over', 'lower body pain', 'problems during pregnancy', 'spotting or bleeding during pregnancy', 'cramps and spasms', 'upper abdominal pain', 'stomach bloating', 'changes in stool appearance', 'unusual color or odor to urine', 'kidney mass', 'swollen abdomen', 'symptoms of prostate', 'leg stiffness or tightness', 'difficulty breathing', 'rib pain', 'joint pain', 'muscle stiffness or tightness', 'pallor', 'hand or finger lump or mass', 'chills', 'groin pain', 'fatigue', 'abdominal distention', 'regurgitation.1', 'symptoms of the kidneys', 'melena', 'flushing', 'coughing up sputum', 'seizures', 'delusions or hallucinations', 'shoulder cramps or spasms', 'joint stiffness or tightness', 'pain or soreness of breast', 'excessive urination at night', 'bleeding from eye', 'rectal bleeding', 'constipation', 'temper problems', 'coryza', 'wrist weakness', 'eye strain', 'hemoptysis', 'lymphedema', 'skin on leg or foot looks infected', 'allergic reaction', 'congestion in chest', 'muscle swelling', 'pus in urine', 'abnormal size or shape of ear', 'low back weakness', 'sleepiness', 'apnea', 'abnormal breathing sounds', 'excessive growth', 'elbow cramps or spasms', 'feeling hot and cold', 'blood clots during menstrual periods', 'absence of menstruation', 'pulling at ears', 'gum pain', 'redness in ear', 'fluid retention', 'flu-like syndrome', 'sinus congestion', 'painful sinuses', 'fears and phobias', 'recent pregnancy', 'uterine contractions', 'burning chest pain', 'back cramps or spasms', 'stiffness all over', 'muscle cramps, contractures, or spasms', 'low back cramps or spasms', 'back mass or lump', 'nosebleed', 'long menstrual periods', 'heavy menstrual flow', 'unpredictable menstruation', 'painful menstruation', 'infertility', 'frequent menstruation', 'sweating', 'mass on eyelid', 'swollen eye', 'eyelid swelling', 'eyelid lesion or rash', 'unwanted hair', 'symptoms of bladder', 'irregular appearing nails', 'itching of skin', 'hurts to breath', 'nailbiting', 'skin dryness, peeling, scaliness, or roughness', 'skin on arm or hand looks infected', 'skin irritation', 'itchy scalp', 'hip swelling', 'incontinence of stool', 'foot or toe cramps or spasms', 'warts', 'bumps on penis', 'too little hair', 'foot or toe lump or mass', 'skin rash', 'mass or swelling around the anus', 'low back swelling', 'ankle swelling', 'hip lump or mass', 'drainage in throat', 'dry or flaky scalp', 'premenstrual tension or irritability', 'feeling hot', 'feet turned in', 'foot or toe stiffness or tightness', 'pelvic pressure', 'elbow swelling', 'elbow stiffness or tightness', 'early or late onset of menopause', 'mass on ear', 'bleeding from ear', 'hand or finger weakness', 'low self-esteem', 'throat irritation', 'itching of the anus', 'swollen or red tonsils', 'irregular belly button', 'swollen tongue', 'lip sore', 'vulvar sore', 'hip stiffness or tightness', 'mouth pain', 'arm weakness', 'leg lump or mass', 'disturbance of smell or taste', 'discharge in stools', 'penis pain', 'loss of sex drive', 'obsessions and compulsions', 'antisocial behavior', 'neck cramps or spasms', 'pupils unequal', 'poor circulation', 'thirst', 'sleepwalking', 'skin oiliness', 'sneezing', 'bladder mass', 'knee cramps or spasms', 'premature ejaculation', 'leg weakness', 'posture problems', 'bleeding in mouth', 'tongue bleeding', 'change in skin mole size or color', 'penis redness', 'penile discharge', 'shoulder lump or mass', 'polyuria', 'cloudy eye', 'hysterical behavior', 'arm lump or mass', 'nightmares', 'bleeding gums', 'pain in gums', 'bedwetting', 'diaper rash', 'lump or mass of breast', 'vaginal bleeding after menopause', 'infrequent menstruation', 'mass on vulva', 'jaw pain', 'itching of scrotum', 'postpartum problems of the breast', 'eyelid retracted', 'hesitancy', 'elbow lump or mass', 'muscle weakness', 'throat redness', 'joint swelling', 'tongue pain', 'redness in or around nose', 'wrinkles on skin', 'foot or toe weakness', 'hand or finger cramps or spasms', 'back stiffness or tightness', 'wrist lump or mass', 'skin pain', 'low back stiffness or tightness', 'low urine output', 'skin on head or neck looks infected', 'stuttering or stammering', 'problems with orgasm', 'nose deformity', 'lump over jaw', 'sore in nose', 'hip weakness', 'back swelling', 'ankle stiffness or tightness', 'ankle weakness', 'neck weakness']

def audio_input():
    st.subheader("🎤 Upload a .wav audio file describing your symptoms")
    uploaded_file = st.file_uploader("Choose a .wav file", type=["wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.success("✅ Transcription successful!")
                st.write("You said:", text)
                return text
            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"⚠ API Error: {e}")
    return None

def text_input():
    user_input = st.text_area("✍ Enter your symptoms here:")
    return user_input

def preprocess_text(text):
    lemmatized_tokens = [
        lemmatizer.lemmatize(w.lower(), pos='v') for w in text.split() if w not in set(stopwords.words('english'))
    ]
    return lemmatized_tokens

def create_input_vector(tokens):
    return [1 if symptom in tokens else 0 for symptom in symptom_list]

def extract_detected_symptoms(symptom_list, input_vector):
    detected = [symptom_list[i] for i in range(len(symptom_list)) if input_vector[i] == 1]
    return detected

def load_model():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def generate_medical_summary(symptoms, diagnosis, recommendation):
    # 🔹 Generate unique patient ID with timestamp + random 4-char suffix
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patient_id = f"user_{timestamp}_{suffix}"

    # 🔹 Create summary dictionary
    summary = {
        "patient_id": patient_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "symptoms": symptoms,
        "diagnosis": diagnosis,
        "recommendation": recommendation
    }

    # 🔹 Convert to JSON (for saving or printing)
    summary_json = json.dumps(summary, indent=4)

    return summary, summary_json

def generateSuggestion(userinput,prediction):
    prompt = f"""
    A user reported the following symptoms: "{userinput}".
    The AI model predicted the following condition: "{prediction}".
    
    Provide first-aid suggestions based on the predicted condition. The suggestions should be general advice that can be safely followed before seeking medical attention in 2 to 3 lines.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "No itinerary generated."

def predict_disease(model, input_vector):
    prediction = model.predict([input_vector])
    if prediction == 0:
        return "The symptoms suggest: No disease detected."
    else:
        return f"The symptoms suggest: Disease detected. (Class {prediction[0]})"


# Streamlit UI
st.title("🩺 AI Health Bot - Disease Prediction System")

mode = st.radio("Choose input mode", ("Audio", "Text"))

if mode == "Audio":
    user_input = audio_input()
elif mode == "Text":
    user_input = text_input()

if user_input:
    tokens = preprocess_text(user_input)
    input_vector = create_input_vector(tokens)

    if st.button("🔍 Predict Disease"):
        model = load_model()
        if len(input_vector) != model.n_features_in_:
            st.error(f"❌ Model expects {model.n_features_in_} features, but got {len(input_vector)}. Please check symptom list.")
        else:
            result = predict_disease(model, input_vector)
            symptoms=extract_detected_symptoms(symptom_list, input_vector)
            recommendation=generateSuggestion(symptoms,result)
            summary=generate_medical_summary(symptoms,result,recommendation)
            

            # Encrypt result
            enc_file, key_file = generate_encrypted_file(summary[1])
            st.success("🔐 Prediction encrypted successfully!")

            with open(enc_file, "rb") as f:
                st.download_button("📥 Download Encrypted Prediction", f.read(), file_name="prediction_encrypted.txt")

            with open(key_file, "rb") as kf:
                st.download_button("🔑 Download Key File", kf.read(), file_name="key.txt")

            # Upload to IPFS
            if st.button("🌐 Upload Encrypted File to IPFS"):
                ipfs_hash = upload_to_pinata(enc_file)
                if ipfs_hash:
                    st.success("✅ Uploaded to IPFS!")
                    st.markdown(f"[🔗 View on IPFS](https://gateway.pinata.cloud/ipfs/{ipfs_hash})")
                else:
                    st.error("❌ Failed to upload to IPFS.")
            PINATA_API_KEY = "9a17fbd24197fae05247"
            PINATA_SECRET_API_KEY = "dbcf4aad6f2f69a99e66aefe0bf32f6f5f64aefe5e9716d728b2b9df130eb5a3"
            metadata_url = upload_metadata("encrypt.txt",PINATA_API_KEY,PINATA_SECRET_API_KEY)
            print("✅ Metadata IPFS URL:",metadata_url)