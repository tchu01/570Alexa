import json
import requests
import os
import re

'''
Notes regarding database:
- database should be for one topic (ie: countries), and is composed of individual choices (ie: China, United States)
- each individual choice is saved as a json
- for each json, keys represent question type and values represent the answers (stored in a list)

To add question to database:
- create a question and answer template inside questions.json, where the key is the same key as the one in the database
  and the value is a list containing the question template and then the answer template
- create a dictionary of dictionaries, where the key is the choice to update, and the value is a dictionary of extra answers
'''


def parse():
    rest_countries = parse_rest_countries()
    append_database(rest_countries)

    print('Done adding rest countries')

    wfb = parse_wfb()
    append_database(wfb)


def append_database(dict):
    for key in dict.keys():
        new_data = dict[key]

        file = "data/" + key + ".json"
        if os.path.isfile(file) == True:
            with open(file, encoding='utf-8') as read:
                jsd = json.load(read)
                new_data.update(jsd)

        with open(file, "w", encoding='utf-8') as out:
            json.dump(new_data, out)


def parse_rest_countries():
    cl = get_countries_list()
    a3c_to_country = a3c_to_country_dict(cl)

    ret = {}
    for country, country_a2c, country_a3c in sorted(cl):
        print(country_a2c)
        data = {}

        url = 'https://restcountries.eu/rest/v2/alpha/' + country_a2c
        response = requests.get(url)
        jsd = json.loads(response.content.decode('utf-8', 'ignore'))

        data['country'] = [country]

        if 'alpha2Code' in jsd:
            data['alpha2Code'] = [jsd['alpha2Code']]
        if 'alpha3Code' in jsd:
            data['alpha3Code'] = [jsd['alpha3Code']]
        if 'area' in jsd:
            val = jsd['area']
            if val is not None:
                data['area'] = [str(int(val)) + ' kilometers squared']
        if 'borders' in jsd:
            borders = jsd['borders']
            if len(borders) > 0:
                str_borders = jsd['borders']
                str_borders = [a3c_to_country[a3c] for a3c in str_borders]
                data['borders'] = str_borders
        if 'capital' in jsd:
            data['capital'] = [jsd['capital']]
        if 'languages' in jsd:
            languages = jsd['languages']
            if len(languages) > 0:
                languages = [lang_dict['name'] for lang_dict in languages]
                data['languages'] = languages
        if 'latlng' in jsd:
            if len(jsd['latlng']) == 2:
                data['latlng'] = [str(jsd['latlng'][0]) + ', ' + str(jsd['latlng'][1])]
        if 'population' in jsd:
            val = jsd['population']
            if val is not None:
                data['population'] = [int(val)]
        if 'region' in jsd:
            data['region'] = [jsd['region']]

        ret[country_a2c] = data

    return ret


def parse_wfb():
    cl = get_countries_list()

    ret = {}
    for country, country_a2c, country_a3c in sorted(cl):
        print(country_a2c)
        data = {}

        factbook_file = os.path.abspath('_data/' + str(country_a2c).lower() + '.json')
        if os.path.isfile(factbook_file) == True:
            with open(factbook_file, encoding='utf-8') as reader:
                jsd = json.load(reader)

                if 'Geography' in jsd and 'Area' in jsd['Geography']:
                    if 'land' in jsd['Geography']['Area']:
                        val = jsd['Geography']['Area']['land']['text']
                        land = re.match("((\d*|\d*,)*) sq km", val)
                        if land is not None:
                            land = land.group(1)
                            land = land.replace(',', '')
                            land = int(float(land))
                            # data['land'] = round(land / 1000.0) * 1000.0
                            data['land'] = [str(land) + ' kilometers squared']
                        else:
                            print('No land')
                    if 'water' in jsd['Geography']['Area']:
                        val = jsd['Geography']['Area']['water']['text']
                        water = re.match("((\d*|\d*,)*) sq km", val)
                        if water is not None:
                            water = water.group(1)
                            water = water.replace(',', '')
                            water = int(float(water))
                            # data['water'] = round(water / 1000.0) * 1000.0
                            data['water'] = [str(water) + ' kilometers squared']
                        else:
                            print('No water')
                else:
                    print("No Geography/Area")

                if 'Geography' in jsd and 'Coastline' in jsd['Geography']:
                    if 'text' in jsd['Geography']['Coastline']:
                        val = jsd['Geography']['Coastline']['text']
                        coastline = re.match("((\d*|\d*,)*) km", val)
                        if coastline is not None:
                            coastline = coastline.group(1)
                            coastline = coastline.replace(',', '')
                            coastline = int(float(coastline))
                            data['coastline'] = [str(coastline) + ' kilometers']
                    else:
                        print('No coastline')
                else:
                    print("No Geography/Coastline")

                if 'Geography' in jsd and 'Climate' in jsd['Geography']:
                    if 'text' in jsd['Geography']['Climate']:
                        data['climate'] = [jsd['Geography']['Climate']['text']]
                    else:
                        keys = list(jsd['Geography']['Climate'].keys())
                        data['climate'] = [jsd['Geography']['Climate'][keys[0]]['text']]
                else:
                    print("No Geography/Climate")

                if 'Geography' in jsd and 'Natural resources' in jsd['Geography']:
                    if 'text' in jsd['Geography']['Natural resources']:
                        val = jsd['Geography']['Natural resources']['text']
                        val = val.split(',')
                        val = [x.strip(' ') for x in val]
                        data['natural_resources'] = val
                    else:
                        print("No natural resources")
                else:
                    print("No Geography/Natural resources")

                if 'People and Society' in jsd and 'Ethnic groups' in jsd['People and Society']:
                    if 'text' in jsd['People and Society']['Ethnic groups']:
                        val = jsd['People and Society']['Ethnic groups']['text']
                        val = val.split(',')
                        val = [x.strip(' ').split(' ')[0] for x in val]
                        if 'other' in val:
                            val.remove('other')
                        if 'unspecified' in val:
                            val.remove('unspecified')
                        if 'and' in val:
                            val.remove('and')

                        data['ethnic_groups'] = val
                    else:
                        print("No ethnic groups")
                else:
                    print("No People and Society/Ethnic groups")

                if 'People and Society' in jsd and 'Median age' in jsd['People and Society']:
                    median_age_male = jsd['People and Society']['Median age']['male']['text']
                    age = re.match("(\d*|\d*\.\d*) years", median_age_male)
                    if age is not None:
                        age = age.group(1)
                        age = int(float(age))
                        # data['median_age_male'] = round(age / 10.0) * 10.0
                        data['median_age_male'] = [str(age) + ' years']
                    else:
                        print('No median age male')

                    median_age_female = jsd['People and Society']['Median age']['female']['text']
                    age = re.match("(\d*|\d*\.\d*) years", median_age_female)
                    if age is not None:
                        age = age.group(1)
                        age = int(float(age))
                        # data['median_age_female'] = round(age / 10.0) * 10.0
                        data['median_age_female'] = [str(age) + ' years']
                    else:
                        print('No median age female')
                else:
                    print("No People and Society/Median Age")

                if 'People and Society' in jsd and 'Population growth rate' in jsd['People and Society']:
                    pop_growth_rate = jsd['People and Society']['Population growth rate']['text']
                    percent = re.match("(-?(\d*|\d*\.\d*))\%", pop_growth_rate)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        data['pop_growth_rate'] = [str(percent) + '%']
                    else:
                        print('No population growth rate')
                else:
                    print("No People and Society/Population growth rate")

                if 'People and Society' in jsd and 'Life expectancy at birth' in jsd['People and Society']:
                    life_expectancy_male = jsd['People and Society']['Life expectancy at birth']['male']['text']
                    age = re.match("(\d*|\d*\.\d*) years", life_expectancy_male)
                    if age is not None:
                        age = age.group(1)
                        age = int(float(age))
                        # data['life_expectancy_male'] = round(age / 10.0) * 10.0
                        data['life_expectancy_male'] = [str(age) + ' years']
                    else:
                        print('No life expectancy male')

                    life_expectancy_female = jsd['People and Society']['Life expectancy at birth']['female']['text']
                    age = re.match("(\d*|\d*\.\d*) years", life_expectancy_female)
                    if age is not None:
                        age = age.group(1)
                        age = int(float(age))
                        # data['life_expectancy_female'] = round(age / 10.0) * 10.0
                        data['life_expectancy_female'] = [str(age) + ' years']
                    else:
                        print('No life expectancy female')
                else:
                    print("No People and Society/Life expectancy at birth")

                if 'People and Society' in jsd and 'Health expenditures' in jsd['People and Society']:
                    health_expenditures = jsd['People and Society']['Health expenditures']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", health_expenditures)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        data['health_expenditures'] = [str(percent) + '%']
                    else:
                        print('No health expenditures')
                else:
                    print("No People and Society/Health expenditures")

                if 'People and Society' in jsd and 'Obesity - adult prevalence rate' in jsd['People and Society']:
                    obesity = jsd['People and Society']['Obesity - adult prevalence rate']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", obesity)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        data['obesity'] = [str(percent) + '%']
                    else:
                        print('No obesity')
                else:
                    print("No People and Society/Obesity - adult prevalence rate")

                if 'People and Society' in jsd and 'Education expenditures' in jsd['People and Society']:
                    health_expenditures = jsd['People and Society']['Education expenditures']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", health_expenditures)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        data['education_expenditures'] = [str(percent) + '%']
                    else:
                        print('No education expenditures')
                else:
                    print("No People and Society/Education expenditures")

                if 'People and Society' in jsd and 'Literacy' in jsd['People and Society']:
                    literacy_male = jsd['People and Society']['Literacy']['male']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", literacy_male)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        # data['literacy_male'] = round(percent / 10.0) * 10.0
                        data['literacy_male'] = [str(percent) + '%']
                    else:
                        print('No literacy male')

                    literacy_female = jsd['People and Society']['Literacy']['male']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", literacy_female)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        # data['literacy_female'] = round(percent / 10.0) * 10.0
                        data['literacy_female'] = [str(percent) + '%']
                    else:
                        print('No literacy female')
                else:
                    print("No People and Society/Literacy")

                if 'Economy' in jsd and 'GDP - real growth rate' in jsd['Economy']:
                    gdp_growth = jsd['Economy']['GDP - real growth rate']['text']
                    percent = re.match("(-?(\d*|\d*\.\d*))\%", gdp_growth)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        # data['unemployment'] = round(percent / 10.0) * 10.0
                        data['gdp_growth_rate'] = [str(percent) + '%']
                    else:
                        print("No gdp real growth rate")
                else:
                    print('No Economy/GDP - real growth rate')

                if 'Economy' in jsd and 'GDP - per capita (PPP)' in jsd['Economy']:
                    gdp_per_capita = jsd['Economy']['GDP - per capita (PPP)']['text']
                    dollar = re.match("\$(\d*|\d*\.\d*)", gdp_per_capita)
                    if dollar is not None:
                        dollar = dollar.group(1)
                        dollar = int(float(dollar))
                        # data['unemployment'] = round(percent / 10.0) * 10.0
                        data['gdp_per_capita'] = ['$' + str(dollar)]
                    else:
                        print("No gdp per capita")
                else:
                    print('No Economy/GDP - per capita (PPP)')

                if 'Economy' in jsd and 'Agriculture - products' in jsd['Economy']:
                    if 'text' in jsd['Economy']['Agriculture - products']:
                        val = jsd['Economy']['Agriculture - products']['text']
                        val = val.split(',')
                        val = [x.strip(' ') for x in val]
                        data['agriculture'] = val
                    else:
                        print("No agriculture")
                else:
                    print('No Economy/Agriculture - products')

                if 'Economy' in jsd and 'Industries' in jsd['Economy']:
                    if 'text' in jsd['Economy']['Industries']:
                        val = jsd['Economy']['Industries']['text']
                        val = val.split(',')
                        val = [x.strip(' ') for x in val]
                        data['industries'] = val
                    else:
                        print("No industries")
                else:
                    print('No Economy/industries')

                if 'Economy' in jsd and 'Unemployment rate' in jsd['Economy']:
                    unemployment = jsd['Economy']['Unemployment rate']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", unemployment)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        # data['unemployment'] = round(percent / 10.0) * 10.0
                        data['unemployment'] = [str(percent) + '%']
                    else:
                        print("No unemployment rate")
                else:
                    print('No Economy/Unemployment rate')

                if 'Economy' in jsd and 'Population below poverty line' in jsd['Economy']:
                    poverty_line = jsd['Economy']['Population below poverty line']['text']
                    percent = re.match("(\d*|\d*\.\d*)\%", poverty_line)
                    if percent is not None:
                        percent = percent.group(1)
                        percent = int(float(percent))
                        # data['poverty_line'] = round(percent / 10.0) * 10.0
                        data['poverty_line'] = [str(percent) + '%']
                    else:
                        print("No population below poverty line")
                else:
                    print('No Economy/Population below poverty line')

                if 'Economy' in jsd and 'Exports - commodities' in jsd['Economy']:
                    if 'text' in jsd['Economy']['Exports - commodities']:
                        val = jsd['Economy']['Exports - commodities']['text']
                        val = val.split(',')
                        val = [x.strip(' ') for x in val]
                        data['exports'] = val
                    else:
                        print("No exports")
                else:
                    print('No Economy/exports')

                if 'Economy' in jsd and 'Imports - commodities' in jsd['Economy']:
                    if 'text' in jsd['Economy']['Imports - commodities']:
                        val = jsd['Economy']['Imports - commodities']['text']
                        val = val.split(',')
                        val = [x.strip(' ') for x in val]
                        data['imports'] = val
                    else:
                        print("No imports")
                else:
                    print('No Economy/imports')

            ret[country_a2c] = data

        else:
            print('Warning, no factbook json for...')
            print(country)
            print(country_a2c)
            print(country_a3c)
            print()

    return ret


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
                if val is not None:
                    # data['population'] = round(val / 1000000.0) * 1000000.0
                    data['population'] = int(float(val))
            if 'region' in json_data:
                data['region'] = json_data['region']
            if 'area' in json_data:
                val = json_data['area']
                if val is not None:
                    # data['area'] = round(val / 1000.0) * 1000.0
                    data['area'] = str(int(float(val))) + ' kilometers squared'
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
                                land = int(float(land))
                                # data['land'] = round(land / 1000.0) * 1000.0
                                data['land'] = str(land) + ' kilometers squared'
                            else:
                                print('No land')
                        if 'water' in json_data['Geography']['Area']:
                            val = json_data['Geography']['Area']['water']['text']
                            water = re.match("(\d*|\d*.\d*) sq km", val)
                            if water is not None:
                                water = water.group(1)
                                water = water.replace(',', '')
                                water = int(float(water))
                                # data['water'] = round(water / 1000.0) * 1000.0
                                data['water'] = str(water) + ' kilometers squared'
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
                            age = int(float(age))
                            # data['median_age_male'] = round(age / 10.0) * 10.0
                            data['median_age_male'] = str(age) + ' years'
                        else:
                            print('No median age male')

                        median_age_female = json_data['People and Society']['Median age']['female']['text']
                        age = re.match("(\d*|\d*.\d*)", median_age_female)
                        if age is not None:
                            age = age.group(1)
                            age = int(float(age))
                            # data['median_age_female'] = round(age / 10.0) * 10.0
                            data['median_age_female'] = str(age) + ' years'
                        else:
                            print('No median age female')
                    else:
                        print("No People and Society/Median Age")

                    if 'People and Society' in json_data and 'Life expectancy at birth' in json_data['People and Society']:
                        life_expectancy_male = json_data['People and Society']['Life expectancy at birth']['male']['text']
                        age = re.match("(\d*|\d*.\d*) years", life_expectancy_male)
                        if age is not None:
                            age = age.group(1)
                            age = int(float(age))
                            # data['life_expectancy_male'] = round(age / 10.0) * 10.0
                            data['life_expectancy_male'] = str(age) + ' years'
                        else:
                            print('No life expectancy male')

                        life_expectancy_female = json_data['People and Society']['Life expectancy at birth']['female']['text']
                        age = re.match("(\d*|\d*.\d*) years", life_expectancy_female)
                        if age is not None:
                            age = age.group(1)
                            age = int(float(age))
                            # data['life_expectancy_female'] = round(age / 10.0) * 10.0
                            data['life_expectancy_female'] = str(age) + ' years'
                        else:
                            print('No life expectancy female')
                    else:
                        print("No People and Society/Life expectancy at birth")

                    if 'People and Society' in json_data and 'Literacy' in json_data['People and Society']:
                        literacy_male = json_data['People and Society']['Literacy']['male']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", literacy_male)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = int(float(percent))
                            # data['literacy_male'] = round(percent / 10.0) * 10.0
                            data['literacy_male'] = str(percent) + '%'
                        else:
                            print('No literacy male')

                        literacy_female = json_data['People and Society']['Literacy']['male']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", literacy_female)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = int(float(percent))
                            # data['literacy_female'] = round(percent / 10.0) * 10.0
                            data['literacy_female'] = str(percent) + '%'
                        else:
                            print('No literacy female')
                    else:
                        print("No People and Society/Literacy")

                    if 'Economy' in json_data and 'Unemployment rate' in json_data['Economy']:
                        unemployment = json_data['Economy']['Unemployment rate']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", unemployment)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = int(float(percent))
                            # data['unemployment'] = round(percent / 10.0) * 10.0
                            data['unemployment'] = str(percent) + '%'
                        print('No Economy/Unemployment rate')

                    if 'Economy' in json_data and 'Population below poverty line' in json_data['Economy']:
                        poverty_line = json_data['Economy']['Population below poverty line']['text']
                        percent = re.match("(\d*|\d*.\d*)\%", poverty_line)
                        if percent is not None:
                            percent = percent.group(1)
                            percent = int(float(percent))
                            # data['poverty_line'] = round(percent / 10.0) * 10.0
                            data['poverty_line'] = str(percent) + '%'
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
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    # second pass
    url = 'https://restcountries.eu/rest/v2/all'
    response = requests.get(url)
    json_data = json.loads(response.content.decode('utf-8', 'ignore'))
    for country in json_data:
        country_list.add((country['name'], country['alpha2Code'], country['alpha3Code']))

    return country_list


def a3c_to_country_dict(countries_list):
    ret = {}
    for country, a2c, a3c in countries_list:
        ret[a3c] = country

    return ret


if __name__ == '__main__':
    # run()
    parse()