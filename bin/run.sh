# docker run -it -p 8000:8501 semsearch:latest streamlit run sem_search.py
docker run -it -p 8000:8501 semsearch:latest -v `pwd`/models:/project/models streamlit run sem_search.py