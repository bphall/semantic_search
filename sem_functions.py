from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import pickle
import streamlit as st
import requests
import os


nltk.download('stopwords')
stop_set = set(stopwords.words('english'))


if not os.path.exists('models/fourth_model.pkl'):
    response = requests.get('https://braytonhall-public.s3.amazonaws.com/semanticsearchmodels/fourth_model.pkl', stream=True)
    with open('models/fourth_model.pkl', 'wb') as f:
        f.write(response.content)


if not os.path.exists('models/paragraphs_dataframe'):
    response = requests.get('https://braytonhall-public.s3.amazonaws.com/semanticsearchmodels/paragraphs_dataframe2', stream=True)
    with open('models/paragraphs_dataframe', 'wb') as f:
        f.write(response.content)


paragraphs = pickle.load(open("models/paragraphs_dataframe", "rb"))
third_model = pickle.load(open('models/fourth_model.pkl', 'rb'))


def model_tokenizer(input_data):
    tokenizer = RegexpTokenizer(r'\w+')
    lowered = input_data.lower()
    tokens = tokenizer.tokenize(lowered)
    return tokens


def para_from_id(tag, rank, cosine):
    start = tag - 1
    end = tag + 2
    name = paragraphs.loc[tag].title
    book_range = paragraphs[paragraphs.title == f'{name}'].index
    location = tag - book_range[0]
    length = book_range[-1] - book_range[0]
    percent = round((location / length) * 100, 2)
    st.write('NOVEL: ' + name, '\n')
    st.write('LOCATION IN NOVEL: AT PARAGRAPH {0} out of {1}, {2}% into the book'.format(location, length, percent), '\n')
    for i in range(start, end):
        if i < tag:
            try:
                st.write('...' + paragraphs.chunks[i][-200:])
            except:
                st.write('Beginning of Novel')
        if i > tag:
            try:
                st.write(paragraphs.chunks[i][:200] + '...')
            except:
                st.write('End of Novel')
        if i == tag:
            st.write('**************************************************')
            st.write('                          {0} MOST SIMILAR PARAGRAPH, COSINE_SIMILARITY: {1}               '.format(
                rank, cosine), '\n')
            st.write(paragraphs.chunks[i])
            st.write('**************************************************')


def semantic_search(type_text_here, include_quoted_novel=True):
    # Tokenizes the input text, vectorizes it, and finds the 300 most similar tagged paragraphs.
    if len(type_text_here) < 3:
        return None
    tokens = model_tokenizer(type_text_here)
    vector = third_model.infer_vector(tokens)
    top300 = third_model.docvecs.most_similar([vector], topn=300)
    final_tags = []
    final_tags_other_novels = []
    quoted_novel = paragraphs.loc[int(top300[0][0])].title

    # These need to be removed later from the whole DataFrame, but in the meantime this solution works
    rid = "La Navigation Aérienne L'aviation Et La Direction Des Aérostats Dans Les Temps Anciens Et Modernes"
    rid2 = "The Decameron of Giovanni Boccaccio"
    rid3 = "The MemoirsCorrespondenceAnd MiscellaniesFrom The Papers Of Thomas Jefferson"
    rid4 = 'The Kama Sutra of Vatsyayana'
    rid5 = 'Leviathan'
    rid6 = "Divine ComedyLongfellow's TranslationHell"
    rid7 = "Also sprach ZarathustraEnglish"
    rid8 = "Geschlecht und CharakterEnglish"
    rid9 = 'Index of Project Gutenberg Works on Black History'

    # The following two for-loops create final_tags and final_tags_other novels, which are used to
    # filter out results based on whether the user wants to include the quoted novel.
    #
    # The numbers (> 20 here) filters out search results with 20 or fewer words, since the model
    # is biased to think that short input strings are similar to short paragraphs, which only exist
    # at the beginning and end of novels, based on how they were broken up originally.
    #
    # The rid statements are a short term solution for removing two Italian and French novels,
    # and the 'letter' and 'chapter' statements are used to remove most books' appendices.

    for i in top300:
        if ((len(model_tokenizer(paragraphs.chunks[int(i[0])])) > 60) &
                (paragraphs.loc[int(i[0])].title != rid) &
                (paragraphs.loc[int(i[0])].title != rid2) &
                (paragraphs.loc[int(i[0])].title != rid3) &
                (paragraphs.loc[int(i[0])].title != rid4) &
                (paragraphs.loc[int(i[0])].title != rid5) &
                (paragraphs.loc[int(i[0])].title != rid6) &
                (paragraphs.loc[int(i[0])].title != rid7) &
                (paragraphs.loc[int(i[0])].title != rid8) &
                (paragraphs.loc[int(i[0])].title != rid9) &
                (model_tokenizer(paragraphs.chunks[int(i[0])]).count('letter') < 10) &
                (model_tokenizer(paragraphs.chunks[int(i[0])]).count('chapter') < 10) &
                ('Gutenberg' not in paragraphs.chunks[int(i[0])])):
            final_tags.append(i)

    for i in top300:
        if ((len(model_tokenizer(paragraphs.chunks[int(i[0])])) > 60) &
                (paragraphs.loc[int(i[0])].title != rid) &
                (paragraphs.loc[int(i[0])].title != rid2) &
                (paragraphs.loc[int(i[0])].title != rid3) &
                (paragraphs.loc[int(i[0])].title != rid4) &
                (paragraphs.loc[int(i[0])].title != rid5) &
                (paragraphs.loc[int(i[0])].title != rid6) &
                (paragraphs.loc[int(i[0])].title != rid7) &
                (paragraphs.loc[int(i[0])].title != rid8) &
                (paragraphs.loc[int(i[0])].title != rid9) &
                (paragraphs.loc[int(i[0])].title != quoted_novel) &
                (model_tokenizer(paragraphs.chunks[int(i[0])]).count('letter') < 10) &
                (model_tokenizer(paragraphs.chunks[int(i[0])]).count('chapter') < 10) &
                ('Gutenberg' not in paragraphs.chunks[int(i[0])])):
            final_tags_other_novels.append(i)

    rank = ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH']
    index = 0
    # The following two for-loops simply run the semantic search with or without the possibly-quoted novel,
    # since otherwise the results will be dominated by paragraphs within the same novel.

    if include_quoted_novel == True:
        st.write(
            '                                  SEARCH RESULTS (INCLUDING THE QUOTED NOVEL)                             ',
            '\n')
        for i in final_tags[:5]:
            st.write('______________________________________________________________________________________')
            st.write(index + 1)
            rank_i = rank[index]
            cosine_i = round(i[1], 4)
            tag_i = int(i[0])
            para_from_id(tag_i, rank_i, cosine_i)
            index += 1
            st.write('\n')

    if include_quoted_novel == False:
        st.write(
            '                                  SEARCH RESULTS (*NOT* INCLUDING THE QUOTED NOVEL)                             ',
            '\n')
        for i in final_tags_other_novels[:5]:
            st.write('______________________________________________________________________________________')
            st.write(index + 1)
            rank_i = rank[index]
            cosine_i = round(i[1], 4)
            tag_i = int(i[0])
            para_from_id(tag_i, rank_i, cosine_i)
            index += 1
            st.write('\n')

