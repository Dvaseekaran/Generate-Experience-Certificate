from flask import Flask, render_template, request, send_file
from jinja2 import Template
from weasyprint import HTML
import os
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Get data from form
        name = request.form["name"]
        role = request.form["role"]
        joining_year = request.form["joining_year"]
        relieving_year = request.form["relieving_year"]
        gender = request.form["gender"]
        date = datetime.today().strftime('%d %B %Y')

        data = {
            "name": name,
            "role": role,
            "joining_year": joining_year,
            "relieving_year": relieving_year,
            "gender": gender,
            "date": date
        }

        # Optional: Save to JSON
        with open("employee_data.json", "w") as f:
            json.dump(data, f, indent=4)

        # Render HTML Template
        rendered_html = render_template("certificate_template.html", **data)

        # Generate PDF
        os.makedirs("output", exist_ok=True)
        file_path = f"output/certificate_{name.replace(' ', '_')}.pdf"
        HTML(string=rendered_html, base_url='.').write_pdf(file_path)

        return send_file(file_path, as_attachment=True)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)

