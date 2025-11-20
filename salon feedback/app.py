from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Google Sheets Setup
SHEET_ID = "1oPAMxJfvrpBFziJcxPr1yNT-4480Lh1w5fkROjc5DQA"   # fill this
RANGE_NAME = "Sheet1!A:F"    # columns A–F

def get_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    return sheet

@app.route("/")
def home():
    return render_template("star.html")

@app.route("/service", methods=["POST", "GET"])
def service_page():
    if request.method == "POST":
        rating = request.form.get("rating")
        return render_template("service.html", rating=rating)
    return redirect(url_for("rating"))


@app.route("/feedback", methods=["POST"])
def feedback_page():
    rating = request.form.get("rating")
    service = request.form.getlist("service")

    employee = request.form.get("employee")

    return render_template(
        "feedback.html",
        rating=rating,
        service=service,
        employee=employee
    )


@app.route("/submit", methods=["POST"])
def submit():
    rating = request.form.get("rating")
    service = request.form.get("service")
    employee = request.form.get("employee")
    feedback = request.form.get("feedback")
    name = request.form.get("name")

    # Prepare the row to insert
    row = [rating, service, employee, feedback, name]

    try:
        sheet = get_sheet()
        sheet.values().append(
            spreadsheetId=SHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body={"values": [row]}
        ).execute()

        return render_template("thankyou.html")

    except Exception as e:
        return f"Error: {e}"



if __name__ == "__main__":
    app.run(debug=True)
