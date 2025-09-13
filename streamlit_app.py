
import streamlit as st
import requests
import json
from urllib.parse import urljoin

st.set_page_config(page_title="RAG Website QA", layout="centered")

st.title("RAG Website Q&A (with citations)")

# Inputs: API base + API key
api_base = st.sidebar.text_input("API Base URL", value="http://localhost:8000")
api_key = st.sidebar.text_input("X-API-KEY (API token)", type="password")

st.sidebar.markdown("**Index a URL**")
url_to_index = st.sidebar.text_input("URL to index")
if st.sidebar.button("Index URL"):
    if not api_key:
        st.sidebar.error("Set X-API-KEY in sidebar first")
    else:
        try:
            resp = requests.post(urljoin(api_base, "/api/v1/index"), json={"url":[url_to_index]}, headers={"X-API-KEY": api_key})
            st.sidebar.write(resp.json())
        except Exception as e:
            st.sidebar.error(str(e))

st.header("Ask a question")
messages = st.session_state.get("messages", [{"role":"assistant", "content":"Index some URLs first (use the sidebar) and then ask questions."}])
user_input = st.text_input("Your question", key="user_input")

if st.button("Ask"):
    if not api_key:
        st.error("Set X-API-KEY in the sidebar.")
    else:
        # prepare messages history (we send only the last user message suffice for RAG)
        payload = {"messages": [{"role":"user","content":user_input}]}
        try:
            resp = requests.post(urljoin(api_base, "/api/v1/chat"), json=payload, headers={"X-API-KEY": api_key})
            data = resp.json()
            # Response format: {"response":[{"answer":{"content": "...", "role":"assistant"}, "citation":[...]}]}
            ans = data["response"][0]["answer"]["content"]
            citations = data["response"][0].get("citation", [])
            st.markdown("### Answer")
            st.write(ans)
            if citations:
                st.markdown("### Citations")
                for c in citations:
                    st.write(f"- {c}")
        except Exception as e:
            st.error(str(e))
