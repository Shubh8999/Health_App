import streamlit as st
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import re
import string
import nltk
import streamlit as st
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import re
import string
import nltk
from datetime import datetime
import sqlite3
import hashlib

st.set_page_config(page_title="Mental Health Chatbot",
                       page_icon=":guardsman:", layout="wide")

st.markdown("""

    <style>
    ul > li:first-child {
  display: none;
}

    </style>

    """, unsafe_allow_html=True)

logout_link = '<a href="/#my_anchor" target="_self" style="font-size: 18px; color:black;padding:10px;border:1px solid white;text-decoration:none;background-color:white;border-radius:5px;border:none;box-shadow:1px 1px 6px red;position: absolute; top: -50px; right: -10px;">Logout</a>'
st.markdown(logout_link, unsafe_allow_html=True)

# Load the mental health chatbot dataset
df = pd.read_csv("../Data/mental_health_data.csv")

# Connect to the database
conn = sqlite3.connect('../Data/1_mental_health_chatbot.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              user_input TEXT,
              bot_response TEXT,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(user_id) REFERENCES users(id))''')

# Preprocess the data


def preprocess_text(text):
    # Remove html tags
    text = re.sub('<.*?>', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert text to lowercase
    text = text.lower()
    # Split text into words
    words = text.split()
    # Remove stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word not in stopwords]
    # Lemmatize words
    lemmatizer = nltk.stem.WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words


# Preprocess the questions and answers
questions = df['questionText'].apply(preprocess_text)
answers = df['answerText'].apply(preprocess_text)
all_text = pd.concat([questions, answers], ignore_index=True)

# Train a Word2Vec model on the preprocessed text
model = Word2Vec(sentences=all_text, vector_size=100,
                 window=5, min_count=1, workers=4, sg=1)

# Define a function to generate a response to a user input


def generate_response(input_text):
    input_words = preprocess_text(input_text)
    # Find similar words in the Word2Vec model
    similar_words = []
    for word in input_words:
        try:
            similar_words.extend(model.wv.most_similar(word, topn=10))
        except KeyError:
            pass
    # Remove duplicates and sort by similarity score
    similar_words = sorted(list(set(similar_words)),
                           key=lambda x: x[1], reverse=True)
    # Select the most similar word and return its corresponding answer
    for similar_word in similar_words:
        index = answers[answers.apply(
            lambda x: similar_word[0] in x)].index.tolist()
        if index:
            return df.iloc[index[0]]['answerText']
    # Check if the input question itself is a match
    index = answers[answers.apply(lambda x: input_text in x)].index.tolist()
    if index:
        return df.iloc[index[0]]['answerText']
    # If no answer is found, return a default response
    return "I'm sorry, I don't understand. Can you please rephrase your question?"

# Define the app function


def chatbot():
    # st.set_page_config(page_title="Mental Health Chatbot", page_icon=":guardsman:", layout="wide")
    # st.write("# Mental Health Chatbot")
    # st.write("Welcome! I'm here to help you with your mental health concerns. Just type in your question or concern and I'll do my best to provide you with an appropriate response.")

    # # Set up the Streamlit app
    # user_input = st.text_input("You:", value="", key="input")
    # if st.button("Send"):
    #     if user_input.lower() in ['hello', 'hi', 'hey']:
    #         response = "Hello! How can I help you today?"
    #     elif user_input.lower() in ['bye', 'goodbye']:
    #         response = "Goodbye! Take care."
    #     else:
    #         response = generate_response(user_input)
    #     st.text_area("Bot:", value=response, key="response")
    #     conversation_history = st.session_state.get("conversation_history", [])
    #     conversation_history.append({"user_input": user_input, "response": response})
    #     st.session_state.conversation_history = conversation_history[-5:]

    # # Display conversation history
    # st.subheader("Conversation History")
    # conversation_history = st.session_state.get("conversation_history", [])
    # for i, conversation in enumerate(conversation_history):
    #     st.write(f"{i+1}. You: {conversation['user_input']}")
    #     st.write(f"Bot: {conversation['response']}")
    #     st.write("---")

    st.session_state.authenticated = True
    params = st.experimental_get_query_params()
    param1 = params["user_id"][0] if "user_id" in params else None
    st.session_state.user_id = param1

    st.write("# Mental Health Chatbot")
    st.write("Welcome! I'm here to help you with your mental health concerns. Just type in your question or concern and I'll do my best to provide you with an appropriate response.")

    # Set up the Streamlit app
#     conversation_history = st.session_state.get("conversation_history", [])
#     conversation_history.reverse()
#     with st.container():
#         for conversation in conversation_history:
#             if conversation["speaker"] == "bot":
#                 st.write(f"Bot: {conversation['response']}")
#             else:
#                 st.write(f"You: {conversation['user_input']}")

#     col1, col2 = st.columns([1, 2])
#     with col1:
#         user_input = st.text_input("You:", value="", key="input")
#     with col2:
#         st.write("")
#         if st.button("Send"):
#             if user_input.lower() in ['hello', 'hi', 'hey']:
#                 response = "Hello! How can I help you today?"
#             elif user_input.lower() in ['bye', 'goodbye']:
#                 response = "Goodbye! Take care."
#             else:
#                 response = generate_response(user_input)
#             st.write(f"Bot: {response}")
#             conversation_history = st.session_state.get("conversation_history", [])
#             conversation_history.append({"speaker": "you", "user_input": user_input})
#             conversation_history.append({"speaker": "bot", "response": response})
#             st.session_state.conversation_history = conversation_history[-5:]

# # Display conversation history
#     st.subheader("Conversation History")
#     conversation_history = st.session_state.get("conversation_history", [])
#     for i, conversation in enumerate(conversation_history):
#         if "user_input" in conversation:
#             st.write(f"{i+1}. You: {conversation['user_input']}")
#         if "response" in conversation:
#             st.write(f"Bot: {conversation['response']}")
#         st.write("---")

    if "user_id" in st.session_state:
        user_input = st.text_input("You:", value="", key="input")
        if st.button("Send"):
            response = generate_response(user_input)
            st.text_area("Bot:", value=response, key="response")
            insert_conversation_history(
                st.session_state.user_id, user_input, response)
            conversation_history = st.session_state.get(
                "conversation_history", [])
            conversation_history.append(
                {"user_input": user_input, "response": response})
            st.session_state.conversation_history = conversation_history[-5:]

            # Display conversation history
            st.subheader("Conversation History")
            c.execute("SELECT user_input, bot_response FROM conversation_history WHERE user_id=? ORDER BY id DESC",
                      (st.session_state.user_id,))
            conversation_history = c.fetchall()
            if not conversation_history:
                st.write("No conversation history found.")
            else:
                for i, conversation in enumerate(conversation_history):
                    st.write(f"{i+1}. You: {conversation[0]}")
                    st.write(f"Bot: {conversation[1]}")
                    st.write("---")

             # Display conversation history
        else:
            st.subheader("Conversation History")
            c.execute("SELECT user_input, bot_response FROM conversation_history WHERE user_id=? ORDER BY id DESC",
                      (st.session_state.user_id,))
            conversation_history = c.fetchall()
            if not conversation_history:
                st.write("No conversation history found.")
            else:
                for i, conversation in enumerate(conversation_history):
                    st.write(f"{i+1}. You: {conversation[0]}")
                    st.write(f"Bot: {conversation[1]}")
                    st.write("---")



def insert_conversation_history(user_id, user_input, bot_response):
    c.execute("INSERT INTO conversation_history (user_id, user_input, bot_response) VALUES (?, ?, ?)",
              (user_id, user_input, bot_response))
    conn.commit()


# Run the app
if __name__ == "__main__":
    chatbot()