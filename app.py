import streamlit as st
import folium
import plotly.express as px
import pandas as pd
from fpdf import FPDF

# Importing Backend Feature Modules
from features.culture import generate_culture_info
from features.safety import generate_safety_tips
from features.travel_insights import generate_travel_insights
from features.recommendations import generate_recommendations
from features.itinerary import generate_itinerary
from features.budget import estimate_budget
from features.chatbot import travel_chat

# Importing Backend Live Geolocation/Weather APIs
from apis.restaurants_api import get_restaurants
from apis.nearby_places import get_nearby_places
from apis.map_api import get_place_coordinates
from apis.weather_api import get_weather
from apis.unsplash_api import get_destination_image
from apis.hotel_api import search_accommodations

# Importing AI Inference Engine
from ai.groq_engine import ask_ai


# =====================================================
# PDF EXPORT GENERATOR WITH ACCENT REPLACEMENT
# =====================================================
def create_trip_pdf():
    def clean_text(text):
        text = str(text)
        text = text.replace("₹", "Rs. ")
        text = text.replace("•", "-")
        return text.encode("latin-1", "ignore").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200, 10, "AI Powered Travel Planner Report", ln=True, align="C")
    pdf.ln(10)

    # 1. OVERVIEW SECTION
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "1. Destination Overview", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(st.session_state.overview))
    pdf.ln(5)

    # 2. ITINERARY SECTION
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "2. Travel Itinerary Schedule", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(st.session_state.itinerary))
    pdf.ln(5)

    # 3. RECOMMENDATIONS SECTION
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "3. Smart AI Recommendations", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(st.session_state.recommendations))
    pdf.ln(5)

    # 4. SAFETY & GUIDANCE
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "4. Safety & Travel Guidance", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(st.session_state.safety_info))

    return pdf.output(dest='S').encode('latin-1')


# =====================================================
# STREAMLIT WINDOW & PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AI Powered Travel Planner",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# SYSTEM PERSISTENT STATE INITIALIZATION
# =====================================================
if "messages" not in st.session_state: st.session_state.messages = []
if "trip_generated" not in st.session_state: st.session_state.trip_generated = False
if "itinerary" not in st.session_state: st.session_state.itinerary = ""
if "weather" not in st.session_state: st.session_state.weather = {"temperature": "N/A", "condition": "N/A", "wind_speed": "N/A"}
if "image_url" not in st.session_state: st.session_state.image_url = ""
if "cost" not in st.session_state: st.session_state.cost = ""
if "overview" not in st.session_state: st.session_state.overview = ""
if "recommendations" not in st.session_state: st.session_state.recommendations = ""
if "insights" not in st.session_state: st.session_state.insights = {}
if "safety_info" not in st.session_state: st.session_state.safety_info = ""
if "culture_info" not in st.session_state: st.session_state.culture_info = ""
if "accommodations" not in st.session_state: st.session_state.accommodations = None
if "saved_destination" not in st.session_state: st.session_state.saved_destination = ""


# =====================================================
# CUSTOM CSS CODE (TOP CHAT INPUT WITH NEON FIX)
# =====================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #030514 !important;
    background: radial-gradient(circle at top right, #090b26, #030514) !important;
    color: #f1f5f9;
    font-family: 'Segoe UI', -apple-system, sans-serif;
}
.stApp {
    background-color: #030514 !important;
}

/* REMOVING STREAMLIT DEFAULT VERTICAL PADDING & MARGINS */
[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}
.block-container {
    padding: 1.5rem 2.5rem 1rem 2.5rem !important;
    max-width: 98%;
}

/* PREMIUM NAVIGATION BAR */
.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
    margin-top: -15px;
}
.brand-title {
    font-size: 24px;
    font-weight: 700;
    color: white;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nav-links {
    display: flex;
    gap: 28px;
    align-items: center;
}
.nav-item {
    color: #94a3b8;
    font-size: 15px;
    font-weight: 500;
    text-decoration: none;
}
.nav-item.active {
    color: white;
    border-bottom: 2px solid #a855f7;
    padding-bottom: 4px;
}
.chat-btn {
    background: rgba(30, 27, 75, 0.5);
    border: 1px solid #4338ca;
    padding: 6px 18px;
    border-radius: 20px;
    color: white;
    font-weight: 500;
}

/* HERO TEXT DESIGN */
.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 20px;
    color: white;
    margin-top: 0px !important;
}
.hero-title span {
    background: linear-gradient(90deg, #3b82f6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* FORM OVERRIDES */
.form-row {
    display: flex;
    align-items: center;
    padding: 12px 0px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.row-label {
    width: 150px;
    font-size: 15px;
    font-weight: 600;
    color: #94a3b8;
}
label { display: none !important; }
.stTextInput input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    border-radius: 0px !important;
    font-size: 16px;
    padding-left: 0px !important;
}
.stSelectbox div[data-baseweb="select"] {
    background: transparent !important;
    border: none !important;
    color: #a855f7 !important;
    font-weight: 600;
    font-size: 16px;
}
.stSlider [data-testid="stSliderTickBar"] { display:none; }

/* ACTION BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #d946ef) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 10px 28px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(217, 70, 239, 0.25);
    margin-top: 15px;
}

/* GRID INFRASTRUCTURE */
.feature-section-title {
    font-size: 18px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 18px;
    color: #f1f5f9;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}
.feature-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #cbd5e1;
}
.feature-icon { font-size: 22px; }
.feature-text { font-weight: 500; font-size: 14px; line-height: 1.2; }
.feature-text span { font-size: 12px; color: #64748b; display: block; }

/* =====================================================
   CLEAN FIXED TOP CHAT DESIGN
   ===================================================== */
.chat-container {
    background: transparent !important;
    border: none !important;
    padding: 0px !important;
    margin: 0px !important;
}

.chat-input-wrapper {
    margin-bottom: 0px !important;
    padding: 0px !important;
    width: 100% !important;
}

.chat-history-box {
    background: #060818 !important;
    border: 1px solid #1e293b !important;
    border-radius: 20px !important;
    padding: 15px !important;
    max-height: 400px !important;
    overflow-y: auto !important;
    margin-top: 15px !important;
}

.chat-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 10px;
    margin-bottom: 12px;
}

.online-indicator {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
}

.chat-bullet {
    color: #64748b;
    font-size: 13px;
    margin-top: 12px;
    padding-left: 5px;
}

/* NATIVE STREAMLIT INTERFACE CONFIGURATION */
div[data-testid="stChatInput"] {
    padding: 0px !important;
    background: transparent !important;
    width: 100% !important;
}
div[data-testid="stChatInput"] textarea {
    background-color: #0f172a !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* RENDER LAYER COMPONENT TABS */
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] {
    background: #0f172a;
    border-radius: 16px;
    padding: 4px 14px;
    color: #94a3b8;
    font-size: 14px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #2563eb, #d946ef) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# RENDER HEADER NAVIGATION BAR CONTROL
# =====================================================
st.markdown("""
<div class="nav-container">
    <div class="brand-title">🌏 AI Powered Travel Planner ✨</div>
    <div class="nav-links">
        <div class="nav-item active">Home</div>
        <div class="nav-item">Features</div>
        <div class="nav-item">About</div>
        <div class="nav-item">Guide</div>
        <div class="chat-btn">💬 AI Chat</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# DYNAMIC UI MATRIX LAYER SWITCHER
# =====================================================
if not st.session_state.trip_generated:
    
    left, right = st.columns([3.8, 1.8], gap="large")

    with left:
        st.markdown('<h1 class="hero-title">Plan Your <span>Perfect Trip</span> 🚀</h1>', unsafe_allow_html=True)

        st.markdown('<div class="form-row"><div class="row-label">📍 Destination :</div>', unsafe_allow_html=True)
        destination = st.text_input("Destination Search Element", placeholder="Enter your dream destination...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-row"><div class="row-label">📅 Days :</div>', unsafe_allow_html=True)
        days = st.slider("Trip Duration Selector", 1, 15, 5, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-row"><div class="row-label">💰 Budget :</div>', unsafe_allow_html=True)
        budget = st.selectbox("Budget Profile Selector", ["Low", "Medium", "Luxury"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-row"><div class="row-label">✈️ Travel Style :</div>', unsafe_allow_html=True)
        style = st.selectbox("Interests Profile Selection", ["Adventure", "Relaxation", "Family", "Cultural"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        generate = st.button("✨ Generate Travel Plan")

        st.markdown('<div class="feature-section-title">What You Get With AI Powered Travel Planner</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-grid">
            <div class="feature-card"><div class="feature-icon">🗺️</div><div class="feature-text">AI Itinerary <span>Generation</span></div></div>
            <div class="feature-card"><div class="feature-icon">🧠</div><div class="feature-text">Smart <span>Recommendations</span></div></div>
            <div class="feature-card"><div class="feature-icon">🌤️</div><div class="feature-text">Weather <span>Insights</span></div></div>
            <div class="feature-card"><div class="feature-icon">📍</div><div class="feature-text">Tourist <span>Attractions</span></div></div>
            <div class="feature-card"><div class="feature-icon">🏨</div><div class="feature-text">Hotel <span>Discovery</span></div></div>
            <div class="feature-card"><div class="feature-icon">🍴</div><div class="feature-text">Restaurant <span>Suggestions</span></div></div>
            <div class="feature-card"><div class="feature-icon">📊</div><div class="feature-text">Budget <span>Analytics</span></div></div>
            <div class="feature-card"><div class="feature-icon">🛡️</div><div class="feature-text">Travel Safety <span>Guidance</span></div></div>
        </div>
        """, unsafe_allow_html=True)

    if generate and destination:
        with st.spinner("🧠 AI Engine compiling your dream travel blueprints..."):
            st.session_state.trip_generated = True
            st.session_state.saved_destination = destination

            st.session_state.image_url = get_destination_image(destination)
            st.session_state.overview = ask_ai(f"Provide a brief overview for {destination} suitable for a {style} trip.")
            st.session_state.weather = get_weather(destination)
            st.session_state.itinerary = generate_itinerary(destination, days, budget, style)
            st.session_state.recommendations = generate_recommendations(destination, budget, style, days)
            st.session_state.insights = generate_travel_insights(style)
            st.session_state.safety_info = generate_safety_tips(destination, style, st.session_state.weather)
            st.session_state.culture_info = generate_culture_info(destination, style)
            st.session_state.accommodations = search_accommodations(destination)
            st.session_state.cost = estimate_budget(days, budget)
            st.rerun()

    with right:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 1. Chat Input Field (ALWAYS REMAIN AT THE ABSOLUTE TOP)
        st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
        user_query = st.chat_input("Ask any travel question...", key="init_chat")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 2. GRADIENT TEXT STYLE HEADING (Matches 'Plan Your Perfect Trip')
        st.markdown("""
        <div style="
            text-align: center; 
            margin-top: 15px; 
            margin-bottom: 10px; 
            font-size: 24px; 
            font-weight: 800; 
            letter-spacing: 0.5px;
        ">
            💬 <span style="
                background: linear-gradient(90deg, #3b82f6, #a855f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">GlobWise Ai</span>
        </div>
        """, unsafe_allow_html=True)
        
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            response_string = travel_chat(user_query, destination if destination else "")
            st.session_state.messages.append({"role": "assistant", "content": response_string})
            st.rerun()

        # 3. Chat Data Box Appears BELOW only if messages populate inside session
        if st.session_state.messages:
            st.markdown('<div class="chat-history-box">', unsafe_allow_html=True)
            st.markdown('<div class="chat-top-bar"><div style="font-size:14px; font-weight:600; color:#94a3b8;">Conversation</div><div class="online-indicator">Online</div></div>', unsafe_allow_html=True)
            
            for message in reversed(st.session_state.messages):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:12px;"><div class="chat-bullet">🔹 Ask for routes, cafes or travel hacks!</div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

else:
    
    left, right = st.columns([3.8, 1.8], gap="large")

    with left:
        if st.button("⬅️ Plan Another Trip"):
            st.session_state.trip_generated = False
            st.rerun()

        current_dest = st.session_state.saved_destination
        lat, lon = get_place_coordinates(current_dest)

        tabs = st.tabs([
            "🌍 Overview", "🗓 Itinerary", "📍 Attractions", "🍴 Food", 
            "🏨 Hotels", "🎭 Culture", "🧠 Recommendations", "📊 Insights", "💸 Budget", "🛡 Safety"
        ])

        # Overview Tab
        with tabs[0]:
            st.header("🌦 Current Atmospheric Weather Window")
            w_data = st.session_state.weather
            w_col1, w_col2, w_col3 = st.columns(3)
            w_col1.metric("🌡 Temperature", f"{w_data.get('temperature', 'N/A')}°C")
            w_col2.metric("☁ Condition", w_data.get('condition', 'N/A'))
            w_col3.metric("💨 Wind Speed", f"{w_data.get('wind_speed', 'N/A')} m/s")
            
            st.header(f"🌍 Overview Profile: {current_dest}")
            st.markdown(st.session_state.overview)
            if st.session_state.image_url:
                st.image(st.session_state.image_url, use_container_width=True)
                
            if lat and lon:
                st.subheader("🗺️ Center Location Interactive Routing Map")
                travel_map = folium.Map(location=[lat, lon], zoom_start=12)
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                popup_html = f'<div style="font-family:sans-serif;font-size:12px;text-align:center;"><b style="color:#030514;">{current_dest}</b><br><br><a href="{google_maps_url}" target="_blank" style="display:inline-block;background-color:#2563eb;color:white;padding:5px 10px;text-decoration:none;border-radius:4px;font-weight:bold;">🗺️ Open Google Maps</a></div>'
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"Center Anchor: {current_dest}",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(travel_map)
                st.iframe(travel_map._repr_html_(), height=400)
            
            pdf_bytes = create_trip_pdf()
            st.download_button(label="⬇ Download Complete PDF Blueprint Report", data=pdf_bytes, file_name=f"{current_dest}_travel_plan.pdf", mime="application/pdf")

        # Itinerary Tab
        with tabs[1]:
            st.header("🗓 Modular AI Trip Schedule")
            st.markdown(st.session_state.itinerary)

        # Attractions Tab
        with tabs[2]:
            st.header("📍 Highly Ranked Tourist Attractions")
            nearby_places = get_nearby_places(current_dest)
            if nearby_places:
                attractions_map = folium.Map(location=[lat, lon], zoom_start=11)
                for place in nearby_places:
                    st.markdown(f"### 📌 {place['name']}\n🗺️ *Location Node: {place['address']}*")
                    g_maps_link = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
                    p_html = f'<div style="font-family:sans-serif;font-size:12px;"><b>{place["name"]}</b><br><br><a href="{g_maps_link}" target="_blank" style="display:inline-block;background-color:#a855f7;color:white;padding:4px 8px;text-decoration:none;border-radius:4px;font-weight:bold;">🚗 Open Route in Maps</a></div>'
                    
                    folium.Marker(
                        [place['lat'], place['lon']], 
                        popup=folium.Popup(p_html, max_width=250),
                        tooltip=place['name']
                    ).add_to(attractions_map)
                st.iframe(attractions_map._repr_html_(), height=450)
            else:
                st.info("No attraction entries found from nearby live map vectors.")

        # Restaurants
        with tabs[3]:
            st.header("🍴 Food Suggestions & Local Restaurants")
            restaurants = get_restaurants(current_dest)
            if restaurants:
                restaurant_map = folium.Map(location=[lat, lon], zoom_start=11)
                for rest in restaurants:
                    st.markdown(f"### 🍽 {rest['name']}\n📍 *Address: {rest['address']}*")
                    g_maps_link = f"https://www.google.com/maps/search/?api=1&query={rest['lat']},{rest['lon']}"
                    p_html = f'<div style="font-family:sans-serif;font-size:12px;"><b>{rest["name"]}</b><br><br><a href="{g_maps_link}" target="_blank" style="display:inline-block;background-color:#10b981;color:white;padding:4px 8px;text-decoration:none;border-radius:4px;font-weight:bold;">🍴 View Google Maps</a></div>'
                    
                    folium.Marker(
                        [rest['lat'], rest['lon']], 
                        popup=folium.Popup(p_html, max_width=250),
                        tooltip=rest['name'], 
                        icon=folium.Icon(color='green', icon='cutlery')
                    ).add_to(restaurant_map)
                st.iframe(restaurant_map._repr_html_(), height=450)
            else:
                st.info("No catering restaurants returned from geolocation APIs.")

        # Accommodations
        with tabs[4]:
            st.header("🏨 Recommended Stay Accommodations")
            accommodations = st.session_state.accommodations
            if accommodations and "features" in accommodations:
                hotel_map = folium.Map(location=[lat, lon], zoom_start=11)
                for place in accommodations["features"][:10]:
                    props = place["properties"]
                    h_lat, h_lon = props.get('lat'), props.get('lon')
                    if h_lat and h_lon:
                        st.markdown(f"### 🏨 {props.get('name', 'Unnamed Hotel')}\n📍 *Address: {props.get('formatted', 'No address')}*")
                        g_maps_link = f"https://www.google.com/maps/search/?api=1&query={h_lat},{h_lon}"
                        p_html = f'<div style="font-family:sans-serif;font-size:12px;"><b>{props.get("name", "Hotel")}</b><br><br><a href="{g_maps_link}" target="_blank" style="display:inline-block;background-color:#2563eb;color:white;padding:4px 8px;text-decoration:none;border-radius:4px;font-weight:bold;">🏨 Route & Directions</a></div>'
                        
                        folium.Marker(
                            [h_lat, h_lon], 
                            popup=folium.Popup(p_html, max_width=250),
                            tooltip=props.get('name', 'Hotel'), 
                            icon=folium.Icon(color='purple', icon='home')
                        ).add_to(hotel_map)
                st.iframe(hotel_map._repr_html_(), height=450)
            else:
                st.info("No hotel property nodes registered around this target boundary.")

        # Culture Insights
        with tabs[5]:
            st.header("🎭 Local Culture, Traditions & Etiquette")
            st.markdown(st.session_state.culture_info)

        # Recommendations
        with tabs[6]:
            st.header("🧠 Smart AI Destination Recommendations")
            st.markdown(st.session_state.recommendations)

        # Analytical Score Vector Gauges
        with tabs[7]:
            st.header("📊 Travel Metric Diagnostic Insights")
            ins = st.session_state.insights
            i_col1, i_col2 = st.columns(2)
            i_col1.metric("🌤 Weather Score Rating", f"{ins.get('Weather Score', '8.5')}/10")
            i_col1.metric("🛡 Security Vector Score", f"{ins.get('Safety Score', '8.9')}/10")
            i_col2.metric("💰 Cost Optimization Score", f"{ins.get('Budget Friendliness', '7.8')}/10")
            i_col2.metric("🎒 Action Density Rating", f"{ins.get('Adventure Level', '8.0')}/10")

        # Budget Matrix Analytics
        with tabs[8]:
            st.header("💸 Financial Budget Expense Allocations")
            st.subheader(st.session_state.cost)
            
            budget_df = pd.DataFrame({
                "Category": ["Accommodation", "Food & Dining", "Transport Logistics", "Attractions & Activities", "Emergency Buffer"],
                "Distribution Ratio": [35, 25, 20, 12, 8]
            })
            fig = px.pie(budget_df, values="Distribution Ratio", names="Category", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)

        # Security Advice Layout
        with tabs[9]:
            st.header("🛡 Tactical Safety Advisor Protocols")
            st.markdown(st.session_state.safety_info)

    with right:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 1. Chat Input Field (ALWAYS REMAIN AT THE ABSOLUTE TOP)
        st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
        user_query = st.chat_input("Ask any travel question...", key="gen_chat")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 2. GRADIENT TEXT STYLE HEADING (Matches 'Plan Your Perfect Trip')
        st.markdown("""
        <div style="
            text-align: center; 
            margin-top: -5px; 
            margin-bottom: 15px; 
            font-size: 24px; 
            font-weight: 800; 
            letter-spacing: 0.5px;
        ">
            💬 <span style="
                background: linear-gradient(90deg, #3b82f6, #a855f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">GlobeWise Ai</span>
        </div>
        """, unsafe_allow_html=True)
        
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            response_string = travel_chat(user_query, st.session_state.saved_destination)
            st.session_state.messages.append({"role": "assistant", "content": response_string})
            st.rerun()

        # 3. Chat Data Box Appears BELOW only if messages populate inside session
        if st.session_state.messages:
            st.markdown('<div class="chat-history-box">', unsafe_allow_html=True)
            st.markdown('<div class="chat-top-bar"><div style="font-size:14px; font-weight:600; color:#94a3b8;">Conversation</div><div class="online-indicator">Online</div></div>', unsafe_allow_html=True)
            
            for message in reversed(st.session_state.messages):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:12px;"><div class="chat-bullet">🔹 Ask for routes, cafes or travel hacks!</div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)