import json
import requests
import random
import re
import pickle
import os


def gen(howMany, countryList):
    # cl = getCountriesList() #Ill call these myself, and pass it in, so we don't have to make API calls every time
    # nl = getNewsList()

    cl = get_countries()
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

    question_answer_list = []
    for i in range(howMany):
        question_answer_list.append(generate_qa(relevant))

    return question_answer_list


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
            keys.remove('climate')
            keys.append('larger_population')
            keys.append('larger_area')
            choice = random.choice(keys)
            print(choice)

            complete_question = possible_questions[choice][0]
            complete_answer = possible_questions[choice][1]

            complete_question = complete_question.replace("#COUNTRY#", country)
            complete_answer = complete_answer.replace("#COUNTRY#", country)

            if '#COUNTRY2#' not in complete_question:
                answer_choices = get_alexa_answers(choice, country_answers[choice])
                fill = round_answer(choice, country_answers[choice])

                complete_answer = complete_answer.replace('#ANSWER#', str(fill))
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

                    complete_question = complete_question.replace("#COUNTRY2#", country2)
                    complete_answer = complete_answer.replace("#COUNTRY2#", country2)

                    if choice == 'larger_population':
                        choice = 'population'
                    elif choice == 'larger_area':
                        choice = 'area'

                    val = country_answers[choice][0]
                    val2 = country2_answers[choice][0]
                    print(val)
                    print(val2)

                    if val > val2:
                        final = country
                        answer_choices = [country]
                    else:
                        final = country2
                        answer_choices = [country2]

                    complete_answer = complete_answer.replace("#ANSWER#", final)

            print(complete_question)
            print(complete_answer)
            print(answer_choices)
            print()
            return complete_question, complete_answer, answer_choices


def get_alexa_answers(choice, answer_list):
    population = ['population']
    kilometers_squared = ['area', 'land', 'water']
    kilometers = ['coastline']
    age = ['median_age_male', 'median_age_female', 'life_expectancy_male', 'life_expectancy_female']
    percent = ['pop_growth_rate', 'health_expenditures', 'obesity', 'education_expenditures', 'literacy_male',
               'literacy_female', 'unemployment', 'poverty_line']

    ret = []

    if choice in population:
        val = answer_list[0]
        val = round(val / 1000000) * 1000000

        ret.append(val)
        ret.append(float(val))
    elif choice in kilometers_squared:
        val = answer_list[0]
        temp = re.match('(\d*) kilometers squared', val).group(1)
        temp = round(int(float(temp)) / 1000) * 1000

        ret.append(str(temp) + ' kilometers squared')
        ret.append(str(float(temp)) + ' kilometers squared')
    elif choice in kilometers:
        val = answer_list[0]
        temp = re.match('(\d*) kilometers', val).group(1)
        temp = round(int(float(temp)) / 1000) * 1000

        ret.append(str(temp) + ' kilometers')
        ret.append(str(float(temp)) + ' kilometers')
    elif choice in age:
        val = answer_list[0]
        temp = re.match('(\d*) years', val).group(1)
        temp = round(int(float(temp)) / 10) * 10

        ret.append(str(temp) + ' years')
        ret.append(str(float(temp)) + ' years')
    elif choice in percent:
        val = answer_list[0]
        temp = re.match('(\d*)%', val).group(1)
        temp = round(int(float(temp)) / 10) * 10

        ret.append(str(temp) + '%')
        ret.append(str(float(temp)) + '%')
    else:
        return answer_list

    return ret


def round_answer(choice, answer_list):
    population = ['population']
    kilometers_squared = ['area', 'land', 'water']
    kilometers = ['coastline']
    age = ['median_age_male', 'median_age_female', 'life_expectancy_male', 'life_expectancy_female']
    percent = ['pop_growth_rate', 'health_expenditures', 'obesity', 'education_expenditures', 'literacy_male',
               'literacy_female', 'unemployment', 'poverty_line']

    one_choice = ['borders', 'languages', 'natural_resources', 'ethnic_groups', 'agriculture', 'industries', 'exports',
                  'imports']

    ret = answer_list[0]

    if choice in population:
        val = answer_list[0]
        ret = round(val / 1000000) * 1000000
        answer_list[0] = ret
    elif choice in kilometers_squared:
        val = answer_list[0]
        temp = re.match('(\d*) kilometers squared', val).group(1)
        temp = round(int(float(temp)) / 1000) * 1000
        ret = str(temp) + ' kilometers squared'
        answer_list[0] = ret
    elif choice in kilometers:
        val = answer_list[0]
        temp = re.match('(\d*) kilometers', val).group(1)
        temp = round(int(float(temp)) / 1000) * 1000
        ret = str(temp) + ' kilometers'
        answer_list[0] = ret
    elif choice in age:
        val = answer_list[0]
        temp = re.match('(\d*) years', val).group(1)
        temp = round(int(float(temp)) / 10) * 10
        ret = str(temp) + ' years'
        answer_list[0] = ret
    elif choice in percent:
        val = answer_list[0]
        temp = re.match('(\d*)%', val).group(1)
        temp = round(int(float(temp)) / 10) * 10
        ret = str(temp) + '%'
        answer_list[0] = ret
    elif choice in one_choice:
        ret = ', '.join(answer_list)
    else:
        pass

    return ret


def get_news_headlines():
    news_headline_file = "news_headlines.p"
    if os.path.isfile(news_headline_file) == True:
        pass
    else:
        pickle_headlines()

    return unpickle_headlines()


def pickle_headlines():
    with open("news_headlines.p", "wb") as outfile:
        news = getNewsList()
        pickle.dump(news, outfile)


def unpickle_headlines():
    with open("news_headlines.p", "rb") as infile:
        news = pickle.load(infile)
        return news


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


def get_countries():
    country_file = "rest_countries.p"
    if os.path.isfile(country_file) == True:
        pass
    else:
        pickle_countries()

    return unpickle_countries()


def pickle_countries():
    with open("rest_countries.p", "wb") as outfile:
        countries = getCountriesList()
        pickle.dump(countries, outfile)


def unpickle_countries():
    with open("rest_countries.p", "rb") as infile:
        countries = pickle.load(infile)
        return countries


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


if __name__ == "__main__":
    gen(5, [])
