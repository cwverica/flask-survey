from surveys import satisfaction_survey, personality_quiz, surveys
from flask import Flask, request, render_template, jsonify, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "supr-rly-secrt"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []
# survey = satisfaction_survey


@app.route('/')
def show_home():
    # Used this as a way to not have to restart the "server" everytime
    # responses = []
    return render_template('home.html', surveys=surveys)


@app.route('/start', methods=["POST"])
def start_survey():
    session['responses'] = []
    choice = request.form.get('surveys')
    global survey 
    survey = surveys.get(f'{choice}')
    return redirect('survey/0')


@app.route('/survey/<ident>')
def show_survey(ident):

    if int(ident) != len(session['responses']):
        return courseCorrect()

    if request.args.get('answers', None):
        responses = session['responses']
        responses.append(request.args['answers'])
        session['responses'] = responses
    
    question_obj = survey.questions[int(ident)]

    page_dict = {'title': survey.title,
                'instructions': survey.instructions,
                'question': question_obj.question,
                'choices': question_obj.choices, 
                'allow_text': question_obj.allow_text, 
                'index': int(ident), 
                'last': len(survey.questions) -1}
    return render_template('survey.html', page_dict=page_dict)

@app.route('/answer', methods=["POST"])
def receive_answer():
    responses = session['responses']
    if request.form.get('comments'):
        answer = request.form['answers']
        comments = request.form['comments']
        responses.append(f'"{answer}", your comments: "{comments}"')
    else:
        answer = request.form['answers']
        responses.append(f'"{answer}"')
    session['responses'] = responses
    next_page=request.form['ident']
    if int(next_page) == len(survey.questions):
        return redirect('survey/end', code=302)
    else:
        return redirect(f'survey/{next_page}', code=302)
    
@app.route('/survey/end')
def show_results():
    title = survey.title
    return render_template('end_page.html', title=title)

def courseCorrect():
    if len(session['responses']) < len(survey.questions):
        flash("You must answer the questions in order. You have been redirected.")
        target = len(session['responses'])
        return redirect(f'{target}', code=302)
    else:
        flash("You have already completed the survey. You have been redirected.")
        return redirect('end', code=302)