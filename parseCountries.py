import json
import requests
import random
import re


def gen(howMany):
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

    question_answer_list = []
    for i in range(howMany):
        question_answer_list.append(generate_qa(relevant))

    return question_answer_list


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
                singular_answer = country_answers[choice]
                fill = round_answer(choice, country_answers[choice])

                answer = answer.replace('#ANSWER#', str(fill))
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

                    val = country_answers[choice][0]
                    val2 = country2_answers[choice][0]
                    print(val)
                    print(val2)

                    if val > val2:
                        final = country
                        singular_answer = country
                    else:
                        final = country2
                        singular_answer = country

                    answer = answer.replace("#ANSWER#", final)

            print(question)
            print(answer)
            print(singular_answer)
            print()
            return question, answer, singular_answer

def round_answer(choice, answer_list):
    population = ['population']
    kilometers_squared = ['area', 'land', 'water']
    kilometers = ['coastline']
    age = ['median_age_male', 'median_age_female', 'life_expectancy_male', 'life_expectancy_female']
    percent = ['pop_growth_rate', 'health_expenditures', 'obesity', 'education_expenditures', 'literacy_male', 'literacy_female', 'unemployment', 'poverty_line']

    one_choice = ['borders', 'languages', 'natural_resources', 'ethnic_groups']

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


if __name__ == "__main__":
    gen(5)