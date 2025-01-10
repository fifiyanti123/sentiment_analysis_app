import streamlit as st
import joblib
import numpy as np
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Load model and vectorizer
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Preprocessing functions
def preprocess_informal_text(text):
    informal_words = {
        "ngga": "tidak",
        "gak": "tidak",
        "ga": "tidak",
        "bagus": "baik",
        "jelek": "buruk",
        "bgt": "banget",
    }
    words = text.split()
    words = [informal_words.get(word, word) for word in words]
    return " ".join(words)

def preprocess_text(text):
    if not isinstance(text, str) or text.strip() == "":
        return ""
    
    text = text.lower()
    text = preprocess_informal_text(text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words("english")) - {"not", "no"}
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Streamlit app
st.title("Aplikasi Analisis Sentimen Komentar YouTube Mengenai chat gpt")
st.write("Masukkan komentar di bawah ini untuk menganalisis sentimen.")

comment = st.text_area("Komentar:", "")

if st.button("Analisis Sentimen"):
    if comment.strip() != "":
        preprocessed_comment = preprocess_text(comment)
        vectorized_comment = vectorizer.transform([preprocessed_comment])
        probabilities = model.predict_proba(vectorized_comment)[0]
        sentiment_label = ["negative", "neutral", "positive"][np.argmax(probabilities)]
        
        st.write(f"**Sentimen:** {sentiment_label.capitalize()}")
        st.write("**Probabilitas:**")
        st.write(f"Negatif: {probabilities[0]:.2f}")
        st.write(f"Netral: {probabilities[1]:.2f}")
        st.write(f"Positif: {probabilities[2]:.2f}")
    else:
        st.write("Harap masukkan komentar.")
