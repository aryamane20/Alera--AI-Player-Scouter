# Alera – AI-powered Scouting Assistant

**Your Vision, Their Future.**

Alera is an AI-driven NBA scouting assistant that combines LLM intelligence with semantic search to help scouts and analysts discover high-potential basketball 
players through natural language queries. Powered by DeepSeek and FAISS, Alera transforms how player data is retrieved, analyzed, and visualized.

---

## App Link

https://nba-draft-scout-app-hns9k3gqyyx4gw6sqqfjop.streamlit.app/

---

## Key Features

- **LLM-Based Recommendations**  
  Generates personalized scouting insights using DeepSeek's instruction-tuned LLM via OpenAI-compatible API.

- **Dual FAISS Vector Search**  
  Two semantic vector databases (400+ players each for Draft & Midseason) allow real-time filtering by archetype, draft year, position, and more.

- **Interactive Streamlit Dashboard**  
  Clean UI to input queries, display best-fit recommendations, and visualize player stats side-by-side with embedded Tableau dashboards.

- **Smart Filtering**  
  Supports filters like "Top 5 Draft Picks", "3&D Wings", "2025 Bigs with Playmaking", etc., making the tool recruiter-friendly and precise.

---

## How It Works

1. **Embeddings Generation**  
   - Player bios, stats, and scouting summaries are embedded using `sentence-transformers`.
   - Stored in two separate FAISS indexes (Draft, Midseason).

2. **Query Input & Retrieval**  
   - User inputs a natural language scouting query.
   - Alera uses LangChain to semantically search the relevant FAISS index.

3. **LLM Recommendation**  
   - DeepSeek LLM processes the top retrieved candidates and generates a ranked list with pros/cons and fit explanations.

4. **Visualization**  
   - Recommendations + player Tableau dashboards are rendered via Streamlit for a complete scouting experience.

---

## Tech Stack

| Component           | Tool/Library                      |
|---------------------|-----------------------------------|
| LLM                 | DeepSeek (OpenAI-compatible API)  |
| Vector DB           | FAISS                             |
| Embeddings          | SentenceTransformers              |
| Frontend            | Streamlit                         |
| Visualization       | Tableau                           |
| RAG Framework       | LangChain                         |
| Data Format         | CSV, JSON                         |

---

## Getting Started

### Prerequisites
- Python 3.9+
- API key for DeepSeek (or compatible OpenAI LLM)
- Tableau Public or Tableau Server credentials (optional)
- Streamlit Cloud or local environment


## Future Enhancements

- **Model Evaluation Pipeline**  
  Implement quantitative metrics (e.g., F1 Score, BLEU, Recall@k) to benchmark recommendation quality.

- **Multi-Modal Scouting**  
  Integrate video highlight clips and physical metrics (wingspan, vertical leap) for deeper player evaluations.

- **User Authentication & Save Queries**  
  Enable scouts to log in, save recommendations, and track historical comparisons.

- **Expand to Other Sports**  
  Add support for other sports and leagues like soccer, NFL, WNBA, NHL etc.
