import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re
import urllib.parse


# ---------------------
# 🔧 Setup
# ---------------------

st.set_page_config(
    page_title="Alera – NBA Scouting Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Custom font CSS (same as landing page)
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


# Load the key

api_key = st.secrets["OPENAI_API_KEY"]

# Hardcode DeepSeek base URL
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)
print("Loaded key:", api_key[:8], "...")  # ✅ Should show the correct prefix

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index based on player type
def load_index(player_type):
    if player_type == "Draft":
        return faiss.read_index("faiss_draft_index/index.faiss")
    else:
        return faiss.read_index("faiss_midseason_index/index.faiss")


# Load player chunks
def load_chunks(player_type):
    if player_type == "Draft":
        with open("player_chunks_with_draft_year_in_chunk.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open("midtrade_player_chunks_cleaned.json", "r", encoding="utf-8") as f:
            return json.load(f)

# Retrieve top-k similar players
def retrieve_players(query, model, index, player_chunks, k=10):
    embedding = model.encode([query])
    D, I = index.search(np.array(embedding), k)
    return [player_chunks[i] for i in I[0]]

# Add draft year prefix to query if needed
def format_query_for_embedding(query):
    match = re.search(r"(19|20)\d{2}", query)
    if match:
        year = match.group(0)
        return f"{year} draft class: {query}"
    return query

# Use DeepSeek to recommend players
def recommend_players_with_deepseek(query, retrieved_players):
    if not retrieved_players:
        return "No matching players found.", []

    context = "\n\n".join([p["chunk"] for p in retrieved_players])
    match = re.search(r"(19|20)\d{2}", query)
    draft_year = match.group(0) if match else None

    system_msg = (
        f"You are an expert NBA scout assistant helping identify ideal draft picks. "
        f"Only recommend players from the {draft_year} draft class."
        if draft_year else
        "You are an expert NBA scout assistant helping identify ideal draft picks."
    )

    prompt = f"""
Scouting Query: {query}

Here are some potential players:
{context}

Based on the query, suggest 1–2 ideal players and explain why. Do not mention other players.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    full_response = response.choices[0].message.content
    retrieved_names = [p["name"] for p in retrieved_players]
    recommended_names = [name for name in retrieved_names if name in full_response]

    return full_response, recommended_names[:2]

# ---------------------
# 🎨 Streamlit UI (Minimal OpenAI Style)
# ---------------------
st.markdown("<h1 style='text-align: center;'>Alera</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Your Vision. Their Future.</h3>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    player_type = st.radio("What type of player are you scouting?", ["Draft", "Midseason"], horizontal=True)

    draft_range = None
    if player_type == "Draft":
        draft_range = st.selectbox("Filter by Draft Range", ["All", "Top 5", "Lottery", "1st Round", "2nd Round", "Undrafted"])

    query = st.text_area("Describe your ideal player:", height=150, placeholder="e.g. A two-way wing who can defend and shoot threes")
# Add custom style for Find Players button
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 0.75em 2.5em;
        border-radius: 30px;
        font-size: 1.1em;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
        transform: scale(1.03);
        align:center;
    }
    </style>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    find_clicked = st.button("🔍 Find Players")
if find_clicked:    
    try:
            index = load_index(player_type)
            player_data = load_chunks(player_type)

            formatted_query = format_query_for_embedding(query)
            retrieved = retrieve_players(formatted_query, embedding_model, index, player_data, k=10)

            # Apply draft-specific filters
            if player_type == "Draft":
                if draft_range and draft_range != "All":
                    retrieved = [
                        p for p in retrieved
                        if draft_range.lower() == p.get("draft_range", "").strip().lower()
                    ]
                retrieved = [
                    p for p in retrieved
                    if str(p.get("draft_year", "")).strip() == "2025"
                ]

            response, recommended_names = recommend_players_with_deepseek(query, retrieved)

            st.markdown("### 📢 AI Recommendation")
            st.markdown(response)

            if recommended_names:
                st.markdown("### Player Dashboards")
                if player_type == "Draft":
                    tableau_base_url = "https://public.tableau.com/views/Player_Stats_17453432818390/playerstats"
                else:
                    tableau_base_url = "https://public.tableau.com/views/Player_Stats_17453432818390/playerstats"


                for name in recommended_names:
                    encoded_name = urllib.parse.quote(name)
                    url = f"{tableau_base_url}?:language=en&PlayerParam={encoded_name}"
                    st.markdown(f"**{name}**")
                    st.components.v1.iframe(url, height=500)
                    st.markdown("---")
    except Exception as e:
            st.error(f"Error: {e}")
