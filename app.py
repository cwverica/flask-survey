from surveys import satisfaction_survey
from flask import Flask, request, render_template, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "supr-rly-secrt"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

responses = []
survey = satisfaction_survey


@app.route('/')
def show_home():
    app.responses = []
    return render_template('home.html')


@app.route('/survey/<ident>')
def show_survey(ident):

    if request.args.get('answers', None):
        responses.append(request.args['answers'])
    
    title = survey.title
    instructions = survey.instructions
    question_obj = survey.questions[int(ident)]
    last = len(survey.questions) - 1
    question = question_obj.question
    choices = question_obj.choices
    allow_text = question_obj.allow_text
    index = int(ident)
    page_dict = {'title': title, 'instructions': instructions, 'question': question,
                    'choices': choices, 'allow_text': allow_text, 'index': index, 'last': last}
    return render_template('survey.html', page_dict=page_dict)

@app.route('/answer', methods=["POST"])
def receive_answer():
    responses.append(request.form['answers'])
    next_page=request.form['ident']
    if int(next_page) == len(survey.questions):
        return redirect('survey/end', code=302)
    else:
        return redirect(f'survey/{next_page}', code=302)
    # Something is happening where I can't get to the end page, the submit button just doesn't work on the last question


@app.route('/survey/end')
def show_results():
    title = survey.title
    return render_template('end_page.html', title=title, responses=responses)

