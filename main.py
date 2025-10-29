# import streamlit as st
# from src.rag import gemini_answer

# st.set_page_config(page_title="Department Chatbot", page_icon="🎓")

# def main():
#     st.title("🎓 AI Chatbot for Statistics Departmental Information")
#     user_input = st.chat_input("Ask your question:")
#     if user_input:
#         st.write( gemini_answer(user_input))

# # if __name__ == "__main__":
# main()

import streamlit as st
from src.rag import gemini_answer

st.set_page_config(page_title="Department Chatbot", page_icon="🎓")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "👋 Hi! I'm your Department Chatbot. How can I help you today?"}
    ]

st.title("🎓 AI Chatbot for Statistics Departmental Information")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# Chat input box
if prompt := st.chat_input("Ask me something about the Department..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = gemini_answer(prompt)
            st.write(response)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
