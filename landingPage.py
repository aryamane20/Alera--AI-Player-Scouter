import streamlit as st
from PIL import Image
 
# Injecting subtle basketball texture background, floating logo animation, and fancy ball swish animation
st.markdown(
    """
<style>
    body {
        background-image: url('https://www.transparenttextures.com/patterns/basketball.png');
        background-size: 400px 400px;
        background-repeat: repeat;
    }
    .main {
        background: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    /* Floating Animation for Logo */
    @keyframes float {
        0% { transform: translatey(0px); }
        50% { transform: translatey(-10px); }
        100% { transform: translatey(0px); }
    }
    .floating-logo {
        animation: float 3s ease-in-out infinite;
    }
    /* Fancy Ball Swish Animation */
    @keyframes ball-move {
        0% { transform: translate(0, 0); }
        30% { transform: translate(50px, -80px); }
        60% { transform: translate(120px, -150px); }
        100% { transform: translate(180px, 0px); }
    }
    .ball {
        position: absolute;
        top: 150px;
        left: 20px;
        font-size: 40px;
        display: none;
    }
    .hoop {
        position: absolute;
        top: 150px;
        left: 200px;
        font-size: 50px;
    }
    .animate-ball {
        display: block;
        animation: ball-move 2s ease forwards;
    }
</style>
    """,
    unsafe_allow_html=True
)
 
# Ball and Hoop Elements
st.markdown("""
<div style='position:relative;height:200px;'>
<div id='ball' class='ball'>🏀</div>
<div class='hoop'>🏀️⛳️</div>
</div>
""", unsafe_allow_html=True)
 
# Alera Logo
logo = Image.open("Logo.png")  # Make sure you have uploaded the logo file
st.markdown("""<div class='floating-logo'>""", unsafe_allow_html=True)
st.image(logo, width=80)
st.markdown("""</div>""", unsafe_allow_html=True)
 
# Hero Section
st.markdown("""
# **Alera – NBA Draft Player Scouter**
### _"Your Vision, Their Future."_
""")
 
# Animated Get Started Button
st.markdown("""
<button id='start-btn' style='font-size:18px;padding:10px 20px;border-radius:10px;border:none;background-color:#0052cc;color:white;cursor:pointer;'>Get Started</button>
<script>
const btn = document.getElementById('start-btn');
btn.onclick = function() {
    document.getElementById('ball').classList.add('animate-ball');
    setTimeout(function() {
        window.location.hash = '#features';
    }, 2000);
}
</script>
""", unsafe_allow_html=True)
 
# Spacer
st.write("\n" * 3)
 
# About Section
st.markdown("""
## About Alera
Alera empowers scouts, coaches, and managers by providing AI-powered player recommendations. 
Our system intelligently blends advanced player stats with qualitative scouting insights to help you find the perfect draft pick.
""")
 
# Features Section
st.markdown("""
## Features <a id='features'></a>
- **AI-Powered Player Scouting**
- **Deep Analytics and Player Comparisons**
- **Custom Attribute Search**
- **Real-Time Tableau Dashboards**
- **Seamless User Experience**
""")
 
# How it Works Section
st.markdown("""
## How It Works
1. **Input your desired player attributes** (e.g., elite shooter, strong defense).
2. **View AI-powered player matches** based on your criteria.
3. **Make smarter, data-driven draft decisions**.
""")
 
# Footer
st.markdown("""
---
Built for the next generation of stars.
 
""")

# Button to Go to Scouting App
if st.button("Go to Scouting App"):
    st.switch_page("nba_scout_app.py")