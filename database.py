import json
import requests


def run():
    cl = get_countries_list()
    a3c_to_country = a3c_to_country_dict(cl)

    for country, country_a2c, country_a3c in cl:
        file = 'data/' + str(country_a2c) + '.json'
        print(file)
        with open(file, 'w') as outfile:
            url = 'https://restcountries.eu/rest/v2/alpha/' + country_a2c
            response = requests.get(url)
            json_data = json.loads(response.content.decode('utf-8'))

            data = {}
            data['capital'] = json_data['capital']
            data['population'] = json_data['population']
            data['region'] = json_data['region']
            data['latlng'] = json_data['latlng']

            borders = json_data['borders']
            if len(borders) == 1:
                str_borders = borders[0]
            elif len(borders) == 2:
                str_borders = borders[0] + " and " + borders[1]
            else:
                for i in range(len(borders)):
                    borders[i] = a3c_to_country[borders[i]]

                str_borders = ', '.join(borders[:-1])
                str_borders = str_borders + ", and " + borders[-1]

            data['borders'] = str_borders


            json.dump(data, outfile)

        break





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