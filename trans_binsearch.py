import os
import sys
sys.path.append('/home/akyle/pywsd')
from pywsd import disambiguate
from pywsd.similarity import max_similarity as maxsim

def bin_search_key(val, matchvalue):
    print val
    print val[:len(matchvalue)]
    return val[:len(matchvalue)]

# thanks to www.grantjenks.com/wiki/random/python_binary_search_file_by_line
# for this binary search implementation. Unfortunately version2 of the
# google ngram corpus isn't strictly lexographically ordered
def line_binary_search(filename, matchvalue, key=lambda val: val):
    """
    Binary search a file for matching lines.
    Returns a list of matching lines.
    filename - path to file, passed to 'open'
    matchvalue - value to match
    key - function to extract comparison value from line

    >>> parser = lambda val: int(val.split('\t')[0].strip())
    >>> line_binary_search('sd-arc', 63889187, parser)
    ['63889187\t3592559\n', ...]
    """

    # Must be greater than the maximum length of any line.

    max_line_len = 120

    start = pos = 0
    end = os.path.getsize(filename)

    with open(filename, 'rb') as fptr:

        # Limit the number of times we binary search.

        for rpt in xrange(1000):

            last = pos
            pos = start + ((end - start) / 2)
            fptr.seek(pos)

            # Move the cursor to a newline boundary.

            fptr.readline()

            line = fptr.readline()
            linevalue = key(line,matchvalue)

            if linevalue == matchvalue or pos == last:

                # Seek back until we no longer have a match.

                while True:
                    fptr.seek(-max_line_len, 1)
                    fptr.readline()
                    if matchvalue != key(fptr.readline(), matchvalue):
                        break

               # Seek forward to the first match.

                for rpt in xrange(max_line_len):
                    line = fptr.readline()
                    linevalue = key(line, matchvalue)
                    if matchvalue == linevalue:
                        break
                else:
                    # No match was found.

                    return []

                results = []

                while linevalue == matchvalue:
                    results.append(line)
                    line = fptr.readline()
                    linevalue = key(line, matchvalue)

                return results
            elif linevalue < matchvalue:
                start = fptr.tell()
            else:
                assert linevalue > matchvalue
                end = fptr.tell()
        else:
            raise RuntimeError('binary search failed')

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

    word = 'goodbye'
    ngram_file = ngrams_prefix + word[0].lower()
    print line_binary_search(ngram_file, word, bin_search_key)
