# streamlit_scout_app.py

import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re
import urllib.parse

# Load DeepSeek client
client = OpenAI(
    api_key="sk-492256da50af4813b2d96c6be1909918",  # Replace with your key
    base_url="https://api.deepseek.com/v1"
)

# Load player data
with open("/Users/aryamane/Downloads/player_chunks_with_draft_year_in_chunk.json", "r", encoding="utf-8") as f:
    player_data = json.load(f)

# Load FAISS index
index = faiss.read_index("/Users/aryamane/Downloads/player_index.faiss")  # Make sure this file exists

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

Based on the query, suggest 1–2 ideal players and explain why.
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

    # Heuristic: extract capitalized names from the recommendation
    retrieved_names = [p["name"] for p in retrieved_players]
    recommended_names = [name for name in retrieved_names if name in full_response]


    return full_response, recommended_names[:2]  # return top 2 names


# Streamlit UI
st.set_page_config(page_title="NBA Draft Player Scouting", layout="wide")
st.title("NBA Draft Player Scouter")

query = st.text_input("Enter your scouting query:", "Stretch 4 who can shoot 3s and rebound (2025 draft class)")

if st.button("Find Players"):
    formatted_query = format_query_for_embedding(query)
    retrieved = retrieve_players(formatted_query, embedding_model, index, player_data)
    response, recommended_names = recommend_players_with_deepseek(query, retrieved)

    st.subheader("AI Recommendation:")
    st.markdown(response)

    st.markdown("Player Stats for Recommended Players")

    tableau_base_url = "https://public.tableau.com/views/Player_Stats_17453432818390/playerstats"

    for name in recommended_names:
        st.markdown(f"{name}")

        encoded_name = urllib.parse.quote(name)
        tableau_url = f"{tableau_base_url}?:language=en&PlayerParam={encoded_name}"

        st.markdown("#### 📊 Stat Overview")
        st.write("🔗 Tableau URL:", tableau_url)
        st.components.v1.iframe(tableau_url, height=600, width=1000)

        st.markdown("---")
