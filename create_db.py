import pandas as pd

ngrams_prefix = '/home/akyle/ngram_data/eng_1gram_'

#ToDo: get data into a Pandas Data frame so that
# perhaps the contains method can be used. See
# (http://pandas.pydata.org/pandas-docs/stable/text.html)
def get_freq(word, date):
    ngram_file = ngrams_prefix + word[0].lower()
    f = open(ngram_file, 'r')
    grams = []
    for s in f:
        grams.append(s.split('\t')[0])
        if s[:len(word)] == word:
            row = s.split('\t')
            if int(row[1]) == date:
                sum += int(row[2])
    f.close()
    pd.Series(
    return sum
