import os
from PyPDF2 import PdfReader
import docx
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_resume_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return None


def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return None


def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        return None


def train_model(X_train, y_train):
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    model = LogisticRegression()

    pipeline = Pipeline([
        ('tfidf', tfidf_vectorizer),
        ('clf', model)
    ])

    pipeline.fit(X_train, y_train)
    logger.info(f"Model trained successfully. Pipeline: {pipeline}")
    return pipeline


def save_pipeline(pipeline, file_path):
    try:
        joblib.dump(pipeline, file_path)
        logger.info(f"Pipeline saved to {file_path}.")
    except Exception as e:
        logger.error(f"Error saving pipeline: {e}")


def load_pipeline(file_path):
    try:
        pipeline = joblib.load(file_path)
        logger.info(f"Pipeline loaded from {file_path}. Type: {type(pipeline)}")
        return pipeline
    except Exception as e:
        logger.error(f"Error loading pipeline: {e}")
        return None


def predict_shortlisting(resumes, pipeline):
    try:
        if not isinstance(pipeline, Pipeline):
            logger.error(f"Loaded object is not a Pipeline. Type: {type(pipeline)}")
            return None

        predictions = pipeline.predict(resumes)
        return predictions
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return None
