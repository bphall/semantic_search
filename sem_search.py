from sem_functions import semantic_search
import streamlit as st

st.title('SEMANTIC SEARCH')
st.write("TYPE IN THE WORDS FOR A PARAGRAPH FROM A CLASSIC NOVEL YOU'D LIKE TO FIND WITH"
         " AS MUCH DETAIL AS YOU CAN PROVIDE")


user_input = st.text_input("(or just random words you'd like to find scenes for)")


st.write("Potential Novels to Draw From: Alice in Wonderland, War and Peace, Anna Karenina, Ulysses, "
         "Frankenstein, Little Women, Les Misérables, Oliver Twist, A Tale of Two Cities, Treasure Island, "
         "Tom Sawyer, Metamorphosis, Heart of Darkness, Emma, Dracula, Jane Eyre, Siddhartha, Plato's Republic, "
         "and many more...")
st.write("Examples:")
st.write(" 'all happy families are alike, unhappy families are different in their own way' ")
st.write(" 'anna karenina' ")
st.write(" 'cheshire cat' ")
st.write(" 'monster created from death back to life' ")
st.write(" 'people with red hair' ")
st.write(" 'people with blonde hair' ")
st.write(" 'pirates searching for treasure' ")
st.write(" 'one morning gregor samsa woke up in his bed and found himself to be a giant insect' ")

semantic_search(user_input, include_quoted_novel=True)
