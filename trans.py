import os
import sys
sys.path.append('/home/akyle/pywsd')
from pywsd import disambiguate
from pywsd.similarity import max_similarity as maxsim

ngrams_prefix = '/home/akyle/ngram_data/eng_1gram_'

def get_freq(word, date):
    ngram_file = ngrams_prefix + word[0].lower()
    f = open(ngram_file, 'r')
    sum = 0
    for s in f:
        if s[:len(word)] == word:
            row = s.split('\t')
            if int(row[1]) == date:
                sum += int(row[2])
    f.close()
    return sum

def translate(text, year):
    parsing = disambiguate(text)
    print parsing

    translated = []
    for word in parsing:
        if word[-1] is not None:
            print word[-1].lemma_names()
            synms = word[-1].lemma_names()
            maxWord = synms[0]
            max = 0
            for synm in synms:
                freq_count = get_freq(str(synm), year)
                if freq_count > max:
                    max = freq_count
                    maxWord = synm
            translated.append(maxWord)
        else:
            translated.append(word[0])
    print 'input text: ', text
    print
    print "final result: ", ' '.join(translated)
    print
    return ' '.join(translated)

if __name__ == '__main__':
    test = 'The quick brown fox jumped over the lazy dog'
    test2 = 'trump and Rubio have taken flak from competitors as candidates launched an all-out offensive across New Hampshire.'

    #print translate(test2, 1850)

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
    #print ",".join(starWars.split(' '))
    #print translate(starWars)

    #print search("goodbye")
    #print get_freq(search('goodbye'), 1960)
