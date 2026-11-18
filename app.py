
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

from meeting_processor import extract_text
from action_extractor import extract_meeting_insights
from rag_engine import create_rag_index, ask_meeting_question
from database import create_tables, save_meeting, get_all_meetings

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Store current meeting RAG data
meeting_index = None
meeting_chunks = []


create_tables()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_meeting():
    global meeting_index, meeting_chunks

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Please select a file"}), 400

    if not file.filename.lower().endswith((".pdf", ".txt")):
        return jsonify({"error": "Only PDF and TXT files are supported"}), 400

    title = secure_filename(file.filename)

    try:
        transcript = extract_text(file)

        if not transcript:
            return jsonify({"error": "No text found in file"}), 400

        insights = extract_meeting_insights(transcript)

        meeting_index, meeting_chunks = create_rag_index(transcript)

        save_meeting(
            title,
            transcript,
            insights,
            "",
            ""
        )

        return jsonify({
            "message": "Meeting processed successfully",
            "title": title,
            "insights": insights
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask_question():
    global meeting_index, meeting_chunks

    if meeting_index is None:
        return jsonify({"error": "Please upload a meeting first"}), 400

    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Enter a question"}), 400

    try:
        answer = ask_meeting_question(
            question,
            meeting_index,
            meeting_chunks
        )

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/meetings")
def meetings():
    records = get_all_meetings()

    return jsonify([
        {
            "id": row[0],
            "title": row[1],
            "summary": row[3],
            "created_at": row[6]
        }
        for row in records
    ])


if __name__ == "__main__":
    app.run(debug=True)
