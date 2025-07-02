# 📝 Extractive Text Summarization

An interactive Streamlit web app for performing extractive summarization and keyword extraction on raw text or uploaded files (.txt, .pdf).

Built with spaCy, pdfplumber, and Streamlit, this tool lets you distill large chunks of information into concise summaries.


## 🚀 Features

- 🔍 **Text Summarization**: Uses frequency-based scoring to extract the most relevant sentences.

- 🧠 **Keyword Extraction**: Identifies and lists the most frequent, meaningful words.

- 📁 **File Support**: Works with both .txt and .pdf documents.

- 📥 **Downloadable Summary**: Save your output as a text file.


## 🛠️ Tech Stack

- **Streamlit** – for the web interface

- **spaCy** – for natural language processing

- **pdfplumber** – to read PDFs


## 🚀 Setup Instructions

1. Clone this repo:
```bash
git clone https://github.com/suraj-maktala/Extractive-Text-Summarization.git
cd Extractive-Text-Summarization
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Start the app:
```bash
streamlit run Main.py
```


## 🧠 How It Works (Quick Peek)

- It scores sentences by how important their words are (based on frequency).

- Then it picks the top sentences to keep, depending on the ratio you set.

- For keywords, it simply grabs the most frequent, meaningful words (ignoring common ones like “the” or “is”).
