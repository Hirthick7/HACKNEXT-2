from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime
import uuid
import random
import os
import bcrypt  # For password hashing

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'super_secret_key_for_learning_copilot')

# -----------------------------------------------
# ✅ MONGODB CONNECTION (safer timeout)
# -----------------------------------------------
MONGODB_URI = os.environ.get(
    'MONGODB_URI',
    "mongodb+srv://hirthick07:bapcx5j97s@cluster0.jqdiyw1.mongodb.net/"
)

USE_IN_MEMORY = False
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['learning_copilot']

    users = db['Education']
    assessments = db['assessments']
    curricula = db['curricula']

    print("MongoDB Connected Successfully!")
except Exception as e:
    print("MongoDB Error:", e)
    # fall back to in-memory lists for local testing
    users = []
    assessments = []
    curricula = []
    USE_IN_MEMORY = True
    print("Using in-memory storage.")


# -----------------------------------------------
# ✅ CONTENT_BANK required by generate_curriculum
# -----------------------------------------------
CONTENT_BANK = {
    "Calculus": {
        "topics": ["Limits", "Derivatives", "Integrals", "Series", "Applications of Integration"],
        "links": [
            "https://www.khanacademy.org/math/calculus-1",
            "https://www.youtube.com/watch?v=derivative_example",
            "https://www.khanacademy.org/math/calculus-2",
            "https://www.youtube.com/watch?v=integral_example"
        ],
        "problems": lambda: f"Solve: ∫ x dx = {random.randint(1,10)} x^2/2 + C",
        "explanations": [
            "Visual: Watch animation on limits.",
            "Auditory: Listen to derivative podcast.",
            "Reading: Read integral theory.",
            "Kinesthetic: Practice series problems hands-on."
        ]
    },
    "Thermodynamics": {
        "topics": ["Laws of Thermo", "Heat Engines", "Entropy", "Phase Changes", "Thermodynamic Cycles"],
        "links": [
            "https://www.khanacademy.org/science/physics/thermodynamics",
            "https://www.youtube.com/watch?v=thermo_laws",
            "https://www.khanacademy.org/science/physics/thermodynamics/entropy",
            "https://www.youtube.com/watch?v=entropy_example"
        ],
        "problems": lambda: f"Calculate entropy change: ΔS = {random.uniform(1,10):.2f} J/K",
        "explanations": [
            "Visual: Simulate heat engine diagram.",
            "Auditory: Lecture on entropy.",
            "Reading: Textbook on phase changes.",
            "Kinesthetic: Lab experiment for cycles."
        ]
    }
}


# -----------------------------------------------
# ROUTES
# -----------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


# Signup & Signin templates assumed to exist (signin.html, signup.html)
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup_post', methods=['POST'])
def signup_post():
    name = request.form.get('name', '')
    email = request.form.get('email', '').lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash("Please provide email and password.")
        return redirect(url_for('signup'))

    if not USE_IN_MEMORY:
        if users.find_one({"email": email}):
            flash("Email already exists! Please sign in.")
            return redirect(url_for('signin'))
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({"name": name, "email": email, "password": hashed_pw})
    else:
        if any(u['email'] == email for u in users):
            flash("Email already exists! Please sign in.")
            return redirect(url_for('signin'))
        users.append({"name": name, "email": email, "password": password})

    flash("Signup successful! Please sign in.")
    return redirect(url_for('signin'))


@app.route('/signin_post', methods=['POST'])
def signin_post():
    email = request.form.get('email', '').lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash("Please provide email and password.")
        return redirect(url_for('signin'))

    user = None
    if not USE_IN_MEMORY:
        user = users.find_one({"email": email})
        if not user:
            flash("User not found.")
            return redirect(url_for('signin'))

        stored = user.get('password')
        # stored is bytes (bcrypt) when using MongoDB
        if not stored or not bcrypt.checkpw(password.encode('utf-8'), stored):
            flash("Incorrect password.")
            return redirect(url_for('signin'))
    else:
        user = next((u for u in users if u['email'] == email), None)
        if not user or user.get('password') != password:
            flash("Invalid credentials.")
            return redirect(url_for('signin'))

    # Login success
    session.clear()
    session['logged_in'] = True
    session['email'] = email
    session['user_name'] = user.get('name', '')
    # use email as stable user id for this demo
    session['user_id'] = email

    flash("Signed in successfully.")
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('index'))


@app.route('/select_subject', methods=['POST'])
def select_subject():
    if not session.get('logged_in'):
        flash("Please sign in first.")
        return redirect(url_for('signin'))

    subject = request.form.get('subject')
    if not subject:
        flash("Please choose a subject.")
        return redirect(url_for('index'))

    session['subject'] = subject
    return redirect(url_for('quiz'))


@app.route('/quiz')
def quiz():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    if 'subject' not in session:
        return redirect(url_for('index'))
    return render_template('quiz.html', subject=session['subject'])


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        payload = request.get_json(force=True)
        responses = payload.get('responses')
        if not responses or len(responses) < 10:
            return jsonify({'success': False, 'error': 'Invalid responses'}), 400

        subject = session.get('subject')
        user_id = session.get('user_id', str(uuid.uuid4()))

        prior_score = sum(1 for r in responses[:5] if int(r) == 1) * 20

        vark_scores = {'V': 0, 'A': 0, 'R': 0, 'K': 0}
        mapping = [('V', 'A'), ('A', 'R'), ('R', 'K'), ('K', 'V'), ('V', 'R')]
        for i, r in enumerate(responses[5:10]):
            first, second = mapping[i]
            r_int = 1 if str(r) == '1' else 0
            if r_int == 1:
                vark_scores[first] += 1
            else:
                vark_scores[second] += 1

        learning_style = max(vark_scores, key=vark_scores.get)

        assessment = {
            "user_id": user_id,
            "subject": subject,
            "prior_score": prior_score,
            "style": learning_style,
            "responses": responses,
            "time": datetime.utcnow()
        }

        # save assessment
        try:
            if not USE_IN_MEMORY:
                assessments.insert_one(assessment)
            else:
                assessments.append(assessment)
        except Exception as e:
            print("Warning: failed to save assessment:", e)

        curriculum = generate_curriculum(user_id, subject, prior_score, learning_style)

        try:
            if not USE_IN_MEMORY:
                curricula.insert_one(curriculum)
            else:
                curricula.append(curriculum)
        except Exception as e:
            print("Warning: failed to save curriculum:", e)

        session['assessment'] = {'score': prior_score, 'style': learning_style}
        return jsonify({'success': True})
    except Exception as e:
        print("submit_quiz error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500


def generate_curriculum(user_id, subject, score, style):
    bank = CONTENT_BANK.get(subject) or CONTENT_BANK['Calculus']
    days = []

    for day_num in range(1, 31):
        num_topics = 3 if score > 70 else 2 if score > 40 else 1
        topics = random.sample(bank['topics'], min(num_topics, len(bank['topics'])))
        links = [random.choice(bank['links']) for _ in topics]
        problems = [bank['problems']() for _ in topics]

        style_lower = style.lower() if isinstance(style, str) else ''
        explanations = [next((e for e in bank['explanations'] if style_lower and style_lower in e.lower()), bank['explanations'][0]) for _ in topics]

        days.append({
            'day': day_num,
            'topics': topics,
            'links': links,
            'problems': problems,
            'explanations': explanations,
            'completed': False
        })

    return {
        'user_id': user_id,
        'subject': subject,
        'days': days,
        'generated_at': datetime.utcnow()
    }


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))

    user_id = session.get('user_id')
    curriculum = None
    try:
        if not USE_IN_MEMORY:
            curriculum = curricula.find_one({'user_id': user_id})
        else:
            curriculum = next((c for c in curricula if c.get('user_id') == user_id), None)
    except Exception as e:
        print("DB read error on dashboard:", e)
        curriculum = None

    if not curriculum:
        flash("No curriculum found. Please take the quiz.")
        return redirect(url_for('quiz'))

    assessment = session.get('assessment', {'score': 0, 'style': 'Unknown'})
    subject = session.get('subject', curriculum.get('subject') if isinstance(curriculum, dict) else None)
    return render_template('dashboard.html', curriculum=curriculum, assessment=assessment, subject=subject)


@app.route('/update_progress', methods=['POST'])
def update_progress():
    try:
        payload = request.get_json(force=True)
        day = int(payload.get('day'))
        user_id = session.get('user_id')

        if not USE_IN_MEMORY:
            curricula.update_one({'user_id': user_id}, {'$set': {f'days.{day-1}.completed': True}})
        else:
            for c in curricula:
                if c.get('user_id') == user_id:
                    c['days'][day-1]['completed'] = True
                    break

        return jsonify({'success': True})
    except Exception as e:
        print("update_progress error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500


# robust 404 handler — falls back if template missing
@app.errorhandler(404)
def not_found(e):
    try:
        return render_template('404.html'), 404
    except Exception:
        # fallback simple HTML if template does not exist
        return (
            "<h1>404 - Page not found</h1>"
            "<p>The page you requested does not exist.</p>"
            '<p><a href="/">Go Home</a></p>',
            404
        )


if __name__ == '_main_':
    # disable reloader to avoid debugpy SystemExit in some debuggers
    app.run(debug=True, use_reloader=False)