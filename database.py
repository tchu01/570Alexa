import json
import requests
import os
import re


def run():
    cl = get_countries_list()
    print(len(cl))
    a3c_to_country = a3c_to_country_dict(cl)

    for country, country_a2c, country_a3c in sorted(cl):
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
                val = json_data['population']
                data['population'] = round(val / 1000000.0) * 1000000.0
            if 'region' in json_data:
                data['region'] = json_data['region']
            if 'area' in json_data:
                val = json_data['area']
                if val is not None:
                    data['area'] = str(round(val / 1000.0) * 1000.0) + ' kilometers squared'
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

            factbook_file = os.path.abspath('_data/' + str(country_a2c).lower() + '.json')
            if os.path.isfile(factbook_file) == True:
                with open(factbook_file, encoding='utf-8') as reader:
                    json_data = json.load(reader)

                    if 'Geography' in json_data and 'Area' in json_data['Geography']:
                        if 'land' in json_data['Geography']['Area']:
                            val = json_data['Geography']['Area']['land']['text']
                            land = re.match("(\d*|\d*.\d*) sq km", val)
                            if land is not None:
                                land = land.group(1)
                                land = land.replace(',', '')
                                land = float(land)
                                data['land'] = round(land / 1000.0) * 1000.0
                            else:
                                print('No land')
                        if 'water' in json_data['Geography']['Area']:
                            val = json_data['Geography']['Area']['water']['text']
                            water = re.match("(\d*|\d*.\d*) sq km", val)
                            if water is not None:
                                water = water.group(1)
                                water = water.replace(',', '')
                                water = float(water)
                                data['water'] = round(water / 1000.0) * 1000.0
                            else:
                                print('No water')
                    else:
                        print("No Geography/Area")

                    if 'Geography' in json_data and 'Climate' in json_data['Geography']:
                        if 'text' in json_data['Geography']['Climate']:
                            data['climate'] = json_data['Geography']['Climate']['text']
                        else:
                            keys = list(json_data['Geography']['Climate'].keys())
                            data['climate'] = json_data['Geography']['Climate'][keys[0]]['text']
                    else:
                        print("No Geography/Climate")

                    if 'People and Society' in json_data and 'Median age' in json_data['People and Society']:
                        median_age_male = json_data['People and Society']['Median age']['male']['text']
                        age = re.match("(\d*|\d*.\d*)", median_age_male)
                        if age is not None:
                            age = age.group(1)
                            age = float(age)
                            data['median_age_male'] = str(round(age / 10.0) * 10.0) + ' years'
                        else:
                            print('No median age male')

                        median_age_female = json_data['People and Society']['Median age']['female']['text']
                        age = re.match("(\d*|\d*.\d*)", median_age_female)
                        if age is not None:
                            age = age.group(1)
                            age = float(age)
                            data['median_age_female'] = str(round(age / 10.0) * 10.0) + ' years'
                        else:
                            print('No median age female')
                    else:
                        print("No People and Society/Median Age")

                    if 'People and Society' in json_data and 'Life expectancy at birth' in json_data['People and Society']:
                        life_expectancy_male = json_data['People and Society']['Life expectancy at birth']['male']['text']
                        age = re.match("(\d*|\d*.\d*) years", life_expectancy_male)
                        if age is not None:
                            age = age.group(1)
                            age = float(age)
                            data['life_expectancy_male'] = str(round(age / 10.0) * 10.0) + ' years'
                        else:
                            print('No life expectancy male')

                        life_expectancy_female = json_data['People and Society']['Life expectancy at birth']['female']['text']
                        age = re.match("(\d*|\d*.\d*) years", life_expectancy_female)
                        if age is not None:
                            age = age.group(1)
                            age = float(age)
                            data['life_expectancy_female'] = str(round(age / 10.0) * 10.0) + ' years'
                        else:
                            print('No life expectancy female')
                    else:
                        print("No People and Society/Life expectancy at birth")

                    if 'People and Society' in json_data and 'Literacy' in json_data['People and Society']:
                        literacy_male = json_data['People and Society']['Literacy']['male']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", literacy_male)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = float(percent)
                            data['literacy_male'] = str(round(percent / 10.0) * 10.0) + '%'
                        else:
                            print('No literacy male')

                        literacy_female = json_data['People and Society']['Literacy']['male']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", literacy_female)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = float(percent)
                            data['literacy_female'] = str(round(percent / 10.0) * 10.0) + '%'
                        else:
                            print('No literacy female')
                    else:
                        print("No People and Society/Literacy")

                    if 'Economy' in json_data and 'Unemployment rate' in json_data['Economy']:
                        unemployment = json_data['Economy']['Unemployment rate']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", unemployment)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = float(percent)
                            data['unemployment'] = str(round(percent / 10.0) * 10.0) + '%'
                    else:
                        print('No Economy/Unemployment rate')

                    if 'Economy' in json_data and 'Population below poverty line' in json_data['Economy']:
                        poverty_line = json_data['Economy']['Population below poverty line']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", poverty_line)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = float(percent)
                            data['poverty_line'] = str(round(percent / 10.0) * 10.0) + '%'
                    else:
                        print('No Economy/Population below poverty line')

            else:
                print('Warning, no factbook json for...')
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