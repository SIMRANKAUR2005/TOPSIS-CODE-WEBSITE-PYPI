# TOPSIS Web Service

A complete end-to-end implementation of the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method, built as:

• A command-line tool  
• A Python package uploaded to PyPI  
• A web service with file upload and email delivery  

This project covers all three parts of the assignment.

---

## What is TOPSIS?

TOPSIS is a multi-criteria decision-making technique that:
- Evaluates multiple alternatives
- Uses multiple criteria with weights and impacts
- Ranks options based on closeness to the ideal solution

---

## Project Features

### Part-I: CLI Implementation
- Command-line program for TOPSIS
- Input via CSV or Excel
- Validates:
  - Correct number of arguments
  - Numeric criteria
  - Weights and impacts count
  - Valid impacts (+ or -)
- Outputs TOPSIS score and rank

### Part-II: PyPI Package
- Packaged as a Python module
- Installable via pip
- Runnable from command line
- Includes full user manual

### Part-III: Web Service
- File upload via browser
- Weights and impacts input
- Email validation
- Sends result file through email
- Flask backend + HTML frontend

---

## Technologies Used

- Python  
- Flask  
- Pandas & NumPy  
- SMTP for Email  
- HTML  
- GitHub  
- PyPI  

---


## How to Run Web Service

### 1. Install Dependencies

pip install flask pandas numpy openpyxl

### 2. Run Server

python app.py

### 3. Open Browser

http://127.0.0.1:5000/

---

## Web Form Inputs

- Upload CSV or Excel file  
- Enter weights (comma separated)  
- Enter impacts (comma separated + or -)  
- Enter valid email  
- Submit  

Result will be sent as an email attachment.

---

## Validations Implemented

- Email format check  
- Weights and impacts count must match  
- Impacts must be + or -  
- Comma separated inputs  
- Minimum 3 columns  
- Numeric criteria columns  

---

## Output

The result file contains:
- Original data  
- TOPSIS Score  
- Rank  

---

## Author

Simran Kaur  
Assignment: TOPSIS – CLI, Package & Web Service  

---

## License

This project is open-source and created for academic learning purposes.
