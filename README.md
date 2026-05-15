#  AI Powered Travel Planner

##  Problem Statement

This project was developed for the **Claysys AI Hackathon** under the **Gen AI LLM Projects** category.

Problem Statement:

> Design an AI assistant that generates end-to-end travel itineraries based on user input such as destination, duration, budget, and interests. The solution should suggest travel options, accommodations, key attractions, and local cuisines or beverages to try. Bonus points for integrating real-time data or external APIs.

---

#  Project Overview

AI Powered Travel Planner is an intelligent tourism assistant built using **Python**, **Streamlit**, **LLMs**, and **real-time APIs**.

The application provides users with a smart travel planning experience by generating personalized travel itineraries, tourism insights, accommodation suggestions, weather information, transport guidance, cultural recommendations, and AI-powered travel conversations.

The system combines **Artificial Intelligence** with **real-world tourism APIs** to create a scalable and interactive travel planning platform.

---

#  Features

##  AI-Powered Travel Planning
- Generates personalized itineraries
- Travel recommendations based on:
  - destination
  - duration
  - budget
  - travel style

---

##  AI Destination Overview
- Real AI-generated tourism descriptions
- Explains:
  - tourism importance
  - attractions
  - local experiences
  - culture
  - activities

---

##  Live Weather Information
- Real-time weather updates
- Climate-aware travel guidance

---

##  Accommodation Suggestions
- Hotel and stay recommendations
- Nearby accommodation discovery

---

##  Tourist Attractions & Nearby Places
- Famous attractions
- Nearby destinations
- Sightseeing suggestions
- One-day trip locations

---

##  Food & Restaurant Guidance
- Local cuisine recommendations
- Traditional food guidance
- Popular food experiences

---

##  Culture & Traditions
- Cultural insights
- Local etiquette
- Traditions and tourism behavior

---

##  Clothing Suggestions
- Destination-based travel clothing guidance
- Weather-aware preparation suggestions

---

##  Transport Guidance
- Public transport suggestions
- Taxi and travel guidance
- Tourist transportation information

---

##  Budget Estimation
- Travel cost estimation
- Budget categories:
  - Low
  - Medium
  - Luxury

---

##  AI Travel Chatbot
Interactive AI assistant capable of answering:
- nearby places
- tourist attractions
- transport help
- food suggestions
- safety guidance
- tourism assistance

---

# 🏗 Solution Approach

The project follows a modular AI-based architecture.

### Workflow:
1. User enters destination and travel preferences
2. AI generates itinerary and tourism overview
3. APIs fetch:
   - weather data
   - destination images
   - accommodation details
4. Chatbot provides interactive travel assistance
5. Streamlit frontend displays all travel information dynamically

The architecture is designed for scalability and future feature integration.

---

# 🧠 Technologies Used

## Frontend
- Streamlit

## Backend
- Python

## AI Integration
- Groq API
- Llama 3.1 Model

## APIs Used
- OpenWeather API
- Unsplash API
- Geoapify API

---

# 📂 Project Structure


ai_powered_travel_planner/
│
├── app.py
├── requirements.txt
├── .env
│
├── ai/
│   └── groq_engine.py
│
├── apis/
│   ├── weather_api.py
│   ├── unsplash_api.py
│   └── hotel_api.py
│
├── features/
│   ├── itinerary.py
│   ├── chatbot.py
│   └── budget.py
│
└── ui/