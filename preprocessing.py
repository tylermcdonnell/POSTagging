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
        with open(out, 'wb') as out:
            for sentence in sentences:
                for token in sentence:
                    out.write('%s\n' % token)
                out.write('\n')

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
        with open(out, 'wb') as out:
            for sentence in sentences:
                for token in sentence:
                    out.write('%s\n' % token)
                out.write('\n')
    
    return sentences

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))

# Sample Usage: WSJ directories to single file.
'''
sentences   = []
directories = ['00', '01', '02']
for directory in directories:
    for root, dirs, files in os.walk(directory):
        for wsj_file in files:
            if wsj_file.endswith(".pos"):
                sentences.extend(wsj_to_mallet(os.path.join(root, wsj_file)))
with open('wsj_mallet.pos', 'wb') as out:
    for sentence in sentences:
        for token in sentence:
            out.write('%s\n' % token)
        out.write('\n')
'''

# Sample Usage: ATIS
'''
atis_to_mallet('atis3.pos', 'wsj_mallet.pos')
'''

# Sample Usage: WSJ
'''
wsj_to_mallet('wsj_0001.pos', 'wsj_0001_mallet.pos')
'''
