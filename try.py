import streamlit as st
from supabase import create_client, Client
import time

# Supabase credentials
SUPABASE_URL = "https://qkvxxalkydceqdfribpt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrdnh4YWxreWRjZXFkZnJpYnB0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMwOTc2NzYsImV4cCI6MjA1ODY3MzY3Nn0.sz5QA6kcrSpPo9KEKOwvuL_sbDMYbAeH6oNbf-pXwes"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User authentication
st.title("Personal Chat App")
username = st.sidebar.selectbox("Select User", ["Furkan", "Sadqua"])
st.sidebar.write(f"Logged in as: {username}")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "message_input" not in st.session_state:
    st.session_state["message_input"] = ""

# Function to fetch messages
def fetch_messages():
    try:
        response = supabase.table("chat_messages").select("*").order("timestamp").execute()
        if response.data:
            st.session_state.messages = response.data  # Update session state
    except Exception as e:
        st.error(f"Error fetching messages: {e}")

# Function to send a message
def send_message():
    message = st.session_state["message_input"].strip()  # Get input and remove extra spaces
    if message:  # Ensure the message is not empty
        data = {"sender": username, "message": message, "timestamp": time.time()}
        try:
            response = supabase.table("chat_messages").insert(data).execute()
            if response.data:
                st.session_state["message_input"] = ""  # Clear input field
                fetch_messages()  # Fetch updated messages
                st.experimental_rerun()  # Refresh chat UI
        except Exception as e:
            st.error(f"Error sending message: {e}")

# Display chat messages
chat_box = st.empty()  # Create an empty container for chat messages
def update_chat():
    with chat_box.container():
        st.subheader("Chat")
        for msg in st.session_state.messages:
            if msg["sender"] == username:
                st.markdown(f"**You:** {msg['message']}")
            else:
                st.markdown(f"**{msg['sender']}:** {msg['message']}")

# Fetch messages initially
fetch_messages()
update_chat()

# Auto-refresh messages every second (without blocking user input)
while True:
    fetch_messages()
    update_chat()
    time.sleep(1)
    st.experimental_rerun()

# Message input and send button
st.text_input("Type a message", key="message_input")
st.button("Send", on_click=send_message)
