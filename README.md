# 🩺 AI Health Bot + Medical NFTs on Aptos  
**Domain:** AIML,

`AI Health Bot` is a Streamlit-powered web application that classifies diseases based on user-reported symptoms (via text or audio input) using a trained Random Forest model. It integrates **Gemini AI** for health recommendations and securely mints health metadata as NFTs on the **Aptos blockchain (testnet)**.

---

## 🚀 Features

- **🗣️ Symptom Input via Audio or Text**  
  Users can either speak or type their symptoms for a diagnosis.

- **🧠 Disease Classification**  
  Predicts possible diseases from **770 classes** using a trained `RandomForestClassifier` on 378 symptoms.

- **💡 AI-Powered Health Tips**  
  Leverages Gemini API to offer personalized treatment suggestions and lifestyle tips.

- **📦 NFT Minting**  
  Automatically generates a private health summary and mints it as a **secure NFT** on the Aptos blockchain (testnet).

- **🌐 Streamlit UI**  
  Clean and intuitive web interface with support for both audio and text input.

---

## ✅ Real-World Use Cases

### 📍 Scenario 1: **Rural Clinic with No Doctor**
> In a remote village with limited medical access, a villager says:  
> _“Body pain, fever, slight cough…”_  
> AI bot analyzes and replies:  
> _“Possible viral fever. Rest, hydration, paracetamol recommended.”_  
> A medical summary is generated and minted as an NFT, creating a tamper-proof, personal digital health record.

### 🏫 Scenario 2: **Students in Hostel**
> A college student reports symptoms at night via the web app.
> helpful for applying medical leaves.
> The AI generates a diagnosis and mints a medical NFT —  
> The summary can be shown to a doctor, or even for leave approval without sharing full medical history.

---

### 👷 Scenario 3: **NGO Health Tracking for Migrants**
> Migrant workers without documentation use the bot.  
> Health records are stored securely via **anonymous NFTs** —  
> Ensuring **privacy**, **portability**, and **ownership** of medical data.

---

## 🧬 Tech Stack

| Layer       | Tools & Libraries |
|-------------|-------------------|
| **Frontend** | Streamlit |
| **ML Model** | RandomForestClassifier (`scikit-learn`) |
| **AI Integration** | Gemini API (Google Generative AI) |
| **Speech Input** | `speech_recognition`, `gTTS` |
| **Blockchain** | Aptos Wallet + CLI / SDK |
| **Metadata** | JSON format hosted via IPFS |

---

## 📁 Project Structure



