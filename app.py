from surveys import satisfaction_survey
from flask import Flask, request, render_template, jsonify, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "supr-rly-secrt"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
survey = satisfaction_survey


@app.route('/')
def show_home():
    # Used this as a way to not have to restart the "server" everytime
    responses.clear()
    return render_template('home.html')


@app.route('/survey/<ident>')
def show_survey(ident):

    if int(ident) != len(responses):
        return courseCorrect()

    if request.args.get('answers', None):
        responses.append(request.args['answers'])
    
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
    responses.append(request.form['answers'])
    next_page=request.form['ident']
    if int(next_page) == len(survey.questions):
        return redirect('survey/end', code=302)
    else:
        return redirect(f'survey/{next_page}', code=302)
    
@app.route('/survey/end')
def show_results():
    title = survey.title
    return render_template('end_page.html', title=title, responses=responses)

def courseCorrect():
    if len(responses) < len(survey.questions):
        flash("You must answer the questions in order. You have been redirected.")
        return redirect(f'{len(responses)}', code=302)
    else:
        flash("You have already completed the survey. You have been redirected.")
        return redirect('end', code=302)