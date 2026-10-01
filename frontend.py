# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="AI Mental Health Therapist",
    layout="wide"
)

st.title("🧠 SafeSpace – AI Mental Health Therapist")


# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Step2: User is able to ask question
user_input = st.chat_input("What's on your mind today?")

if user_input:

    # Append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        # Send request to FastAPI backend
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input},
            timeout=120
        )

        # Check if backend returned an error
        response.raise_for_status()

        # Convert backend response to JSON
        data = response.json()

        # Get response safely
        final_response = data.get(
            "response",
            "Sorry, I could not generate a response."
        )

        tool_called = data.get(
            "tool_called",
            "None"
        )

        # Display AI response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"{final_response}\n\nTool used: {tool_called}"
        })

    except requests.exceptions.ConnectionError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ Could not connect to the backend. Please make sure FastAPI is running on port 8000."
        })

    except requests.exceptions.Timeout:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ The AI is taking too long to respond. Please try again."
        })

    except requests.exceptions.HTTPError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"⚠️ Backend error: {response.status_code}\n\n{response.text}"
        })

    except ValueError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ The backend returned an invalid response."
        })

    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"⚠️ Something went wrong: {str(e)}"
        })


# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])