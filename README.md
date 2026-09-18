VeriHire – Fake Job Posting Detector

VeriHire is a Streamlit-based job posting verification platform that helps users identify potential fraudulent job advertisements by analyzing job description text and available metadata.

The application combines text-based analysis with structured job-posting signals and presents the result through a professional verification dashboard.

Features

Single Job Verification

Enter job posting information manually.

Analyze job title, company information, description, requirements, benefits, and metadata.

Display a prediction and risk classification.

Batch CSV Evaluation

Upload a CSV file containing multiple job postings.

Evaluate several records in one workflow.

Review the generated results and download outputs when supported.

Model and Dataset Insights

View available dataset information.

Display model evaluation metrics.

Review charts and analysis results.

Preset Examples

Load sample high-risk, suspicious, and authentic job postings for demonstration and testing.

Professional Dashboard

VeriHire branding.

Verification summary section.

Risk indicators and confidence information.

Interactive visualizations where supported.

Technology Stack

Python

Streamlit

Pandas

NumPy

Scikit-learn

TF-IDF text vectorization

Logistic Regression

Plotly (for interactive charts, if enabled)

Project Structure

archive/
├── app.py
├── ml_engine.py
├── fake_job_postings.csv
├── model_cache.pkl
└── README.md

The exact files may vary depending on the current project implementation.

Installation

1. Clone or open the project

Open the project directory in VS Code or Antigravity.

cd C:\Users\agaly\Downloads\archive

2. Install the required packages

If a requirements.txt file is available:

python -m pip install -r requirements.txt

Otherwise, install the main dependencies:

python -m pip install streamlit pandas numpy scikit-learn plotly scipy

Run the Application

Use the following command from the project directory:

python -m streamlit run app.py

After starting the application, open the local URL shown in the terminal, usually:

http://localhost:8501

Application Workflow

Open the VeriHire application.

Select Verify Job from the navigation.

Enter or load job posting details.

Select the available verification options.

Click Run Risk Analysis & Verification.

Review the prediction, risk classification, confidence information, and detected signals.

Use Batch Analysis to evaluate multiple postings through a CSV file.

Open Model Insights to review dataset and evaluation information.

Machine Learning Approach

The project uses a text classification workflow based on:

Data Preparation

Read job posting data.

Handle available text and metadata fields.

Prepare the target labels.

Text Processing

Convert job-related text into numerical features using TF-IDF.

Combine text features with selected metadata features when available.

Model Training

Train a Logistic Regression classification model.

Use balanced class weights when configured.

Evaluate the model using a held-out test dataset.

Prediction

Generate a classification for a submitted job posting.

Display the available confidence or probability information.

Present the result as a verification aid.

Evaluation Metrics

The application may display metrics such as:

Accuracy

ROC-AUC

Precision

Recall

F1-score

Dataset record count

The values shown in the application depend on the currently trained model, dataset, and evaluation configuration.

Important Notes

The model output is an analytical aid and should not be treated as a guaranteed determination of fraud.

Users should independently verify company details, contact information, salary claims, payment requests, and official recruitment channels.

Model confidence should not automatically be interpreted as the exact probability that a job posting is fraudulent.

Keep the dataset and model files secure and avoid storing unnecessary personal information.

Troubleshooting

Streamlit command is not recognized

Run Streamlit through Python:

python -m streamlit run app.py

Package installation issue

Upgrade pip and try again:

python -m pip install --upgrade pip

Then install the required packages again.

Application error after a code change

Stop the running application using Ctrl + C.

Save the modified files.

Start the application again:

python -m streamlit run app.py

Future Enhancements

User authentication and role-based access

Company website and domain verification

Explainable prediction indicators

Improved batch reporting

Exportable verification reports

Model monitoring and periodic retraining

Accessibility and responsive UI improvements

Disclaimer

VeriHire is intended for educational, research, and decision-support purposes. Its predictions may contain errors. Always perform additional verification before applying for a job, sharing sensitive information, or making financial decisions.

Author

Developed as an academic machine learning and Streamlit application project.
