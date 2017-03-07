import os
import json
import requests

def answer_set():
    data = os.listdir('data')
    answer = set()

    for file in data:
        with open('data/' + file) as country:
            js = json.load(country)
            for key in js.keys():
                answer.add(js[key])

    return answer


if __name__ == '__main__':
    alexa_set = answer_set()
    print(alexa_set)

