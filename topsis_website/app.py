import os
import re
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "topsis_secret_key"

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# SMTP Configuration (REPLACE THESE WITH YOUR DETAILS)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
GMAIL_USER = "skaur8_be23@thapar.edu"  # Your Gmail address
GMAIL_APP_PASS = "sifd dhvt ynov rwqt" # Your 16-digit App Password

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(recipient_email, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Analysis Results'
    msg['From'] = GMAIL_USER
    msg['To'] = recipient_email
    msg.set_content("Hello,\n\nPlease find the attached TOPSIS analysis results for your recent submission.\n\nRegards,\nTOPSIS Web Service")

    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

def run_topsis(input_path, weights, impacts, output_path):
    # Load data
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    # Validation: At least 3 columns
    if len(df.columns) < 3:
        raise ValueError("File must have at least 3 columns (Object Name + 2 or more Criteria).")

    # Validation: Columns 2nd onwards must be numeric
    data = df.iloc[:, 1:].values
    if not np.issubdtype(data.dtype, np.number):
        raise ValueError("All criteria columns (from 2nd column onwards) must be numeric.")

    # Validation: Weights and Impacts count
    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        raise ValueError(f"Number of weights ({len(weights)}) and impacts ({len(impacts)}) must match the number of criteria ({data.shape[1]}).")

    # Step 1: Normalize the matrix
    # sqrt(sum(x^2)) for each column
    norm_factors = np.sqrt(np.sum(np.square(data), axis=0))
    normalized_matrix = data / norm_factors

    # Step 2: Calculate weighted normalized matrix
    weighted_matrix = normalized_matrix * weights

    # Step 3: Determine Ideal Best and Ideal Worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        col = weighted_matrix[:, i]
        if impacts[i] == '+':
            ideal_best.append(np.max(col))
            ideal_worst.append(np.min(col))
        else:
            ideal_best.append(np.min(col))
            ideal_worst.append(np.max(col))

    # Step 4: Calculate Euclidean distances from ideal best and worst
    s_best = np.sqrt(np.sum(np.square(weighted_matrix - ideal_best), axis=1))
    s_worst = np.sqrt(np.sum(np.square(weighted_matrix - ideal_worst), axis=1))

    # Step 5: Calculate Performance Score (P-Score)
    p_scores = s_worst / (s_best + s_worst)

    # Step 6: Rank
    df['Topsis Score'] = p_scores
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

    df.to_csv(output_path, index=False)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        weights_str = request.form.get('weights')
        impacts_str = request.form.get('impacts')
        file = request.files.get('file')

        # 1. Validate Email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.")
            return redirect(request.url)

        # 2. Validate File
        if not file or not allowed_file(file.filename):
            flash("Please upload a valid CSV or Excel file.")
            return redirect(request.url)

        try:
            # 3. Parse and Validate Weights/Impacts
            weights = [float(w.strip()) for w in weights_str.split(',')]
            impacts = [i.strip() for i in impacts_str.split(',')]

            if any(i not in ['+', '-'] for i in impacts):
                flash("Impacts must only contain '+' or '-'.")
                return redirect(request.url)

            # Save uploaded file
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)

            # Process TOPSIS
            output_filename = f"result_{filename.split('.')[0]}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            run_topsis(input_path, weights, impacts, output_path)

            # Send Email
            if send_email(email, output_path):
                flash(f"Success! The TOPSIS results have been sent to {email}.")
            else:
                flash("TOPSIS calculated, but failed to send email. Check SMTP settings.")

        except ValueError as ve:
            flash(f"Input Error: {str(ve)}")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}")

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)