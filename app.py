from flask import Flask, render_template, request, redirect, url_for, flash
import os
from app.forms import UploadForm
from app.utils import read_resume_file, train_model, save_pipeline, load_pipeline, predict_shortlisting

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train', methods=['GET', 'POST'])
def train():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename.endswith(('.pdf', '.docx')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            resume_text = read_resume_file(file_path)
            if resume_text:
                label = form.label.data
                X_train = [resume_text]
                y_train = [label]
                if len(set(y_train)) < 2:
                    flash('Training data must contain samples for both classes (e.g., 0 and 1).')
                    return redirect(url_for('train'))
                model, vectorizer = train_model(X_train, y_train)
                save_pipeline(model, vectorizer, 'models/trained_pipeline.pkl')
                flash('Training complete.')
                return redirect(url_for('home'))
            else:
                flash('Error reading file.')
                return redirect(url_for('train'))
        else:
            flash('Error: Please upload a PDF or DOCX file.')
            return redirect(url_for('train'))
    return render_template('train.html', form=form)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename.endswith(('.pdf', '.docx')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            resume_text = read_resume_file(file_path)
            if resume_text:
                model, vectorizer = load_pipeline('models/trained_pipeline.pkl')
                predictions = predict_shortlisting([resume_text], model, vectorizer)
                return f'Prediction: {"Shortlisted" if predictions[0] == 1 else "Not Shortlisted"}'
            else:
                flash('Error reading file.')
                return redirect(url_for('predict'))
        else:
            flash('Error: Please upload a PDF or DOCX file.')
            return redirect(url_for('predict'))
    return render_template('predict.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
