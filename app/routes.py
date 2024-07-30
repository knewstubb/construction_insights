from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import Feedback
from app import db
from .llm_analysis import analyze_trends
import csv
from io import StringIO
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        try:
            highlights = request.form['highlights']
            lowlights = request.form['lowlights']
            emerging_issues = request.form['emerging_issues']
            weather = request.form['weather']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            new_feedback = Feedback(highlights=highlights, lowlights=lowlights, emerging_issues=emerging_issues, weather=weather, timestamp=timestamp)
            
            db.session.add(new_feedback)
            db.session.commit()

            return jsonify({"message": "Feedback submitted successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    return render_template('form.html')

@bp.route('/dashboard')
def dashboard():
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    return render_template('dashboard.html', feedbacks=feedbacks)

@bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        query = request.form.get('query')
        result = analyze_trends(query)
        return jsonify({"result": result})
    
    return render_template('analyze.html')

@bp.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            try:
                stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                for row in csv_reader:
                    feedback = Feedback(
                        highlights=row['highlights'],
                        lowlights=row['lowlights'],
                        emerging_issues=row['emerging_issues'],
                        timestamp=row['timestamp'],
                        weather=row['weather']
                    )
                    db.session.add(feedback)
                db.session.commit()
                flash('CSV file successfully uploaded and processed')
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error processing CSV: {str(e)}')
                return redirect(request.url)
    return render_template('upload_csv.html')