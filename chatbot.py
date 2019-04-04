#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:33:38 2019

@author: pveronezi
"""

import numpy as np
import tensorflow as tf
import re
import time

# Corpus downloaded at: https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

id2line = {}

for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]

conversations_ids = []

for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))

questions = []
answers = []

for ci in conversations_ids:
    for i in range(len(ci) - 1):
        questions.append(id2line[ci[i]])
        answers.append(id2line[ci[i + 1]])


def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"[-()\"#/@<>;:{}+=~|.?,!]", "", text)
    return text


clean_question = []
clean_answers = []
for q in questions:
    clean_question.append(clean_text(q))
for a in answers:
    clean_answers.append(clean_text(a))

word2count = {}

for q in clean_question:
    for w in q.split():
        if w not in word2count:
            word2count[w] = 1
        else:
            word2count[w] += 1

for a in clean_answers:
    for w in a.split():
        if w not in word2count:
            word2count[w] = 1
        else:
            word2count[w] += 1


threshold = 20
qwords2int = {}
word_number = 0

for w, c in word2count.items():
    if c >= threshold:
        qwords2int[w] = word_number
        word_number += 1

awords2int = {}
word_number = 0

for w, c in word2count.items():
    if c >= threshold:
        awords2int[w] = word_number
        word_number += 1

tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

for t in tokens:
    qwords2int[t] = len(qwords2int) + 1

for t in tokens:
    awords2int[t] = len(awords2int) + 1

aint2word = {w_i: w for w, w_i in awords2int.items()}

for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'

# for i in range(len(clean_question)):
#    clean_question[i] += ' <EOS>'

q2int = []
for q in clean_question:
    ints = []
    for w in q.split():
        if w not in qwords2int:
            ints.append(qwords2int['<OUT>'])
        else:
            ints.append(qwords2int[w])
    q2int.append(ints)

a2int = []
for a in clean_answers:
    ints = []
    for w in a.split():
        if w not in awords2int:
            ints.append(awords2int['<OUT>'])
        else:
            ints.append(awords2int[w])
    a2int.append(ints)

sort_clean_questions = []
sort_clean_answers = []

for l in range(1, 26):
    for i in enumerate(q2int):
        if len(i[1]) == l:
            sort_clean_questions.append(q2int[i[0]])
            sort_clean_answers.append(a2int[i[0]])


