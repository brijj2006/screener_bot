# Resume Shortlisting Application

This application uses Machine Learning to train a model for shortlisting resumes based on their content. The application is built using Flask and follows the MVC architecture.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Logging Configuration](#logging-configuration)
- [Workflow](#workflow)
- [Routes](#routes)
- [Forms](#forms)

## Project Structure

your_project/
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── forms.py
│ ├── utils.py
│ └── models.py
│
├── config/
│ ├── init.py
│ └── config.py
│
├── logs/
│ └── app.log
│
├── templates/
│ ├── index.html
│ ├── train.html
│ └── predict.html
│
├── static/
│ └── (your static files)
│
├── run.py
└── logging_config.py

bash
Copy code

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_project.git
   cd your_project
Create and activate a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory of the project and add the following variables:

env
Copy code
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=uploads
Set up the uploads directory:

bash
Copy code
mkdir uploads
Running the Application
Run the Flask application:

bash
Copy code
python run.py
Access the application in your browser:

Go to http://127.0.0.1:5000 in your web browser.

Logging Configuration
The logging configuration is defined in logging_config.py. Logs are saved to logs/app.log and printed to the console. You can adjust the logging level and format as needed.

Workflow
Train Model:

Go to the Train Model page.
Upload a PDF or DOCX file and provide a label (0 or 1).
Click the Submit button to train the model. The model will be saved to models/trained_pipeline.pkl.
Predict Shortlisting:

Go to the Predict Shortlisting page.
Upload a PDF or DOCX file.
Click the Submit button to get the prediction (Shortlisted or Not Shortlisted).
Routes
Home Route (/): Displays the home page with links to train and predict functionalities.
Train Route (/train): Handles the training of the model with uploaded resumes.
Predict Route (/predict): Handles the prediction of shortlisting based on uploaded resumes.
Forms
TrainForm:

python
Copy code
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class TrainForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    label = IntegerField('Label (0 or 1)', validators=[InputRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField('Submit')
PredictForm:

python
Copy code
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

class PredictForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    submit = SubmitField('Submit')
Code Overview
run.py
This file contains the entry point for running the Flask application.

app/__init__.py
This file initializes the Flask application and sets up the application context.

app/routes.py
This file defines the routes and their corresponding request handlers.

app/forms.py
This file contains the form classes for training and prediction.

app/utils.py
This file contains utility functions for reading resume files, training the model, saving/loading the pipeline, and predicting shortlisting.

config/config.py
This file contains the configuration settings