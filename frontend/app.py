import pickle
import speech_recognition as sr
import streamlit as st
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Ensure necessary NLTK data is downloaded
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define your full symptom list here (shortened for example)
symptom_list = [
    'anxiety and nervousness', 'depression', 'shortness of breath', 'sharp chest pain',
    'dizziness', 'insomnia', 'abnormal involuntary movements', 'cough', 'sore throat',
    # ... include all symptoms ...
]

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
st.title("🩺 AI Health Bot - Disease Prediction System")

mode = st.radio("Choose input mode", ("Audio", "Text"))

if mode == "Audio":
    user_input = audio_input()
elif mode == "Text":
    user_input = text_input()

if user_input:
    tokens = preprocess_text(user_input)
    input_vector = create_input_vector(tokens)

    model = load_model()
    result = predict_disease(model, input_vector)
    st.markdown(f"### 🧠 Prediction Result: {result}")