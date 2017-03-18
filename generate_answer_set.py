import os
import json

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


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
    answerSet = set()

    for x in alexa_set:
        x = str(x)
        x = str(x.replace('\"',''))
        answerSet.add(str(x).encode(encoding='ascii', errors='ignore'))

    for x in answerSet:
        print x

