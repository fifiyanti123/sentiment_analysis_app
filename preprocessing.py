import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string

# Download resources jika belum tersedia
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Fungsi preprocessing teks
def preprocess_text(text):
    if not isinstance(text, str) or text.strip() == "":
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Hilangkan karakter khusus dan angka
    text = re.sub(r"[^\w\s]", "", text)  # Hapus tanda baca
    text = re.sub(r"\d+", "", text)      # Hapus angka

    # 3. Ganti kata-kata informal atau tidak baku
    informal_words = {
        "ga": "tidak",
        "gak": "tidak",
        "nggak": "tidak",
        "bgt": "banget",
        "bgtt": "banget",
        "bkn": "bukan",
        "bgtu": "begitu",
        "aja": "saja",
        "jd": "jadi",
        "dong": "",
        "yah": "",
        "loh": "",
        "dr": "dari",
        "tp": "tapi",
        "pake": "pakai",
        "sm": "sama",
    }

    for word, replacement in informal_words.items():
        text = re.sub(rf'\b{word}\b', replacement, text)

    # 4. Tokenisasi
    tokens = word_tokenize(text)

    # 5. Stopword removal (tapi tetap mempertahankan kata sentimen penting seperti "not", "no")
    stop_words = set(stopwords.words("indonesian") + stopwords.words("english")) - {"not", "no", "tidak"}
    tokens = [word for word in tokens if word not in stop_words]

    # 6. Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # 7. Gabungkan kembali menjadi string
    return " ".join(tokens)

# Contoh penggunaan
if __name__ == "__main__":
    comments = [
        "Ga ngerti cara pake aplikasinya!",
        "Aplikasi ini bener2 bagus bgt!",
        "Aplikasi ini ga guna sm sekali.",
        "Kok jd ribet sih pakenya? 😒",
    ]

    for comment in comments:
        print(f"Original: {comment}")
        print(f"Processed: {preprocess_text(comment)}")
        print()
