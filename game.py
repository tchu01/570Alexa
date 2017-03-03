import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import flask_ask

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG) 


currentQuestion = None

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    global currentQuestion
    question = generateQuestions(1)[0]
    currentQuestion = question 
    print question.toEnglish() 
    return flask_ask.question(question.toEnglish())
    #numbers = [randint(0, 9) for _ in range(3)]
    #round_msg = render_template('round', numbers=numbers)
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    #return question(round_msg)

@ask.intent("NoIntent")
def stop():
    msg = "Ok.  See you later"
    return statement(msg)

#detect invalid answer and Out of index number
@ask.intent("AnswerIntent", convert={'saidNum': int})
def answer(saidNum):
    global currentQuestion
    if saidNum == currentQuestion.correct:
        msg = "Good job!"
    else:
        msg = "Sorry.  The answer is " + str(currentQuestion.answers[currentQuestion.correct])

    #winning_numbers = session.attributes['numbers']
    #if [first, second, third] == winning_numbers:
    #    msg = "Good job!"
    #else:
    #    msg = "Sorry, that's the wrong answer."
    return statement(msg) 

#howMany = Int 
#returns list of questions
def generateQuestions(howMany):
    questionList = []
    questionList.append(TriviaQuestion("What is the best hockey team?",["","Calgary Flames","San Jose Sharks"],1))
    return questionList

class TriviaQuestion:
    def __init__(self, questionText, answers, correct):
        self.questionText = questionText 
        self.answers = answers
        self.correct = correct #int referring to the correct answer in the answer list 

    def toEnglish(self):
        toReturn = self.questionText
        for a in range(len(self.answers)):
            if a != 0:
                toReturn += " " + str(a) + ". " + self.answers[a] + ". "
        return toReturn

if __name__ == '__main__':

    app.run(debug=True)