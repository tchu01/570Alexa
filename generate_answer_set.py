import os
import json
import requests

def answer_set():
    data = os.listdir('data')
    ret = set()

    for file in data:
        with open('data/' + file) as country:
            js = json.load(country)
            for key in js.keys():
                if key != 'climate':
                    answers = js[key]
                    for answer in answers:
                        ret.add(answer)

    return ret


if __name__ == '__main__':
    alexa_set = answer_set()
    print(alexa_set)

