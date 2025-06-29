"""Streamlit web interface for the Pokédex agent."""
import streamlit as st
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import chat, create_chat_session, add_user_message, add_assistant_message
from src.db import DB_PATH


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Pokédex Conversational Agent",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 Pokédex Conversational Agent")
    st.markdown("Your advanced Pokémon research assistant with comprehensive data from PokéAPI!")
    
    # Check if database exists
    if not DB_PATH.exists():
        st.error("❌ Database not found!")
        st.info("Please run the ETL first:")
        st.code("python -m src.etl")
        st.stop()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = create_chat_session()
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Capabilities:**
        - Team building and analysis
        - Type effectiveness and coverage
        - Stat analysis and comparisons
        - Habitat and location information
        - Evolution chains and requirements
        - Ability analysis
        - Legendary and mythical Pokémon identification
        
        **Example Questions:**
        - "What's the best team of 6 Pokémon for competitive battling?"
        - "Which Pokémon have the highest attack stat?"
        - "What types are super effective against Water types?"
        """)
        
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = create_chat_session()
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(message["content"])
                # Show tool calls if present
                if "tool_calls" in message:
                    for tool_call in message["tool_calls"]:
                        st.info(f"🔧 Called: {tool_call['function']['name']}")
        elif message["role"] == "tool":
            with st.expander(f"🔧 Tool Result"):
                st.json(json.loads(message["content"]))
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Pokémon!"):
        # Add user message
        add_user_message(st.session_state.messages, prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.write(response)
        
        # Add assistant response
        add_assistant_message(st.session_state.messages, response)


if __name__ == "__main__":
    main() 