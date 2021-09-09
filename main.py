# Write your code here
from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter
import random
import re


def tokenization():
    filename = input()
    corpus = open(filename, "r", encoding="utf-8").read()
    tk = WhitespaceTokenizer()
    tokenized_corpus = tk.tokenize(corpus)
    #bigrams_corpus = bigrams(tokenized_corpus)
    trigrams_corpus = trigrams(tokenized_corpus)
    chains = markovChains(trigrams_corpus)
    sentenceGenerator(chains, trigrams_corpus)


def queries(corpus: list, chains: list):
    current_word = random.choice(corpus)
    for j in range(10):
        sentence = ""
        for i in range(10):
            tails = [tail for tail, _ in chains[current_word]]
            freq_weights = [weight for _, weight in chains[current_word]]
            current_word = random.choices(tails, weights=freq_weights)[0]
            sentence += current_word + " "
        print(sentence)


def trigrams(corpus: list) -> dict:
    trigrams_corpus = {}
    for i in range(len(corpus) - 2):
        if re.match(r'\S*[.?!]$', corpus[i]) or re.match(r'\S*[.?!]$', corpus[i + 1]):
            continue
        trigrams_corpus.setdefault(corpus[i], [])
        trigrams_corpus[corpus[i]].append((corpus[i + 1], corpus[i + 2]))
    return trigrams_corpus


'''
def trigrams(bigrams: dict) -> list:
    trigram = []
    for head in bigrams:
        for tail in bigrams[head]:
            head_trigram = head + " " + tail
            if re.match(r'\S*[.?!]$', tail):
                continue
            for tail_trigram in bigrams[tail]:
                trigram.append((head_trigram, tail_trigram))
    return trigram
'''

'''
def markovChains(ngrams: dict):
    appearances = {}
    for idx in ngrams:
        appearances[idx] = Counter(ngrams[idx])
    chains = {}
    for head in ngrams:
        for tail in ngrams[head]:
            chains.setdefault(head, set())
            chains[head].add((tail, appearances[head][tail]))
    return chains
'''


def markovChains(ngrams: dict):
    appearances = {}
    for idx in ngrams:
        appearances[idx] = Counter(ngrams[idx])
    chains = {}
    for head in ngrams:
        for tail in ngrams[head]:
            chains.setdefault((head,tail[0]), set())
            chains[(head,tail[0])].add((tail[1], appearances[head][tail]))
    return chains


def sentenceGenerator(chains: list, tokens: list):
    sentence_counter = 10
    while sentence_counter > 0:
        brake = False
        sentence = ""
        word_counter = 0
        current_word = random.choice(tokens)
        while not re.match(r'[A-Z]\S*[^.?!]', current_word):
            current_word = random.choice(tokens)
        sentence += current_word
        word_counter += 1
        while not re.match(r'\S*[.?!]$', current_pair[1]):
            tails = [tail for tail, _ in chains[current_pair]]
            freq_weights = [weight for _, weight in chains[current_pair]]
            current_pair = random.choices(tails, weights=freq_weights)
            current_word = current_pair[0][0]
            if re.match(r'[A-Z]', current_word):
                brake = True
                break
            sentence += " " + current_pair[0][0] + " " + current_pair[0][1]
            word_counter += 1
        if word_counter >= 5 and not brake:
            sentence_counter -= 1
            print(sentence)


if __name__ == '__main__':
    tokenization()
