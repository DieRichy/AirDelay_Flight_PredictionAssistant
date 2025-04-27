<img width="942" alt="Screenshot 2025-04-27 at 14 41 44" src="https://github.com/user-attachments/assets/166de73b-1d42-43e7-9632-afc5a090d520" /># ✈️ Flight Delay Prediction & LLM-Based Chatbot
This project predicts flight delay categories using historical and real-time data. It also features an interactive chatbot powered by a local LLM to support natural language flight queries. The app is built with Streamlit, integrates batch and streaming pipelines via Azure, and offers explainable model outputs.

## ❗ Prerequisite
1. Ollama needs to be installed and configured locally in advance.

    - **Reference Link**: [Ollama Installation Tutorial](https://www.cnblogs.com/obullxl/p/18295202/NTopic2024071001)

2. If you want to change the model, please change `def query_ollama_chat()` in **llm_dialogue_2.py** accordingly.
    
    [library (ollama.com)](https://ollama.com/library) is the ollama model library, please search for the model you need and launch it before running this project.

    - **Reference Link**: [Ollama GitHub](https://github.com/ollama/ollama)

## 🔍 Features Overview

### Part 1: Prediction Interface
- User inputs flight details (airline, airports, datetime, etc.)
- Model returns delay category and probability distribution in real-time

<img width="805" alt="Screenshot 2025-04-27 at 14 40 56" src="https://github.com/user-attachments/assets/604578a2-1df3-4801-8480-99714ec6d485" />

### Part 2: Exploratory Data Analysis (EDA)
- Delay category distribution
- Histograms of numerical features
- Average arrival delays per airline
- Most delayed airports
- Delay trends by time-related features

<img width="837" alt="Screenshot 2025-04-27 at 14 42 02" src="https://github.com/user-attachments/assets/d0df7e58-7041-4689-b322-6e597e7f9f04" />


### Part 3: LLM-Based Flight Chatbot
- Users can describe flights in natural language
- The system extracts structured information (slots) through LLM
- If information is incomplete, follow-up questions are generated
- The final prediction is explained to the user

<img width="942" alt="Screenshot 2025-04-27 at 14 41 44" src="https://github.com/user-attachments/assets/51c600c4-ce2c-4c31-9a8f-953d1cc9ce56" />


### 📂 Directory and Function Description




## 🚀 Getting Started

1️⃣ **Create a Virtual Environment**
```
python -m venv venv
```
* Windows
```
venv\Scripts\activate
```
* Linux/MacOS
```
source venv/bin/activate
```

2️⃣ **Install Dependencies**
```
pip install -r requirements.txt
```

3️⃣ **Launch the Web Application**
```
streamlit run app.py
```
