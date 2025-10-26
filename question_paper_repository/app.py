from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to save uploaded papers
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'papers')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Temporary in-memory "database"
papers = [
    {"subject": "Maths", "year": "2023", "title": "Maths 2023 Paper", "url": "static/papers/maths2023.pdf"},
    {"subject": "Physics", "year": "2022", "title": "Physics 2023 Paper", "url": "static/papers/physics2023.pdf"},
    {"subject": "Electronics and Communication", "year": "2023", "title": "Electronics and Communication", "url": "static/papers/electronics2023.pdf"},
   
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_papers')
def get_papers():
    return jsonify(papers)

@app.route('/upload', methods=['POST'])
def upload_paper():
    subject = request.form.get('subject')
    year = request.form.get('year')
    file = request.files['file']

    if not (subject and year and file):
        return jsonify({"error": "All fields required"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # Save info
    papers.append({
        "subject": subject,
        "year": year,
        "title": f"{subject} {year} Paper",
        "url": f"static/papers/{filename}"
    })

    return jsonify({"message": "Upload successful!"}), 200

@app.route('/download/<path:filename>')
def download_paper(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)