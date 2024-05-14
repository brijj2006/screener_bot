import os
import joblib
import PyPDF2
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def read_resume_file(file_path):
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path)
    return None


def read_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])


def train_model(X, y):
    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X)
    model = LogisticRegression()
    model.fit(X_vect, y)
    return model, vectorizer


def save_pipeline(model, vectorizer, file_path):
    joblib.dump({'model': model, 'vectorizer': vectorizer}, file_path)


def load_pipeline(file_path):
    pipeline = joblib.load(file_path)
    return pipeline['model'], pipeline['vectorizer']


def predict_shortlisting(resumes, model, vectorizer):
    X_vect = vectorizer.transform(resumes)
    return model.predict(X_vect)
