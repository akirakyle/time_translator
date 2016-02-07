from ast import literal_eval
import re
import requests
from pywsd import disambiguate
from pywsd.similarity import max_similarity as maxsim

# thanks to github.com/econpy/google-ngrams for this function to get ngrams
# from google's servers
def getNgrams(query,  startYear, endYear, smoothing, is_case_insensitive):
    the_corpus = 'eng_2012'
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=the_corpus, smoothing=smoothing,
                  case_insensitive=is_case_insensitive)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    #print req, req.text
    # req.url for url
    res = re.findall('var data = (.*?);\\n', req.text)
    if res:
        data = {qry['ngram']: qry['timeseries'] for qry in literal_eval(res[0])}
        #data['year'] = list(range(startYear, endYear+1))
    else:
        print('failed to get data')
    return data

#query = 'hello,goodbye'
#print(res)

def getNgramsWrapper(words, year):
    startYear, endYear, smoothing, caseInsensitive = 1800, 2000, 3, False
    all = getNgrams(words,startYear,endYear,smoothing,caseInsensitive)
    for word in all:
        all[word] = all[word][year-startYear]
    return all

def translate(text, year):
    parsing = disambiguate(text)

    translated = []
    for word in parsing:
        if word[-1] is not None:
            #synms = getNgramsWrapper(','.join(word[-1].lemma_names()), year)
            print ','.join(word[-1].lemma_names())
            print
            synms = {"hi":"bye"}
            maxWord = synms.keys()[0]
            max = synms.values()[0]
            for synm in synms:
                if synms[synm] > max:
                    max = synms[synm]
                    maxWord = synm
            translated.append(maxWord)
        else:
            translated.append(word[0])
    return " ".join(translated)

test = 'The quick brown fox jumped over the lazy dog'
print translate(test, 1850)
print translate(test, 1900)
print translate(test, 1930)
print translate(test, 1960)
print translate(test, 1990)

starWars = """
It is a period of civil war. Rebel spaceships, striking from a hidden base,
have won their first victory against the evil Galactic Empire.
During the battle, Rebel spies managed to steal secret plans to the
Empire's ultimate weapon, the DEATH STAR, an armored space station with enough
power to destroy an entire planet.
Pursued by the Empire's sinister agents, Princess Leia races home aboard
her starship, custodian of the stolen plans that can save her people and
restore freedom to the galaxy....
"""
#print translate(starWars)
