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

    question, answer = generate_question(relevant)


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


def generate_question(relevant):
    print()
    if 0.1 >= 0.2:
        with open('factbook_questions.json') as data_file:
            factbook_questions = json.load(data_file)
        print(len(factbook_questions))

    else:
        with open('simple_questions.json') as data_file:
            simple_questions = json.load(data_file)

        keys = list(simple_questions.keys())
        choice = random.choice(keys)

        question = simple_questions[choice][0]
        answer = simple_questions[choice][1]

        country, country_a2c = random.choice(relevant)
        print(choice)
        print(country)
        print(country_a2c)

        question = question.replace("#COUNTRY#", country)
        answer = answer.replace("#COUNTRY#", country)

        if "#COUNTRY2#" not in question:
            url = "https://restcountries.eu/rest/v2/alpha/" + country_a2c
            response = requests.get(url)
            jsonData = json.loads(response.content.decode("utf-8"))
            val = jsonData[choice]
            answer = answer.replace("#ANSWER#", str(val))

        elif "#COUNTRY2#" in question:
            country2 = country
            country2_a2c = country_a2c
            while country == country2:
                country2, country2_a2c = random.choice(relevant)

            print(country2)

            question = question.replace("#COUNTRY2#", country2)
            answer = answer.replace("#COUNTRY2#", country2)

            url = "https://restcountries.eu/rest/v2/alpha/" + country_a2c
            response = requests.get(url)
            jsonData = json.loads(response.content.decode("utf-8"))
            val = jsonData["population"]

            url = "https://restcountries.eu/rest/v2/alpha/" + country2_a2c
            response = requests.get(url)
            jsonData = json.loads(response.content.decode("utf-8"))
            val2 = jsonData["population"]

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
