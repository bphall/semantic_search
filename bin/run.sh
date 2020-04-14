# docker run -it -p 8000:8501 semsearch:latest streamlit run sem_search.py
docker run -it -p 8000:8888 -e PORT=8888 -v `pwd`/models:/project/models semsearch:latest