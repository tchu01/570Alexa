import json
import requests
import random


def main():
    cl = getCountriesList()
    nl = getNewsList()
    relevant = []
    for a in nl:
        # print(a)
        found = False
        for c, a2c in cl:
            if c in a:
                print("FOUND: " + str(c))
                # print("FROM: " + str(a))
                relevant.append((c, a2c))
                found = True
        if not found:
            # print("Could not find a country :<")
            # print("\n")
            pass

    question, answer = generate_qa(relevant)


def getNewsList():
    newsList = []
    sourceList = ['bbc-news', 'cnn', 'cnbc', 'google-news', 'the-huffington-post']
    API_KEY = 'd017adabb56b40d1919976e8206486c2'

    for src in sourceList:
        url = 'https://newsapi.org/v1/articles?source=' + src + '&apiKey=' + API_KEY
        response = requests.get(url)
        jsonData = json.loads(response.content.decode("utf-8"))
        for article in jsonData['articles']:
            # print article['title']
            # print "\t" + (article['description'] or '')
            articleString = article['title'] + " - " + (article['description'] or '')
            newsList.append(articleString)

    return newsList


def getCountriesList():
    countryList = set()

    # first pass
    url = 'https://restcountries.eu/rest/v1/all'
    response = requests.get(url)
    jsonData = json.loads(response.content.decode("utf-8"))
    for country in jsonData:
        # print country['name']
        countryList.add((country['name'], country['alpha2Code']))

    # second pass
    url = 'https://restcountries.eu/rest/v2/all'
    response = requests.get(url)
    jsonData = json.loads(response.content.decode("utf-8"))
    for country in jsonData:
        # print country['name']
        countryList.add((country['name'], country['alpha2Code']))

    return countryList


def generate_qa(relevant):
    country, country_a2c = random.choice(relevant)
    print(country)
    print(country_a2c)

    country_file = 'data/' + str(country_a2c) + '.json'
    with open(country_file) as country_json:
        country_answers = json.load(country_json)

        with open('questions.json') as questions_json:
            possible_questions = json.load(questions_json)

            keys = list(country_answers.keys())
            keys.remove('country')
            keys.append('larger_population')
            keys.append('larger_area')
            choice = random.choice(keys)
            print(choice)

            question = possible_questions[choice][0]
            answer = possible_questions[choice][1]

            question = question.replace("#COUNTRY#", country)
            answer = answer.replace("#COUNTRY#", country)

            if '#COUNTRY2#' not in question:
                answer = answer.replace('#ANSWER#', str(country_answers[choice]))
            else:
                country2 = country
                country2_a2c = country_a2c
                while country == country2:
                    country2, country2_a2c = random.choice(relevant)

                print(country2)
                print(country2_a2c)

                country2_file = 'data/' + str(country2_a2c) + '.json'
                with open(country2_file) as country2_json:
                    country2_answers = json.load(country2_json)

                    question = question.replace("#COUNTRY2#", country2)
                    answer = answer.replace("#COUNTRY2#", country2)

                    if choice == 'larger_population':
                        choice = 'population'
                    elif choice == 'larger_area':
                        choice = 'area'

                    val = country_answers[choice]
                    val2 = country2_answers[choice]
                    print(val)
                    print(val2)

                    if val > val2:
                        final = country
                    else:
                        final = country2

                    answer = answer.replace("#ANSWER#", final)

            print(question)
            print(answer)
            return question, answer


if __name__ == "__main__":
    main()