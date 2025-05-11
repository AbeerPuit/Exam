from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

teachers = {'teacher1': 'teachpass'}
students = {'student1': 'studpass'}

@app.route('/')
def home():
    return redirect(url_for('login_teacher'))

@app.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if teachers.get(username) == password:
            session['user'] = username
            session['role'] = 'teacher'
            return redirect(url_for('dashboard_teacher'))
        return "Invalid teacher credentials"
    return render_template('login_teacher.html')

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if students.get(username) == password:
            session['user'] = username
            session['role'] = 'student'
            session['student_name'] = username
            return redirect(url_for('dashboard_student'))
        return "Invalid student credentials"
    return render_template('login_student.html')

@app.route('/dashboard_teacher')
def dashboard_teacher():
    if session.get('role') != 'teacher':
        return redirect(url_for('login_teacher'))
    return render_template('dashboard_teacher.html')

@app.route('/dashboard_student')
def dashboard_student():
    if session.get('role') != 'student':
        return redirect(url_for('login_student'))
    try:
        files = os.listdir('quizzes/')
        quizzes = []
        for file in files:
            if file.endswith('.json'):
                parts = file.replace('.json', '').split('_')
                quizzes.append({'id': file.replace('.json', ''), 'subject': parts[0], 'section': parts[1]})
    except FileNotFoundError:
        quizzes = []
    return render_template('dashboard_student.html', quizzes=quizzes, student_name=session.get('student_name'))

@app.route('/upload_question', methods=['POST'])
def upload_question():
    subject = request.form.getlist('subject[]')[0]
    section = request.form.getlist('section[]')[0]

    questions = []
    total = len(request.form.getlist('question[]'))

    for i in range(total):
        q = request.form.getlist('question[]')[i]
        a = request.form.getlist('option_a[]')[i]
        b = request.form.getlist('option_b[]')[i]
        c = request.form.getlist('option_c[]')[i]
        d = request.form.getlist('option_d[]')[i]
        correct = request.form.getlist('correct[]')[i]
        options = {'A': a, 'B': b, 'C': c, 'D': d}

        questions.append({
            'question': q,
            'options': options,
            'answer': correct
        })

    if not os.path.exists('quizzes'):
        os.makedirs('quizzes')

    filename = f'{subject}_{section}.json'
    with open(os.path.join('quizzes', filename), 'w') as f:
        json.dump(questions, f)

    return render_template('quiz_uploaded.html', subject=subject, section=section)

# ✅ FIXED: This is the only correct attempt route
@app.route('/attempt_quiz/<quiz_id>', methods=['GET', 'POST'])
def attempt_quiz(quiz_id):
    if session.get('role') != 'student':
        return redirect(url_for('login_student'))

    quiz_path = os.path.join('quizzes', f'{quiz_id}.json')
    if not os.path.exists(quiz_path):
        return "Quiz not found"

    with open(quiz_path) as f:
        questions = json.load(f)

    if request.method == 'POST':
        score = 0
        responses = []

        for i, q in enumerate(questions):
            selected = request.form.get(f'question{i}')
            correct = q['answer']
            status = "Correct" if selected == correct else ("Wrong" if selected else "Not Answered")
            if selected == correct:
                score += 1
            responses.append({
                'question': q['question'],
                'selected': selected if selected else "Not Answered",
                'correct': correct,
                'status': status
            })

        return render_template('result.html', score=score, total=len(questions), responses=responses)

    return render_template('attempt_quiz.html', questions=questions, quiz_id=quiz_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
