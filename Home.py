import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(   
    page_title="Alera – NBA Scouting Assistant",
    layout="wide",
    initial_sidebar_state="collapsed")

# ---------------------
# Load + Encode Logo
# ---------------------
logo = Image.open("Logo.png")  # Update path if needed
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_b64 = base64.b64encode(buffered.getvalue()).decode()

# ---------------------
# Custom CSS Styling
# ---------------------
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    html, body, [class*="css"] {
        background-color: #f8f9fa;
    }
    .logo-container {
        animation: float 4s ease-in-out infinite;
        transition: all 0.3s ease;
        filter: drop-shadow(0 0 15px rgba(0, 122, 255, 0.2));
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }
    .launch-btn {
        background-color: #007BFF;
        color: white;
        padding: 0.75em 2.5em;
        border: none;
        border-radius: 30px;
        font-size: 1.1em;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        width: auto;
    }
    .launch-btn:hover {
        background-color: #0056b3;
        transform: scale(1.04);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------
# Branding Block
# ---------------------
st.markdown(f"""
    <div style="text-align: center; padding-top: 80px;">
        <img src="data:image/png;base64,{logo_b64}" width="140" class="logo-container" style="margin-bottom: 30px;" />
        <h1 style="font-size: 2.8em; font-weight: 600; margin: 0;">Alera – Player Scouter</h1>
        <p style="font-size: 1.3em; font-style: italic; color: gray; margin-top: 10px;">
            "Your Vision, Their Future."
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------------
# Let's Go Button
# ---------------------
clicked = st.markdown("""
    <div style="text-align: center; margin-top: 5px;">
        <a href="?nav=ScoutPlayers">
            <button style="
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 0.8em 2.5em;
                font-size: 1.1em;
                font-weight: 500;
                border-radius: 30px;
                cursor: pointer;
                transition: all 0.3s ease;
            " onmouseover="this.style.backgroundColor='#0056b3'" onmouseout="this.style.backgroundColor='#007BFF'">
                Let's Go Scouting
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Detect manual nav and switch
if st.query_params.get("nav") == "ScoutPlayers":
    st.switch_page("pages/ScoutPlayers.py")


# ---------------------
# About Section
# ---------------------
st.markdown("""
## About Alera
Alera empowers scouts, coaches, and managers by providing AI-powered player recommendations. 
Our system intelligently blends player stats with qualitative scouting insights to help you find the perfect player for your team.
""")

# ---------------------
# Features Section
# ---------------------
st.markdown("""
## Features
- **AI-Powered Player Scouting**
- **Deep Analytics and Player Comparisons**
- **Custom Attribute Search**
- **Real-Time Tableau Dashboards**
- **Seamless User Experience**
""")

# ---------------------
# How It Works Section
# ---------------------
st.markdown("""
## How It Works
1. **Input your desired player attributes** (e.g., elite shooter, strong defense).
2. **View AI-powered player matches** based on your criteria.
3. **Make smarter, data-driven draft decisions**.
""")

# ---------------------
# Footer
# ---------------------
st.markdown("""
---
Built for the next generation of stars.
""")
st.markdown("""
---
    <hr style="margin-top: 50px;"/>
    <div style='text-align: right; font-size: 0.9em; color: gray;'>
        © Developed by **Arya Mane** and **Ameya Phansalkar**
    </div>
""")
