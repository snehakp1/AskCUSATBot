import streamlit as st
from src.rag import gemini_answer

st.set_page_config(page_title="AskCUSATBot", page_icon="🎓")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "👋 Hello! I'm AskCUSATBot. How can I assist you today?"}
    ]

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

st.title("🎓 AskCUSATBot")

# Sidebar Section
with st.sidebar:

    st.header("🤖 AskCUSATBot")

    # Compact Chatbot Description Box
    st.markdown(
        """
        <div style="
            border: 1px solid #D3D3D3; 
            border-radius: 8px; 
            padding: 12px; 
            background-color: #f9f9f9;
            font-size: 14px;
            text-align: justify;
        ">
        <b>AskCUSATBot</b> is an intelligent assistant for the Department of Statistics, CUSAT, providing quick and reliable information about academic programs, admissions, faculty, facilities, events, and updates making departmental communication seamless and user-friendly.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("🔑 Gemini API Access")

    # API key input field
    api_key_input = st.text_input(
        "Enter API Key:",
        type="password",
        placeholder="Paste your API key here..."
    )

    # Info text
    st.markdown(
        "<p style='text-align: center; font-size: 14px; color: grey;'>"
        "The key is temporary,not saved."
        "</p>",
        unsafe_allow_html=True
    )


    if st.button("Enter"):
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            st.success("✅ API key saved successfully for this session!")
        else:
            st.warning("⚠️ Please enter a valid API key before saving.")

    # Clear chat option
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "🧹 Chat history cleared. How can I assist you next?"}
        ]
        st.success("Chat history cleared!")


    
    # Footer credit line
    st.markdown(
        """
        <div style="text-align: center; font-size: 14px; color: grey;">
        Developed by <b>Sneha K P</b><br>
        Department of Statistics, <b>CUSAT</b><br>
        
        </div>
        """,
        unsafe_allow_html=True
    )

# Main Chat Section
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input Section
if prompt := st.chat_input("Ask me something about the Department..."):
    if not st.session_state["api_key"]:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar and click 'Enter' before asking a question.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get model response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = gemini_answer(prompt, st.session_state["api_key"])
                st.write(response)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
