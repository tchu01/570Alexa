import json
import requests
import random


def main():
    cl = getCountriesList()
    nl = getNewsList()
    relevant = []
    for a in nl:
        # print a
        found = False
        for c in cl:
            if c in a:
                print("FOUND: " + str(c))
                # print("FROM: " + str(a))
                relevant.append(c)
                found = True
        if not found:
            # print("Could not find a country :<")
            # print("\n")
            pass

    qa = generate_question(relevant)


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
        countryList.add(country['name'])

    # second pass
    url = 'https://restcountries.eu/rest/v2/all'
    response = requests.get(url)
    jsonData = json.loads(response.content.decode("utf-8"))
    for country in jsonData:
        # print country['name']
        countryList.add(country['name'])

    return countryList


def generate_question(relevant):
    if random.random() >= 0.2:
        with open('factbook_questions.json') as data_file:
            factbook_questions = json.load(data_file)
        print(len(factbook_questions))

    else:
        with open('simple_questions.json') as data_file:
            simple_questions = json.load(data_file)
        print(len(simple_questions))

        num_countries = random.randint(1,2)
        if num_countries == 1:
            country = random.choice(relevant)
        else:
            country1 = random.choice(relevant)
            country2 = country1
            while country1 == country2:
                country2 = random.choice(relevant)


if __name__ == "__main__":
    main()
