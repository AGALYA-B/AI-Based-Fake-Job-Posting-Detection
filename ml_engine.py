"""
VeriHire - ML Engine & Risk Signal Evaluation
"""
import os
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.pipeline import FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
import pickle

DATASET_PATH = 'fake_job_postings.csv'
MODEL_CACHE_PATH = 'model_cache.pkl'

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_combined_features(df):
    title = df['title'].fillna('').apply(preprocess_text)
    comp = df['company_profile'].fillna('').apply(preprocess_text)
    desc = df['description'].fillna('').apply(preprocess_text)
    req = df['requirements'].fillna('').apply(preprocess_text)
    ben = df['benefits'].fillna('').apply(preprocess_text)
    ind = df['industry'].fillna('').apply(preprocess_text)
    func = df['function'].fillna('').apply(preprocess_text)
    
    combined_text = title + " " + comp + " " + desc + " " + req + " " + ben + " " + ind + " " + func
    return combined_text

def build_and_train_model():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset {DATASET_PATH} not found.")
    
    df = pd.read_csv(DATASET_PATH)
    
    # Combined text feature
    X_text = create_combined_features(df)
    
    # Metadata features
    has_logo = df['has_company_logo'].fillna(0).astype(int).values.reshape(-1, 1)
    has_quest = df['has_questions'].fillna(0).astype(int).values.reshape(-1, 1)
    telecommuting = df['telecommuting'].fillna(0).astype(int).values.reshape(-1, 1)
    missing_comp = df['company_profile'].isna().astype(int).values.reshape(-1, 1)
    missing_sal = df['salary_range'].isna().astype(int).values.reshape(-1, 1)
    missing_req = df['requirements'].isna().astype(int).values.reshape(-1, 1)
    
    meta_features = np.hstack([has_logo, has_quest, telecommuting, missing_comp, missing_sal, missing_req])
    
    y = df['fraudulent'].values
    
    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(max_features=4000, ngram_range=(1, 2), stop_words='english')
    X_text_tfidf = tfidf.fit_transform(X_text)
    
    # Combine TF-IDF and Metadata
    from scipy.sparse import hstack
    X_combined = hstack([X_text_tfidf, meta_features]).tocsr()
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Logistic Regression with balanced weights
    model = LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    roc_auc = roc_auc_score(y_test, y_prob)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
    cm = confusion_matrix(y_test, y_pred)
    
    # Feature coefficients for fraud indicators
    feature_names = list(tfidf.get_feature_names_out()) + [
        'has_company_logo (meta)', 'has_questions (meta)', 'telecommuting (meta)',
        'missing_company_profile (meta)', 'missing_salary_range (meta)', 'missing_requirements (meta)'
    ]
    
    coefs = model.coef_[0]
    top_fraud_indices = np.argsort(coefs)[::-1][:20]
    top_legit_indices = np.argsort(coefs)[:20]
    
    top_fraud_features = [(feature_names[i], float(coefs[i])) for i in top_fraud_indices]
    top_legit_features = [(feature_names[i], float(coefs[i])) for i in top_legit_indices]
    
    metrics = {
        'roc_auc': float(roc_auc),
        'accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1': float(f1),
        'confusion_matrix': cm.tolist(),
        'dataset_count': len(df),
        'fraud_count': int(df['fraudulent'].sum()),
        'legit_count': int((df['fraudulent'] == 0).sum()),
        'fraud_rate': float(df['fraudulent'].mean()),
        'top_fraud_features': top_fraud_features,
        'top_legit_features': top_legit_features
    }
    
    model_artifact = {
        'tfidf': tfidf,
        'model': model,
        'metrics': metrics,
        'feature_names': feature_names
    }
    
    return model_artifact

def get_model():
    """Load cached model artifact or build on first run."""
    if os.path.exists(MODEL_CACHE_PATH):
        try:
            with open(MODEL_CACHE_PATH, 'rb') as f:
                return pickle.load(f)
        except Exception:
            pass
    
    artifact = build_and_train_model()
    try:
        with open(MODEL_CACHE_PATH, 'wb') as f:
            pickle.dump(artifact, f)
    except Exception:
        pass
    return artifact

def analyze_job_posting(job_data, model_artifact):
    """
    Evaluates a single job posting dictionary.
    Returns detailed fraud analysis, risk score, and specific detected signals.
    """
    tfidf = model_artifact['tfidf']
    model = model_artifact['model']
    
    # Format inputs
    title = str(job_data.get('title', ''))
    comp_prof = str(job_data.get('company_profile', ''))
    desc = str(job_data.get('description', ''))
    req = str(job_data.get('requirements', ''))
    ben = str(job_data.get('benefits', ''))
    ind = str(job_data.get('industry', ''))
    func = str(job_data.get('function', ''))
    salary = str(job_data.get('salary_range', ''))
    
    has_logo = 1 if job_data.get('has_company_logo', 0) in [1, True, '1', 'Yes'] else 0
    has_quest = 1 if job_data.get('has_questions', 0) in [1, True, '1', 'Yes'] else 0
    telecommuting = 1 if job_data.get('telecommuting', 0) in [1, True, '1', 'Yes'] else 0
    
    missing_comp = 1 if not comp_prof.strip() or comp_prof.strip().lower() in ['none', 'n/a', 'nan'] else 0
    missing_sal = 1 if not salary.strip() or salary.strip().lower() in ['none', 'n/a', 'nan', 'unspecified'] else 0
    missing_req = 1 if not req.strip() or req.strip().lower() in ['none', 'n/a', 'nan'] else 0
    
    combined_raw = f"{title} {comp_prof} {desc} {req} {ben} {ind} {func}"
    processed_text = preprocess_text(combined_raw)
    
    # Vectorize
    text_vec = tfidf.transform([processed_text])
    meta_vec = np.array([[has_logo, has_quest, telecommuting, missing_comp, missing_sal, missing_req]])
    
    from scipy.sparse import hstack
    x_input = hstack([text_vec, meta_vec]).tocsr()
    
    prob = float(model.predict_proba(x_input)[0, 1])
    
    # Categorize Risk
    if prob >= 0.55:
        risk_level = "High Risk"
        classification = "Potential Scam Posting"
    elif prob >= 0.25:
        risk_level = "Medium Risk"
        classification = "Needs Careful Review"
    else:
        risk_level = "Low Risk"
        classification = "Legitimate Posting"
        
    confidence = round((prob if prob >= 0.5 else 1 - prob) * 100, 1)
    fraud_pct = round(prob * 100, 1)
    
    # Extract Detected Risk Signals
    detected_signals = []
    positive_signals = []
    
    if missing_comp:
        detected_signals.append({
            "type": "warning",
            "title": "Missing Company Profile",
            "detail": "No background information or verified company history was provided in the posting."
        })
    else:
        positive_signals.append("Detailed company profile provided.")
        
    if not has_logo:
        detected_signals.append({
            "type": "warning",
            "title": "Missing Company Logo",
            "detail": "No official employer brand logo associated with this posting."
        })
    else:
        positive_signals.append("Verified employer branding logo present.")
        
    if not has_quest:
        detected_signals.append({
            "type": "info",
            "title": "No Screening Questions",
            "detail": "Application lacks standard applicant screening or qualification questions."
        })
    else:
        positive_signals.append("Includes structured applicant screening questions.")
        
    if missing_sal:
        detected_signals.append({
            "type": "info",
            "title": "Unspecified Salary Compensation",
            "detail": "Salary range is omitted or unverified."
        })
        
    # High risk text pattern matches
    text_lower = processed_text.lower()
    high_risk_keywords = [
        ("wire transfer", "References payment transfers or wire transactions."),
        ("cashier check", "Mentions handling cashier checks or financial deposits."),
        ("data entry from home", "Promotes generic high-pay work-from-home data entry."),
        ("no experience required", "Offers disproportionately high compensation for zero requirements."),
        ("telegram", "Directs candidates to informal messaging apps like Telegram."),
        ("whatsapp", "Directs candidates to informal messaging apps like WhatsApp."),
        ("earn $", "Promotes aggressive income promises or daily pay rates."),
        ("unlimited earning", "Uses sales-heavy language promising extreme compensation.")
    ]
    
    for kw, kw_desc in high_risk_keywords:
        if kw in text_lower:
            detected_signals.append({
                "type": "danger",
                "title": f"Flagged Phrase: '{kw.title()}'",
                "detail": kw_desc
            })
            
    # Risk summary explanation
    if prob >= 0.55:
        explanation = (
            f"This posting shows a high probability ({fraud_pct}%) of being fraudulent. "
            f"Multiple risk indicators were detected, including structural omissions and text patterns "
            f"frequently found in deceptive recruitment ads."
        )
    elif prob >= 0.25:
        explanation = (
            f"This posting exhibits moderate risk signals ({fraud_pct}% fraud probability). "
            f"While it may be legitimate, we recommend verifying company contact details and domain authenticity before sharing sensitive personal data."
        )
    else:
        explanation = (
            f"This posting appears legitimate with low risk ({fraud_pct}% fraud probability). "
            f"Structural metadata and text signals align with standard authentic job announcements."
        )
        
    return {
        "fraud_probability": prob,
        "fraud_pct": fraud_pct,
        "risk_level": risk_level,
        "classification": classification,
        "confidence": confidence,
        "detected_signals": detected_signals,
        "positive_signals": positive_signals,
        "explanation": explanation
    }

def evaluate_batch(df, model_artifact):
    """
    Evaluates a pandas DataFrame of job postings.
    """
    results = []
    for idx, row in df.iterrows():
        job_dict = row.to_dict()
        analysis = analyze_job_posting(job_dict, model_artifact)
        results.append({
            "Job Title": row.get('title', 'N/A'),
            "Company Profile": "Present" if pd.notna(row.get('company_profile')) and str(row.get('company_profile')).strip() else "Missing",
            "Fraud Probability": f"{analysis['fraud_pct']}%",
            "Risk Level": analysis['risk_level'],
            "Classification": analysis['classification'],
            "Primary Signal": analysis['detected_signals'][0]['title'] if analysis['detected_signals'] else "None Detected",
            "_raw_prob": analysis['fraud_probability']
        })
    res_df = pd.DataFrame(results)
    
    total = len(res_df)
    high_risk = (res_df['Risk Level'] == 'High Risk').sum()
    med_risk = (res_df['Risk Level'] == 'Medium Risk').sum()
    low_risk = (res_df['Risk Level'] == 'Low Risk').sum()
    
    batch_summary = {
        "total_jobs": total,
        "high_risk_count": int(high_risk),
        "med_risk_count": int(med_risk),
        "low_risk_count": int(low_risk),
        "high_risk_pct": round((high_risk / total * 100) if total > 0 else 0, 1)
    }
    
    return res_df, batch_summary
