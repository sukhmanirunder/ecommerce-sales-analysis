import streamlit as st
import pandas as pd
from transformers import pipeline

# ---- Load Dataset ----
@st.cache_data
def load_data():
    df = pd.read_csv("indian_ecommerce2.csv")  # columns: City, Sales, Profit
    return df

df = load_data()

# ---- Precompute city-wise summary ----
city_summary = df.groupby('City').agg({'Sales':'sum', 'Profit':'sum'}).reset_index()

# ---- Context text for QA model ----
context = ""
for _, row in city_summary.iterrows():
    context += f"{row['City']} has total sales {row['Sales']:.2f} and total profit {row['Profit']:.2f}. "

# ---- Load QA Model ----
@st.cache_resource
def load_model():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa_model = load_model()

# ---- Streamlit UI ----
st.set_page_config(page_title="Smart E-commerce Chatbot", layout="wide")
st.title("🧠 Smart E-commerce Chatbot")

user_question = st.text_input("💬 Your Question:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Custom logic ----
def answer_query(question):
    q = question.lower()

    # 🟢 Handle max/min logic using pandas
    if "max" in q or "highest" in q:
        if "sales" in q:
            row = city_summary.loc[city_summary['Sales'].idxmax()]
            return f"{row['City']} has the highest sales: {row['Sales']:.2f}"
        if "profit" in q:
            row = city_summary.loc[city_summary['Profit'].idxmax()]
            return f"{row['City']} has the highest profit: {row['Profit']:.2f}"

    if "min" in q or "lowest" in q:
        if "sales" in q:
            row = city_summary.loc[city_summary['Sales'].idxmin()]
            return f"{row['City']} has the lowest sales: {row['Sales']:.2f}"
        if "profit" in q:
            row = city_summary.loc[city_summary['Profit'].idxmin()]
            return f"{row['City']} has the lowest profit: {row['Profit']:.2f}"

    # 🟡 Otherwise use QA model
    result = qa_model(question=question, context=context)
    return result['answer']

# ---- Button ----
if st.button("Ask"):
    if user_question.strip() != "":
        answer = answer_query(user_question)
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("Bot", answer))

# ---- Show Chat History ----
st.subheader("💭 Chat History")
for sender, msg in st.session_state.chat_history:
    st.write(f"**{sender}:** {msg}")
