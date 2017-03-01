import json
import requests
import os


def run():
    cl = get_countries_list()
    print(len(cl))
    a3c_to_country = a3c_to_country_dict(cl)

    for country, country_a2c, country_a3c in cl:
        data = {}

        file = 'data/' + str(country_a2c) + '.json'
        print(file)
        with open(file, 'w') as outfile:
            url = 'https://restcountries.eu/rest/v2/alpha/' + country_a2c
            response = requests.get(url)
            json_data = json.loads(response.content.decode('utf-8', 'ignore'))

            data['country'] = country
            data['capital'] = json_data['capital']
            data['population'] = json_data['population']
            data['region'] = json_data['region']
            data['latlng'] = str(json_data['latlng'][0]) + ', ' + str(json_data['latlng'][1])

            borders = json_data['borders']
            if len(borders) == 0:
                str_borders = "none"
            elif len(borders) == 1:
                str_borders = borders[0]
            elif len(borders) == 2:
                str_borders = borders[0] + " and " + borders[1]
            else:
                for i in range(len(borders)):
                    borders[i] = a3c_to_country[borders[i]]

                str_borders = ', '.join(borders[:-1])
                str_borders = str_borders + ", and " + borders[-1]

            data['borders'] = str_borders

            languages = json_data['languages']
            languages = [lang_dict['name'] for lang_dict in languages]
            if len(languages) == 0:
                str_languages = "none"
            elif len(languages) == 1:
                str_languages = languages[0]
            elif len(languages) == 2:
                str_languages = languages[0] + " and " + languages[1]
            else:
                str_languages = ', '.join(languages[:-1])
                str_languages = str_languages + ", and " + languages[-1]

            data['languages'] = str_languages

        factbook_file = '_data/' + str(country_a2c) + '.json'
        if os.path.isfile(factbook_file) == True:
            with open(factbook_file, encoding='utf-8') as reader:
                json_data = json.load(reader)

                data['area'] = 0
                data['land'] = 0
                data['water'] = 0
                data['climate'] = 0
                data['median_age_male'] = 0
                data['median_age_female'] = 0
                data['life_expectancy_male'] = 0
                data['life_expectancy_female'] = 0
                data['literacy_male'] = 0
                data['literacy_female'] = 0
                data['unemployment'] = 0
                data['poverty_line'] = 0
        else:
            print("Warning, no factbook json for...")
            print(country)
            print(country_a2c)
            print(country_a3c)
            print()

        # json.dump(data, outfile)
        # break


def get_countries_list():
    country_list = set()

    # first pass
    url = 'https://restcountries.eu/rest/v1/all'
    response = requests.get(url)
    json_data = json.loads(response.content.decode("utf-8"))
    for country in json_data:
        # print country['name']
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    # second pass
    url = 'https://restcountries.eu/rest/v2/all'
    response = requests.get(url)
    json_data = json.loads(response.content.decode("utf-8"))
    for country in json_data:
        # print country['name']
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    return country_list


def a3c_to_country_dict(countries_list):
    ret = {}
    for country, a2c, a3c in countries_list:
        ret[a3c] = country

    return ret


if __name__ == "__main__":
    run();