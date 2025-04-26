# streamlit_scout_app.py

import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re
import urllib.parse
from PIL import Image

# Load DeepSeek client
client = OpenAI(
    api_key="sk-492256da50af4813b2d96c6be1909918",  # Replace with your key
    base_url="https://api.deepseek.com/v1"
)

# Load player data
with open("player_chunks_with_draft_year_in_chunk.json", "r", encoding="utf-8") as f:
    player_data = json.load(f)

# Load FAISS index
index = faiss.read_index("player_index.faiss")  # Make sure this file exists

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to retrieve players
def retrieve_players(query, model, index, player_chunks, k=5):
    embedding = model.encode([query])
    D, I = index.search(np.array(embedding), k)
    return [player_chunks[i] for i in I[0]]

# Smart query formatting
def format_query_for_embedding(query):
    match = re.search(r"(19|20)\d{2}", query)
    if match:
        year = match.group(0)
        return f"{year} draft class: {query}"
    return query

# LLM-based recommendation using DeepSeek
def recommend_players_with_deepseek(query, retrieved_players):
    if not retrieved_players:
        return "No matching players found.", [], {}

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

Based on the query, suggest 3-4 ideal players.
For each player, give a short paragraph explaining why they are a good fit.
After listing all players, give a final recommendation for the best overall fit.
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

    # Remove any extra suggestions like "Would you like deeper stats..."
    full_response = full_response.split("Would you like deeper stats")[0].strip()

    # Heuristic: extract player names
    retrieved_names = [p["name"] for p in retrieved_players]
    recommended_names = [name for name in retrieved_names if name in full_response]
    recommended_names = list(dict.fromkeys(recommended_names))  # Remove duplicates

    # Extract individual player recommendations
    detailed_recommendations = {}
    for name in recommended_names:
        pattern = rf"{name}(.*?)(\n\n|$)"
        match = re.search(pattern, full_response, re.DOTALL)
        if match:
            detailed_recommendations[name] = match.group(1).strip()
        else:
            detailed_recommendations[name] = "No detailed recommendation found."

        # Extract final summary
    final_summary = "No final best fit recommendation was provided."

    if "Final Best Fit Recommendation" in full_response:
        parts = full_response.split("Final Best Fit Recommendation")
        if len(parts) > 1:
            final_summary = parts[-1].strip()
        else:
            final_summary = "No final best fit recommendation was provided."


# --- Streamlit UI Setup ---
st.set_page_config(page_title="Alera – Player Scouter", layout="wide", page_icon="🏀")

# Display Logo + App Title
logo = Image.open("Logo.png")
st.image(logo, width=60)
st.markdown("## **Alera – NBA Draft Player Scouter**")

# --- User Input ---
query = st.text_input("🔍 Enter your scouting query:", "Stretch 4 who can shoot 3s and rebound (2025 draft class)")

# Initialize session state to track button press
if "button_pressed" not in st.session_state:
    st.session_state.button_pressed = False

# Handle Button Press
if st.button("🔎 Find Players"):
    st.session_state.button_pressed = True

# Only run this AFTER button was clicked
if st.session_state.button_pressed:
    with st.spinner('Finding the best players... 🏀'):
        formatted_query = format_query_for_embedding(query)
        retrieved = retrieve_players(formatted_query, embedding_model, index, player_data)
        final_summary, recommended_names, detailed_recommendations = recommend_players_with_deepseek(query, retrieved)

    st.success("Recommendations ready!")

    tableau_base_url = "https://public.tableau.com/views/Player_Stats_17453432818390/playerstats"

    # --- Recommended Players ---
    st.markdown("## **Recommended Players**")

    for name in recommended_names:
        st.markdown(f"### 👤 **{name}**")

        # 1. Recommendation (Why)
        st.markdown(f"#### 🏀 **Why {name}?**")
        st.markdown(detailed_recommendations.get(name, "No detailed reason available."))

        # 2. Tableau Dashboard
        encoded_name = urllib.parse.quote(name)
        tableau_url = f"{tableau_base_url}?:embed=yes&:showVizHome=no&PlayerParam={encoded_name}"
        st.components.v1.iframe(tableau_url, height=850, width=1200)

        st.markdown("---")

    # 🏆 Final Best Fit
    st.markdown("## 🏆 **Final Best Fit Recommendation**")
    st.markdown(final_summary)
