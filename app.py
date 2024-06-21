import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from app.forms import UploadForm
from app.utils import read_resume_file, train_model, save_pipeline, load_pipeline, predict_shortlisting

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# In-memory storage for resumes and labels
resumes = []
labels = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/train', methods=['GET', 'POST'])
def train():
    form = UploadForm(label=0)
    if request.method == 'POST':
        logger.info('Form data: %s', request.form)
        if form.validate_on_submit():
            logger.info('Form validated successfully')
            file = form.file.data
            label = form.label.data

            if file and file.filename.endswith(('.pdf', '.docx')):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                resume_text = read_resume_file(file_path)
                if resume_text:
                    resumes.append(resume_text)
                    labels.append(label)

                    if len(set(labels)) < 2:
                        flash('Need more samples for both classes (0 and 1) before training.')
                        logger.info('Insufficient samples for training')
                        return redirect(url_for('train'))

                    model, vectorizer = train_model(resumes, labels)
                    save_pipeline(model, 'models/trained_pipeline.pkl')

                    resumes.clear()
                    labels.clear()

                    flash('Training complete.')
                    logger.info('Training completed successfully')
                    return redirect(url_for('home'))
                else:
                    flash('Error reading file.')
                    logger.error('Error reading file: %s', file.filename)
                    return redirect(url_for('train'))
            else:
                flash('Error: Please upload a PDF or DOCX file.')
                logger.error('Invalid file type: %s', file.filename)
                return redirect(url_for('train'))
        else:
            logger.info('Form validation failed')
            logger.info('Form errors: %s', form.errors)
    return render_template('train.html', form=form)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = UploadForm()
    prediction = None
    if request.method == 'POST':
        logger.info('Form data: %s', request.form)
        if form.validate_on_submit():
            logger.info('Form validated successfully')
            file = form.file.data
            if file and file.filename.endswith(('.pdf', '.docx')):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                resume_text = read_resume_file(file_path)
                if resume_text:
                    model, vectorizer = load_pipeline('models/trained_pipeline.pkl')
                    predictions = predict_shortlisting([resume_text], model, vectorizer)
                    prediction = 'Shortlisted' if predictions[0] == 1 else 'Not Shortlisted'
                    logger.info('Prediction made: %s', prediction)
                else:
                    flash('Error reading file.')
                    logger.error('Error reading file: %s', file.filename)
                    return redirect(url_for('predict'))
            else:
                flash('Error: Please upload a PDF or DOCX file.')
                logger.error('Invalid file type: %s', file.filename)
                return redirect(url_for('predict'))
        else:
            logger.info('Form validation failed')
            logger.info('Form errors: %s', form.errors)
    return render_template('predict.html', form=form, prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
