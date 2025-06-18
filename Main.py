import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from collections import Counter
import pdfplumber


# Utility Functions
def summarize_text(text, ratio):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1

    max_frequency = max(word_frequencies.values())
    word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}

    sentence_scores = {sent: sum(word_frequencies.get(word.text.lower(), 0) for word in sent)
                       for sent in doc.sents}

    select_length = int(len(list(doc.sents)) * ratio)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    return ' '.join([sent.text for sent in summary])


def keyword(text, num_keywords=5):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    word_freq = Counter(words)
    sorted_keywords = word_freq.most_common(num_keywords)
    return [f"{word}: {freq}" for word, freq in sorted_keywords]


def extract_text_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Append text from each page
    return text


# App Logic
def generate_summary(input_text, ratio, file_name=None):
    if not input_text.strip():
        st.warning("Input text is empty or insufficient for summarization.")
        return
    try:
        summary = summarize_text(input_text, ratio)
        if summary.strip():
            st.subheader("Summary:")
            st.write(summary)
            if file_name:
                st.download_button(label=f"Download {file_name}_summary.txt",
                                   data=summary.encode("utf-8"),
                                   file_name=f"{file_name}_summary.txt",
                                   mime='text/plain')
        else:
            st.warning("The generated summary is empty. Try increasing the text or ratio.")
    except Exception as e:
        st.error(f"Error: {e}")


def generate_keywords(input_text, num_keywords=5):
    if not input_text.strip():
        st.warning("Input text is empty.")
        return
    try:
        keywords = keyword(input_text, num_keywords)
        st.subheader("Keywords:")
        for idx, kw in enumerate(keywords, 1):
            st.write(f"{idx}. {kw}")
    except Exception as e:
        st.error(f"Error: {e}")


# Streamlit App
def app():
    st.title("Text Summarization")
    option = st.radio("Select an option:", ("Help", "Summarize Text", "Keyword Finder", "File Summary (.txt)", "File Summary (.pdf)"))

    if option == "Help":
        st.subheader("Help Guide")
        st.markdown("""
        ### Summarize Text
        1. Enter text in the input box.
        2. Select summary percentage.
        3. Click "Generate Summary".

        ### Keyword Finder
        1. Enter text in the input box.
        2. Click "Generate Keywords".

        ### File Summary
        1. Upload a `.txt` or `.pdf` file.
        2. Select summary percentage.
        3. Click "Generate Summary".
        """)

    elif option == "Summarize Text":
        input_text = st.text_area("Enter text to summarize", height=200)
        summary_ratio = st.slider("Select summary percentage", 1, 100) / 100
        if st.button("Generate Summary"):
            generate_summary(input_text, summary_ratio)

    elif option == "Keyword Finder":
        input_text = st.text_area("Enter text to find keywords", height=200)
        if st.button("Generate Keywords"):
            generate_keywords(input_text)

    elif option in {"File Summary (.txt)", "File Summary (.pdf)"}:
        file_type = "txt" if ".txt" in option else "pdf"
        uploaded_file = st.file_uploader(f"Upload a {file_type} file", type=[file_type])
        summary_ratio = st.slider("Select summary percentage", 1, 100) / 100

        if uploaded_file and st.button("Generate File Summary"):
            try:
                text_content = extract_text_pdf(uploaded_file) if file_type == "pdf" else uploaded_file.read().decode("utf-8")
                generate_summary(text_content, summary_ratio, file_name=uploaded_file.name.rsplit('.', 1)[0])
            except Exception as e:
                st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    app()
