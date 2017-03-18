import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import flask_ask
from parseCountries import *

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
    print "QUESTION " + question.toEnglish()
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
@ask.intent("AnswerIntent", convert={'reply': str})
def answer(reply):
    global currentQuestion

    print "HERE"
    print reply
    if reply in currentQuestion.answer:
        msg = "Good job!"
    else:
        msg = "Sorry.  The answer is " + str(currentQuestion.answer)

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
    tempQ, news = gen(1)
    print tempQ[0]
    print ""
    tempQ = tempQ[0]
    tq = TriviaQuestion(tempQ[0], tempQ[1], tempQ[2])
    questionList.append(tq)
    return questionList



class TriviaQuestion:
    def __init__(self, questionText, answerText, answerList,country):
        self.questionText = questionText
        self.answerText = answerText
        self.answerList = answerList
        self.newsSource = None
        self.country = country #Which country is this question about?


    def toEnglish(self):
        toReturn = self.questionText
        #print self.answer
        #print self.questionText
    #    for a in range(len(self.answers)):
    #        if a != 0:
    #            toReturn += " " + str(a) + ". " + self.answers[a] + ". "
        return toReturn


if __name__ == '__main__':
    app.run(debug=True)




