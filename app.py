import streamlit as st
from features.itinerary import generate_itinerary
from apis.weather_api import get_weather
from apis.unsplash_api import get_destination_image
from features.budget import estimate_budget
from apis.hotel_api import search_accommodations
from features.chatbot import travel_chat
from ai.groq_engine import ask_ai

# PAGE CONFIG

st.set_page_config(
    page_title="AI Powered Travel Planner",
    layout="wide"
)

# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "trip_generated" not in st.session_state:
    st.session_state.trip_generated = False

if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "weather" not in st.session_state:
    st.session_state.weather = ""

if "image_url" not in st.session_state:
    st.session_state.image_url = ""

if "cost" not in st.session_state:
    st.session_state.cost = ""

if "overview" not in st.session_state:
    st.session_state.overview = ""

if "accommodations" not in st.session_state:
    st.session_state.accommodations = None

# CUSTOM CSS

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #020817;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0rem;
    max-width: 100%;
}

.panel {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1e293b;
}

.stButton > button {

    width: 100%;
    background-color: #ff6600;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

.stTextInput input {
    background-color: #111827;
    color: white;
}

::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# LAYOUT

left, right = st.columns([2, 1])

# LEFT PANEL

with left:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.title("🌍 AI Powered Travel Planner")

    st.subheader("✈ Trip Generator")

    destination = st.text_input("📍 Destination")

    days = st.slider(
        "🗓 Days",
        1,
        15,
        5
    )

    budget = st.selectbox(
        "💰 Budget",
        ["Low", "Medium", "Luxury"]
    )

    style = st.selectbox(
        "🌍 Travel Style",
        ["Adventure", "Relaxation", "Family", "Cultural"]
    )

    generate = st.button("Generate Travel Plan")

    # GENERATE ONLY ONCE

    if generate:

        st.session_state.trip_generated = True

        st.session_state.image_url = get_destination_image(destination)

        st.session_state.weather = get_weather(destination)

        st.session_state.itinerary = generate_itinerary(
            destination,
            days,
            budget,
            style
        )

        st.session_state.cost = estimate_budget(
            days,
            budget
        )

        st.session_state.accommodations = search_accommodations(
            destination
        )

        # REAL AI OVERVIEW

        st.session_state.overview = ask_ai(f"""
        Give a detailed tourism overview about {destination}.

        Include:
        - why the destination is famous
        - tourism importance
        - culture
        - best experiences
        - nature
        - attractions
        - tourist activities

        Keep it professional and tourist friendly.
        """)

    # BEFORE GENERATE

    if not st.session_state.trip_generated:

        st.markdown("""
        ## Welcome

        Your intelligent AI tourism assistant helps users plan smarter trips using AI.

        ### Features

        - 🗺 AI itinerary generation
        - 🌦 Weather forecasting
        - 🏨 Accommodation suggestions
        - 💰 Budget estimation
        - 🍴 Food guidance
        - 🚖 Transport help
        - 📍 Tourist attraction suggestions
        - 💬 AI travel chatbot
        """)

    # AFTER GENERATE

    if st.session_state.trip_generated:

        st.success(f"Welcome to {destination} ✈")

        # DESTINATION OVERVIEW

        st.markdown("---")
        st.header(f"🌍 About {destination}")

        st.write(st.session_state.overview)

        # DESTINATION IMAGE

        st.markdown("---")
        st.header("📸 Destination Preview")

        if st.session_state.image_url:
            st.image(
                st.session_state.image_url,
                width="stretch"
            )

        # WEATHER

        st.markdown("---")
        st.header("🌦 Weather Information")

        st.info(st.session_state.weather)

        # AI ITINERARY

        st.markdown("---")
        st.header("🗺 AI Itinerary")

        st.write(st.session_state.itinerary)

        # TOURIST SPOTS

        st.markdown("---")
        st.header("📍 Tourist Attractions & Nearby Places")

        st.markdown(f"""
        Explore the best tourist destinations in and around **{destination}**:

        ### 🌟 Main Attractions
        - Historical landmarks
        - Nature destinations
        - Adventure activities
        - Photography locations
        - Cultural hotspots
        - Tourist-friendly attractions

        ### 🗺 Nearby Visiting Places
        - Popular nearby towns and cities
        - Hill stations and beaches
        - Waterfalls and parks
        - Museums and heritage sites
        - Religious and spiritual places
        - One-day trip destinations around {destination}

        ### 📸 Best Experiences
        - Local sightseeing
        - Sunrise and sunset points
        - Shopping streets and local markets
        - Hidden gems and peaceful spots
        - Family-friendly attractions
        """)

        # FOOD SPOTS

        st.markdown("---")
        st.header("🍴 Food & Restaurants")

        st.markdown(f"""
        Discover popular food experiences in **{destination}**:

        - Famous local foods
        - Traditional cuisines
        - Popular restaurants
        - Cafes and bakeries
        - Street food areas
        - Vegetarian and non-vegetarian specialties
        """)

        # ACCOMMODATION

        st.markdown("---")
        st.header("🏨 Accommodation Spots")

        try:

            accommodations = st.session_state.accommodations

            if accommodations and "features" in accommodations:

                for place in accommodations["features"][:5]:

                    props = place["properties"]

                    name = props.get(
                        "name",
                        "Unknown Place"
                    )

                    address = props.get(
                        "formatted",
                        "No Address"
                    )

                    st.markdown(f"""
                    ### 🏨 {name}

                    📍 {address}
                    """)

            else:
                st.warning("No accommodations found")

        except Exception as e:

            st.error(f"Accommodation Error: {e}")

        # CULTURE

        st.markdown("---")
        st.header("🏛 Culture & Traditions")

        st.markdown(f"""
        Culture and traditions in **{destination}** may include:

        - Local festivals and celebrations
        - Traditional foods and cuisines
        - Regional customs and etiquette
        - Religious and cultural practices
        - Traditional music and dance
        - Lifestyle of local people
        """)

        # CLOTHING

        st.markdown("---")
        st.header("👕 Clothing Suggestions")

        st.markdown(f"""
        Recommended clothing for **{destination}**:

        - Comfortable walking shoes
        - Lightweight casual wear
        - Sunglasses and caps
        - Raincoat or umbrella if needed
        - Warm jackets for cold destinations
        - Traditional-friendly outfits
        """)

        # TRANSPORT

        st.markdown("---")
        st.header("🚖 Transport & Travel")

        st.markdown(f"""
        Common transport options available in **{destination}**:

        - Local buses
        - Taxi and cab services
        - Train or metro connectivity
        - Rental bikes and scooters
        - Airport transportation
        """)

        # BUDGET

        st.markdown("---")
        st.header("💸 Estimated Budget")

        st.success(st.session_state.cost)

        # SAFETY TIPS

        st.markdown("---")
        st.header("🛡 Safety Tips")

        st.markdown(f"""
        Safety recommendations while visiting **{destination}**:

        - Keep emergency contacts saved
        - Carry local currency
        - Stay hydrated
        - Use verified transportation
        - Avoid isolated places at night
        """)

        # TRAVEL ESSENTIALS

        st.markdown("---")
        st.header("🎒 Travel Essentials")

        st.markdown(f"""
        Essentials to carry while travelling to **{destination}**:

        - Passport / ID proof
        - Power bank
        - Mobile charger
        - Medicines
        - Water bottle
        - Offline maps
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT PANEL

with right:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("💬 AI Travel Chat")

    st.markdown("""
    Ask anything:

    - nearby places
    - tourist attractions
    - foods
    - transport
    - safety tips
    - emergency helplines
    - hidden spots
    """)

    # CHAT INPUT

    user_input = st.chat_input(
        "Ask travel questions..."
    )

    # HANDLE INPUT

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = travel_chat(
            user_input,
            destination
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    # DISPLAY CHAT HISTORY

    for message in reversed(st.session_state.messages):

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown("</div>", unsafe_allow_html=True)