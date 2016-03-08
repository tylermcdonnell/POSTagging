'''
@author Tyler McDonnell

Converts POS tags to the Mallet format.

Supports two datasets:

1. Airline Travel Information Service (ATIS)
2. Wall Street Journal (WSJ)

Mallet requires input data to contain one word word and label
per line, space sparated, with a blank line between sentences.

e.g.,

List VB
the DT
flights NNS
from IN
Baltimore NNP
to TO
Seattle NNP
that WDT
stop VBP
in IN
Minneapolis NNP


Does VBZ
this DT
flight NN
serve VB
dinner NN
'''

import os
import copy

def atis_to_mallet(atis, out=None):
    sentence_boundary = '======================================'
    current           = []
    sentences         = []
    # True when we are reading lines between two boundaries.
    sentence          = False

    for line in [line.rstrip('\n') for line in open(atis)]:
        if line == sentence_boundary:
            if not sentence:
                if current:
                    sentences.append(current)
                current = []
            sentence = not sentence
        elif sentence:
            tokens = line.replace('[','').replace(']','').strip().split()
            for token in tokens:
                word = token.split('/')[0]
                pos  = token.split('/')[1]
                current.append('%s %s' % (word, pos))

    # We should not end in the middle of a sentence.
    assert(not sentence)

    if out:
        mallet_to_file(sentences)

    return sentences    

def wsj_to_mallet(wsj, out=None):
    sentence_boundary = '======================================'
    current           = []
    sentences         = []

    for line in [line.rstrip('\n') for line in open(wsj)]:
        if line == sentence_boundary:
            if current:
                sentences.append(current)
            current = []
        else:
            tokens = line.replace('[','').replace(']','').strip().split()
            for token in tokens:
                word = token.split('/')[0]
                pos  = token.split('/')[1]
                current.append('%s %s' % (word, pos))

                # Sometimes WSJ's sentence boundaries aren't perfect.
                if word == '.':
                    sentences.append(current)
                    current = []

    if out:
        mallet_to_file(sentences)
    
    return sentences

##################################################
# Orthographic Features                          #
##################################################

def of_caps(word):
    return "caps" if (word[0].isupper()) else ""

def of_ends_in_s(word):
    return "s" if (word.endswith('s')) else ""

def of_ends_in_ing(word):
    return "ing" if (word.endswith('ing')) else ""

def of_ends_in_ly(word):
    return 'ly' if (word.endswith('ly')) else ""

def of_contains_hyphen(word):
    return 'hyphen' if ('-' in word) else ""

def of_starts_with_number(word):
    return 'number' if (word[0].isdigit()) else ""

def of_ends_in_ed(word):
    return 'past' if (word.endswith('ed')) else ""

def of_ends_in_er_or(word):
    return 'person' if (word.endswith('er') or word.endswith('or')) else ""

def of_ends_in_ion(word):
    return 'act' if (word.endswith('ion')) else ""

def of_ends_in_y(word):
    return 'characterizer' if (word.endswith('y')) else ""

def of_ends_in_ment(word):
    return 'state' if (word.endswith('ment')) else ""

def apply_orthographic_features(sentences, *features):
    for sentence in sentences:
        for idx, token in enumerate(sentence):
            word = token.split(' ')[0]
            applicable_features = []
            for feature in features:
                if feature(word):
                    applicable_features.append(feature(word))
            for feature in applicable_features:
                sentence[idx] = token + (" %s" % feature)



def mallet_to_file(sentences, out):
    with open(out, 'wb') as out:
        for sentence in sentences:
            for token in sentence:
                out.write('%s\n' % token)
            out.write('\n')
        

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))

sentences   = []
'''
directories = ['00', '01', '02', '03', '04',
               '05', '06', '07', '08', '09',
               '10', '11', '12', '13', '14',
               '15', '16', '17', '18', '19', 
               '20', '21', '22', '23', '24']
'''

# Sample UsagE: Apply features to ATIS dataset.
'''
sentences = atis_to_mallet('atis3.pos')
features = [of_caps,
            of_ends_in_s,
            of_ends_in_ing,
            of_ends_in_ly,
            of_contains_hyphen,
            of_starts_with_number,
            of_ends_in_ed,
            of_ends_in_er_or,
            of_ends_in_ion,
            of_ends_in_y,
            of_ends_in_ment]
apply_orthographic_features(sentences, *features)
mallet_to_file(sentences, 'atis_all_features.pos')
'''

# Sample Usage: ATIS
'''
atis_to_mallet('atis3.pos', 'wsj_mallet.pos')
'''

# Sample Usage: WSJ
'''
wsj_to_mallet('wsj_0001.pos', 'wsj_0001_mallet.pos')
'''
