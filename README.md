# 🧓🏼🤖 AI for Elderly Care and Support – Complete Project Documentation

---

## 📘 Table of Contents

1. [Introduction](#introduction)  
2. [Objectives](#objectives)  
3. [Tools and Technologies Used](#tools-and-technologies-used)  
4. [Dataset Collection](#dataset-collection)  
5. [Data Preprocessing](#data-preprocessing)  
6. [Machine Learning Model Building](#ml-model-building)  
7. [Model Evaluation](#model-evaluation)  
8. [Multi-Agent System](#multi-agent-system)  
9. [API Development](#api-development)  
10. [Streamlit Web App Interface](#streamlit-interface)  
11. [System Flow Overview](#system-flow-overview)  
12. [Prediction Examples](#prediction-examples)  
13. [Challenges and Learnings](#challenges-and-learnings)  
14. [Conclusion](#conclusion)

---

## 🧠 Introduction

As the elderly population increases, there is a growing need for technology to support their health, safety, and daily routines. We developed an AI-powered **multi-agent system** that can monitor **vital signs**, detect **safety issues**, and manage **daily reminders** using machine learning and automation tools.

---

## 🎯 Objectives

- To build a multi-agent system that assists elderly people in:
  - **Monitoring health vitals**
  - **Detecting safety risks**
  - **Reminding about daily tasks**
- To provide an interactive web interface using **Streamlit**
- To enable real-time **predictions and alerts** using **trained ML models**

---

## 🧰 Tools and Technologies Used

| Category            | Tool / Library                      |
|---------------------|--------------------------------------|
| Programming Language| Python                               |
| Data Handling       | Pandas, NumPy                        |
| Visualization       | Matplotlib, Plotly                   |
| Machine Learning    | Scikit-learn                         |
| Model Persistence   | Pickle (.pkl)                      |
| API Layer           | Flask                                |
| Web App             | Streamlit                            |
| Frontend Requests   | Requests (Python)                    |
| Agent Architecture  | Custom Python Classes                |


---

## 📁 Project Folder Structure

ElderlyCare-AI-System/
│
├── Dataset/
│   ├── health_dataset.csv
│   ├── safety_dataset.csv
│   └── reminder_dataset.csv
│
├── cleaned_data/
│   ├── health_cleaned.csv
│   ├── safety_cleaned.csv
│   └── reminder_cleaned.csv
│
├── models/
│   ├── health_model.pkl
│   ├── safety_model.pkl
│   └── reminder_model.pkl
│
├── agents.py              ← Logic for Health, Safety, and Reminder Agents
├── app.py                 ← Streamlit frontend
├── combined_api.py        ← Flask backend for API endpoints
├── utils.py               ← Helper functions for prediction
├── requirements.txt       ← Python dependencies
├── README.md              ← Project overview and instructions
└── image.png              ← Architecture or system overview image


---

## 📂 Dataset Collection

We created **three synthetic datasets** based on realistic scenarios of elderly care:

1. **Health Monitoring** – Includes heart rate, blood pressure, temperature, and alert class.  
2. **Safety Monitoring** – Includes events like fall, call for help, room location, and alert status.  
3. **Daily Reminders** – Includes task, time slots, reminder sent, and whether it was acknowledged.

These were stored in the Dataset/ folder.

---

## 🧹 Data Preprocessing

Each dataset was cleaned and stored in cleaned_data/:

### Health Monitoring
- Handled nulls and outliers in vitals
- Encoded categorical variables
- Normalized vitals (min-max scaling)

### Safety Monitoring
- Encoded safety event types
- Checked time-based patterns
- Binary label encoding

### Daily Reminders
- Time converted into numerical categories
- Handled acknowledgment delays
- Encoded binary outcomes (acknowledged/missed)

---

## 🤖 ML Model Building

We trained **three different models** for each agent’s task using scikit-learn:

| Agent Type        | Algorithm Used     | Accuracy | Details |
|-------------------|--------------------|----------|---------|
| Health Monitoring | **Random Forest Classifier** | **95.2%** | Best performance on classifying 'Critical' vs 'Normal' health |
| Safety Monitoring | **Logistic Regression**      | **89.6%** | Lightweight model for binary classification of safety alerts |
| Daily Reminders   | **Decision Tree Classifier** | **91.8%** | Effectively handled routine adherence patterns |

Each model was serialized using Python’s pickle and stored in the models/ folder for reuse.
---

## 📊 Model Evaluation

Each model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

We ensured **balanced performance** across all classes (especially important for 'Critical' or 'Alert' classes).

---

## 🧩 Multi-Agent System

We implemented **three separate intelligent agents**:

| Agent               | File                 | Responsibility                              |
|---------------------|----------------------|----------------------------------------------|
| Health Agent        | agents.py          | Predict and manage health status             |
| Safety Agent        | agents.py          | Detect falls or alarms, generate alerts      |
| Reminder Agent      | agents.py          | Predict task adherence and routine support   |

They work **independently** but are **coordinated via Streamlit and API** to simulate multi-agent architecture.

---

## 🌐 API Development (Flask)

To enable model interaction, we built a Flask API (combined_api.py) with the following endpoints:

- /predict_health – takes vitals and returns health prediction  
- /predict_safety – detects safety alert  
- /predict_reminder – predicts if reminder will be acknowledged  
- /auto_predict – fetches latest entry from cleaned datasets and returns predictions

These APIs are triggered in the frontend using requests.post().

---

## 🌈 Streamlit Interface

Main file: app.py

The Streamlit frontend has:

- 📄 Tabs/pages for each agent  
- 🧪 Input widgets for new data (sliders, selectors)  
- ✅ Prediction results displayed instantly  
- 📊 Plotly charts to visualize trends  
- 🧠 Intelligent alerts when a prediction is critical

Also included: **“Auto Predict”** button that fetches latest user data and provides smart alerts.

---

## 🔁 System Flow Overview

plaintext
Raw Dataset ─▶ Data Cleaning ─▶ ML Training ─▶ Model (.pkl) ─▶ Flask API ─▶ Streamlit App
                                    ▲
                               Multi-Agent Logic


---

## 📍 Prediction Examples

| Agent        | Input Values                                  | Output           |
|--------------|------------------------------------------------|------------------|
| Health       | BP: 180/120, HR: 110, Temp: 102                | ❗ Critical       |
| Safety       | Event: Fall, Location: Bathroom, Call: No      | ⚠️ Emergency      |
| Reminder     | Task: Medicine, Time: 8 AM, Ack: No            | ❌ Missed Task    |

---

## 🧠 Challenges and Learnings

### Challenges:
- Designing realistic datasets
- Creating a scalable agent framework
- Managing data communication between frontend ↔ API ↔ models
- Streamlit component customization

### Learnings:
- Real-time ML with Streamlit + Flask
- Working with pickle, API endpoints, and prediction routing
- Agent-based architecture and smart prediction flows
- Enhanced frontend logic using condition-based rendering and Plotly

---

## ✅ Conclusion

We successfully built a **smart elderly care assistant** with a working **multi-agent system**, live **prediction models**, and an interactive **Streamlit dashboard**. The project showcases how AI can be used for socially impactful causes like elderly support.

---

## 📝 Optional Additions

- Add MongoDB or PostgreSQL for user-level data tracking
- Email/SMS alerts for emergency cases
- Deploy to **Streamlit Cloud** or **Render**