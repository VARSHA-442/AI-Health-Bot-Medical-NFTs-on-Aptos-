import pickle
import speech_recognition as sr
import time
import streamlit as st
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

# Ensure necessary NLTK data is downloaded
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define symptom list (shortened for brevity, include all symptoms)
symptom_list = [
    'anxiety and nervousness', 'depression', 'shortness of breath', 'depressive or psychotic symptoms', 
    'sharp chest pain', 'dizziness', 'insomnia', 'abnormal involuntary movements', 'chest tightness', 
    'palpitations', 'irregular heartbeat', 'breathing fast', 'hoarse voice', 'sore throat', 'difficulty speaking', 
    'cough', 'nasal congestion', 'throat swelling', 'diminished hearing', 'lump in throat', 'throat feels tight', 
    'difficulty in swallowing', 'skin swelling', 'retention of urine', 'groin mass', 'leg pain', 'hip pain', 
    'suprapubic pain', 'blood in stool', 'lack of growth', 'emotional symptoms', 'elbow weakness', 'back weakness', 
    'pus in sputum', 'symptoms of the scrotum and testes', 'swelling of scrotum', 'pain in testicles', 'flatulence', 
    'pus draining from ear', 'jaundice', 'mass in scrotum', 'white discharge from eye', 'irritable infant', 'abusing alcohol',
    # (Include all the other symptoms you listed...)
]

def audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now... (3-second pause max, 15 sec total)")
        r.adjust_for_ambient_noise(source)
        audio_data = []
        end_time = time.time() + 15
        last_audio_time = time.time()

        while time.time() < end_time:
            try:
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
                audio_data.append(audio)
                last_audio_time = time.time()
            except sr.WaitTimeoutError:
                if time.time() - last_audio_time > 2:
                    st.write("Paused too long. Stopping.")
                    break
                else:
                    continue

        if audio_data:
            combined_audio = sr.AudioData(
                b''.join([a.get_raw_data() for a in audio_data]),
                audio_data[0].sample_rate,
                audio_data[0].sample_width
            )

            try:
                text = r.recognize_google(combined_audio)
                st.write("You said:", text)
                return text
            except sr.UnknownValueError:
                st.write("Sorry, could not understand the audio.")
            except sr.RequestError as e:
                st.write("API Error:", e)
    return None

def text_input():
    user_input = st.text_area("Enter your symptoms here:")
    if user_input:
        st.write("You typed:", user_input)
    return user_input

def preprocess_text(text):
    lemmatized_tokens = [
        lemmatizer.lemmatize(w.lower(), pos='v') for w in text.split() if w not in set(stopwords.words('english'))
    ]
    return lemmatized_tokens

def create_input_vector(tokens):
    return [1 if symptom in tokens else 0 for symptom in symptom_list]

def load_model():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_disease(model, input_vector):
    prediction = model.predict([input_vector])
    if prediction == 0:
        return "The symptoms suggest: No disease detected."
    else:
        return f"The symptoms suggest: Disease detected. (Class {prediction[0]})"

# Streamlit app layout
st.title("Disease Prediction System")

mode = st.radio("Choose input mode", ("Audio", "Text"))

if mode == "Audio":
    user_input = audio_input()
elif mode == "Text":
    user_input = text_input()

if user_input:
    tokens = preprocess_text(user_input)
    input_vector = create_input_vector(tokens)

    # Load the pre-trained model
    model = load_model()

    # Get prediction
    result = predict_disease(model, input_vector)
    st.write("\nFinal result:", result)
