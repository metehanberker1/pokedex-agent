"""Streamlit web interface for the Pokédex agent."""
import streamlit as st
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import chat, create_chat_session, add_user_message, add_assistant_message
from src.db import DB_PATH
from src.etl import load_all

if not DB_PATH.exists():
    st.info("Running ETL to populate the database. This may take a few minutes on first deploy...")
    load_all(force=True)

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
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background-color: #23272f;
                color: #f5f6fa;
            }
            .sidebar-section {
                margin-bottom: 2rem;
            }
            .sidebar-header {
                font-size: 1.3rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
                color: #61dafb;
            }
            .sidebar-subheader {
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 1.2rem;
                margin-bottom: 0.3rem;
                color: #f5c518;
            }
            .sidebar-divider {
                border-top: 1px solid #444857;
                margin: 1.2rem 0 1.2rem 0;
            }
            ul.sidebar-list {
                margin-left: 1.2rem;
                margin-bottom: 0.5rem;
            }
            li.sidebar-list-item {
                margin-bottom: 0.3rem;
            }
            /* Fix Clear Chat button text color */
            section[data-testid="stSidebar"] button {
                color: #23272f !important;
                font-weight: 600;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<span class="sidebar-header">ℹ️ About</span>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subheader">Capabilities:</div>', unsafe_allow_html=True)
        st.markdown(
            '<ul class="sidebar-list">'
            '<li class="sidebar-list-item">🧩 Team building and analysis</li>'
            '<li class="sidebar-list-item">⚡ Type effectiveness and coverage</li>'
            '<li class="sidebar-list-item">📊 Stat analysis and comparisons</li>'
            '<li class="sidebar-list-item">🌎 Habitat and location information</li>'
            '<li class="sidebar-list-item">🔗 Evolution chains and requirements</li>'
            '<li class="sidebar-list-item">✨ Ability analysis</li>'
            '<li class="sidebar-list-item">🏆 Legendary and mythical Pokémon identification</li>'
            '</ul>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subheader">Example Questions:</div>', unsafe_allow_html=True)
        st.markdown(
            '<ul class="sidebar-list">'
            '<li class="sidebar-list-item">"What\'s the best team of 6 Pokémon for competitive battling?"</li>'
            '<li class="sidebar-list-item">"Which Pokémon have the highest attack stat?"</li>'
            '<li class="sidebar-list-item">"What types are super effective against Water types?"</li>'
            '</ul>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
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