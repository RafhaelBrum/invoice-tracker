# Invoice Tracker - Auto Peças Brum

This is an invoice tracking system developed in Python with Google Sheets integration, designed to manage payments for a store, but can also be used for personal purposes. It allows you to manually register invoices via the terminal, automatically generates installments, and saves them to a Google Sheets spreadsheet.

## Features

- Register invoices via terminal
- Automatically generates monthly installments
- Auto-export to Google Sheets
- Unique ID per installment
- Prevents duplicate entries based on "Document Number"
- Script to mark specific installment as paid

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/RafhaelBrum/invoice-tracker.git
cd invoice-tracker
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Connecting to Google Sheets

### 1. Create a project in Google Cloud:
- Go to: https://console.cloud.google.com/
- Create a new project
- Enable the following APIs:
  - Google Sheets API
  - Google Drive API

### 2. Create a service account credential:
- Go to "APIs & Services > Credentials"
- Create a new credential > Service account
- Download the `.json` file and save it as:
  ```
  config/credentials.json
  ```

### 3. Share the spreadsheet with the service account email
- Copy the service account email from the JSON file
- Share your spreadsheet with that email (Editor access)

---

## Usage

### Register new invoices
```bash
python register_bills.py
```
The script will prompt you for:
- Document Number (must be unique)
- Supplier
- Description
- Installment amount
- Number of installments
- First due date (DD/MM/YYYY)
- Payment method
- Observations (optional)

The installments will be auto-generated and sent to the Google Sheets document.

### Mark an installment as paid
```bash
python mark_as_paid.py
```
The script will prompt you for:
- Document Number
- Installment number (e.g. 2 for 02/06)

It will update the payment date and status to "Paid" in Google Sheets.

---

## Contributions
Suggestions, improvements and bug fixes are welcome! Feel free to open an issue or a pull request.

---

## License
MIT License.