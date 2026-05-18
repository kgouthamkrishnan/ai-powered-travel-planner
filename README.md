# AI Powered Travel Planner 🌍✨

AI Powered Travel Planner is an intelligent tourism assistance platform that leverages Generative AI and real-time APIs to deliver personalized travel experiences. The application helps users plan complete trips by generating smart itineraries, destination insights, accommodation suggestions, weather updates, travel recommendations, and AI-powered conversational assistance.

The platform combines Large Language Models (LLMs) with live tourism data to create a modern and scalable travel planning ecosystem capable of adapting to different user preferences, travel styles, and budget categories.

---

# 📌 Project Overview

The primary objective of the project is to simplify travel planning through Artificial Intelligence. Users can enter travel preferences such as destination, duration, budget, and travel interests, and the system dynamically generates personalized travel guidance.

The application integrates multiple external APIs and AI modules to provide:
- AI-generated travel itineraries
- destination overviews
- weather intelligence
- accommodation discovery
- tourist attraction guidance
- food recommendations
- cultural insights
- travel safety assistance
- interactive AI conversations

The system is designed using a modular architecture to ensure scalability, maintainability, and seamless future enhancements.

---

# ✨ Key Features

## 🧠 AI-Powered Itinerary Generation

The platform generates intelligent and personalized travel itineraries based on the user's selected destination, trip duration, travel style, and budget preferences. The AI engine dynamically structures travel schedules and recommends activities suitable for the traveler’s interests.

---

## 🌍 Destination Intelligence

The application provides AI-generated destination overviews that explain tourism significance, local attractions, activities, travel experiences, and important highlights related to the selected destination.

---

## 🌦 Real-Time Weather Integration

The system integrates live weather APIs to provide current climate conditions, temperature updates, and weather-aware travel guidance, helping users prepare better for their trips.

---

## 🏨 Accommodation Discovery

Users receive hotel and accommodation suggestions fetched through real-time APIs. The platform assists travelers in identifying nearby stay options suitable for different travel budgets and preferences.

---

## 📍 Tourist Attractions & Nearby Places

The application identifies famous tourist destinations, nearby attractions, sightseeing spots, and local points of interest to improve the overall travel experience.

---

## 🍴 Food & Restaurant Recommendations

The platform recommends local cuisines, traditional dishes, and popular restaurants to help travelers explore authentic food experiences at their destination.

---

## 🎭 Cultural & Local Guidance

The system provides cultural insights, local etiquette guidance, traditions, and tourism-related behavioral recommendations to help travelers better understand the destination environment.

---

## 👕 Smart Travel Preparation

The application offers weather-aware clothing and preparation suggestions based on the destination’s climate conditions and travel season.

---

## 🚖 Travel Assistance & Navigation

The platform provides guidance regarding local transportation, travel movement, and tourist-friendly navigation assistance for easier destination exploration.

---

## 💸 Budget Analytics

AI Powered Travel Planner estimates travel expenses and categorizes trips into Low, Medium, and Luxury budget profiles. The system also provides expense distribution insights for improved financial planning.

---

## 📄 AI Travel Report Generation

The platform includes an integrated PDF report generation system that enables users to download complete travel plans for offline access and future reference. The generated report compiles important travel information into a structured and user-friendly document.

The downloadable travel report includes:
- personalized itinerary details
- destination overview
- AI-generated recommendations
- travel safety guidance
- tourism insights and planning information

This feature enhances the practical usability of the application by allowing travelers to store, share, and access their travel plans conveniently during their journey.

---

## 💬 AI Travel Chatbot

An integrated AI chatbot assists users through conversational interactions. Travelers can ask questions related to attractions, nearby places, transport, restaurants, travel safety, and tourism assistance in real time.

---

# 🏗️ System Workflow

The application follows a modular AI-driven workflow. Users first provide travel preferences such as destination, trip duration, budget, and travel style. The AI engine then processes this information and generates personalized travel recommendations and itineraries.

Simultaneously, multiple external APIs fetch live tourism data including weather conditions, destination imagery, accommodation information, nearby attractions, and restaurant recommendations.

The Streamlit frontend dynamically presents all generated travel intelligence through an interactive and user-friendly interface, while the AI chatbot enables real-time tourism assistance and conversational support.

---

# 🧠 Technologies Used

### Frontend
- Streamlit

### Backend
- Python

### Artificial Intelligence
- Groq API
- Llama 3.1 Large Language Model (LLM)

### External APIs
- OpenWeather API
- Unsplash API
- Geoapify API

### Visualization & Mapping
- Plotly
- Folium Maps

---

# 📂 Project Structure

```plaintext
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
│   ├── hotel_api.py
│   ├── restaurants_api.py
│   ├── nearby_places.py
│   └── map_api.py
│
├── features/
│   ├── itinerary.py
│   ├── chatbot.py
│   ├── budget.py
│   ├── recommendations.py
│   ├── culture.py
│   ├── safety.py
│   └── travel_insights.py
│
└── ui/