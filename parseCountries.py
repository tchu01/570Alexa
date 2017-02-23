import json
import requests


def main():
	cl = getCountriesList()
	nl = getNewsList()
	for a in nl:
		#print a
		found = False
		for c in cl: 
			if c in a: 
				print "FOUND: " + c
				found = True
		if not found: 
			#print "Could not find a country :<"
			pass
		#print "\n"


def getNewsList():
	newsList = []
	sourceList = ['bbc-news','cnn','cnbc','google-news','the-huffington-post']
	API_KEY = 'd017adabb56b40d1919976e8206486c2'
	for src in sourceList:
		url = 'https://newsapi.org/v1/articles?source=' + src + '&apiKey=' + API_KEY
		response = requests.get(url)
		jsonData = json.loads(response.content)
		for article in jsonData['articles']: 
			#print article['title']
			#print "\t" + (article['description'] or '')
			articleString = article['title'] + " - " + (article['description'] or '')
			newsList.append(articleString)

	return newsList

def getCountriesList():
	countryList = []
	url = 'https://restcountries.eu/rest/v1/all'
	response = requests.get(url)
	jsonData = json.loads(response.content)
	for country in jsonData:
		#print country['name']
		countryList.append(country['name'])
	return countryList


if __name__ == "__main__":
	main()