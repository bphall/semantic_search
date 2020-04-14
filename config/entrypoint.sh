#! bin/bash
mkdir -p ~/.streamlit
touch ~/.streamlit/config.toml
echo "[server]" > ~/.streamlit/config.toml
echo "port=${PORT}" >> ~/.streamlit/config.toml

streamlit run sem_search.py
