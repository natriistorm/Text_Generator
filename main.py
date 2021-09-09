# Write your code here
from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter
import random
import re


def tokenization():
    filename = "corpus.txt"
    corpus = open(filename, "r", encoding="utf-8").read()
    tk = WhitespaceTokenizer()
    tokenized_corpus = tk.tokenize(corpus)
    #bigrams_corpus = bigrams(tokenized_corpus)
    trigrams_corpus = trigrams(tokenized_corpus)
    chains = markovChains(trigrams_corpus)
    sentenceGenerator(trigrams_corpus, chains, tokenized_corpus)


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


def sentenceGenerator(trigrams: dict, chains: list, tokens: list):
    sentence_counter = 10
    while sentence_counter > 0:
        brake = False
        sentence = ""
        word_counter = 0
        current_word = random.choice(tokens)
        while not re.match(r'[A-Z]\S*[^.?!]', current_word) or trigrams.get(current_word) is None:
            current_word = random.choice(tokens)
        sentence += current_word
        word_counter += 1
        current_tail = random.choice(trigrams[current_word])
        sentence += " " + current_tail[0] + " " + current_tail[1]
        word_counter += 2
        current_three = (current_word, current_tail[0], current_tail[1])
        while not re.match(r'\S*[.?!]$', current_three[2]):
            tails = [tail for tail, _ in chains[current_tail]]
            freq_weights = [weight for _, weight in chains[current_tail]]
            current_word = random.choices(tails, weights=freq_weights)[0]
            if re.match(r'[A-Z]', current_word):
                brake = True
                break
            sentence += " " + current_word
            word_counter += 1
            current_three = (current_tail[0], current_tail[1], current_word)
            current_tail = (current_tail[1], current_word)
        if word_counter >= 5 and not brake:
            sentence_counter -= 1
            print(sentence)


if __name__ == '__main__':
    tokenization()
