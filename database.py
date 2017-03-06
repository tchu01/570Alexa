import json
import requests
import os
import re


def run():
    cl = get_countries_list()
    print(len(cl))
    a3c_to_country = a3c_to_country_dict(cl)

    for country, country_a2c, country_a3c in cl:
        data = {}

        file = 'data/' + str(country_a2c) + '.json'
        print(file)
        with open(file, 'w', encoding='utf-8', ) as outfile:
            url = 'https://restcountries.eu/rest/v2/alpha/' + country_a2c
            response = requests.get(url)
            json_data = json.loads(response.content.decode('utf-8', 'ignore'))

            data['country'] = country
            if 'capital' in json_data:
                data['capital'] = json_data['capital']
            if 'population' in json_data:
                data['population'] = json_data['population']
            if 'region' in json_data:
                data['region'] = json_data['region']
            if 'area' in json_data:
                data['area'] = json_data['area']
            if 'latlng' in json_data:
                if len(json_data['latlng']) == 2:
                    data['latlng'] = str(json_data['latlng'][0]) + ', ' + str(json_data['latlng'][1])

            if 'borders' in json_data:
                borders = json_data['borders']
                if len(borders) == 0:
                    str_borders = 'none'
                elif len(borders) == 1:
                    str_borders = a3c_to_country[borders[0]]
                elif len(borders) == 2:
                    str_borders = a3c_to_country[borders[0]] + ' and ' + a3c_to_country[borders[1]]
                else:
                    for i in range(len(borders)):
                        borders[i] = a3c_to_country[borders[i]]

                    str_borders = ', '.join(borders[:-1])
                    str_borders = str_borders + ', and ' + borders[-1]

                data['borders'] = str_borders

            if 'languages' in json_data:
                languages = json_data['languages']
                languages = [lang_dict['name'] for lang_dict in languages]
                if len(languages) == 0:
                    str_languages = 'none'
                elif len(languages) == 1:
                    str_languages = languages[0]
                elif len(languages) == 2:
                    str_languages = languages[0] + ' and ' + languages[1]
                else:
                    str_languages = ', '.join(languages[:-1])
                    str_languages = str_languages + ', and ' + languages[-1]

                data['languages'] = str_languages

            factbook_file = '_data/' + str(country_a2c) + '.json'
            if os.path.isfile(factbook_file) == True:
                with open(factbook_file, encoding='utf-8') as reader:
                    json_data = json.load(reader)

                    if 'Geography' in json_data and 'Area' in json_data['Geography']:
                        if 'land' in json_data['Geography']['Area']:
                            data['land'] = json_data['Geography']['Area']['land']['text']
                        if 'water' in json_data['Geography']['Area']:
                            data['water'] = json_data['Geography']['Area']['water']['text']
                    if 'Geography' in json_data and 'Climate' in json_data['Geography']:
                        if 'text' in json_data['Geography']['Climate']:
                            data['climate'] = json_data['Geography']['Climate']['text']
                        else:
                            keys = list(json_data['Geography']['Climate'].keys())
                            data['climate'] = json_data['Geography']['Climate'][keys[0]]['text']

                    if 'People and Society' in json_data and 'Median age' in json_data['People and Society']:
                        data['median_age_male'] = json_data['People and Society']['Median age']['male']['text']
                        data['median_age_female'] = json_data['People and Society']['Median age']['female']['text']
                    if 'People and Society' in json_data and 'Life expectancy at birth' in json_data['People and Society']:
                        data['life_expectancy_male'] = json_data['People and Society']['Life expectancy at birth']['male']['text']
                        data['life_expectancy_female'] = json_data['People and Society']['Life expectancy at birth']['female']['text']
                    if 'People and Society' in json_data and 'Literacy' in json_data['People and Society']:
                        data['literacy_male'] = json_data['People and Society']['Literacy']['male']['text']
                        data['literacy_female'] = json_data['People and Society']['Literacy']['male']['text']

                    if 'Economy' in json_data and 'Unemployment rate' in json_data['Economy']:
                        unemployment = json_data['Economy']['Unemployment rate']['text']
                        percent = re.match("(\d*)\%", unemployment).group()
                        if percent is not None:
                            data['unemployment'] = str(percent)

                    if 'Economy' in json_data and 'Population below poverty line' in json_data['Economy']:
                        poverty_line = json_data['Economy']['Population below poverty line']['text']
                        percent = re.match("(\d*)\%", poverty_line).group()
                        if percent is not None:
                            data['poverty_line'] = str(percent)
            else:
                print("Warning, no factbook json for...")
                print(country)
                print(country_a2c)
                print(country_a3c)
                print()

            json.dump(data, outfile)
            # break


def get_countries_list():
    country_list = set()

    # first pass
    url = 'https://restcountries.eu/rest/v1/all'
    response = requests.get(url)
    json_data = json.loads(response.content.decode('utf-8', 'ignore'))
    for country in json_data:
        # print country['name']
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    # second pass
    url = 'https://restcountries.eu/rest/v2/all'
    response = requests.get(url)
    json_data = json.loads(response.content.decode('utf-8', 'ignore'))
    for country in json_data:
        # print country['name']
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    return country_list


def a3c_to_country_dict(countries_list):
    ret = {}
    for country, a2c, a3c in countries_list:
        ret[a3c] = country

    return ret


if __name__ == '__main__':
    run()