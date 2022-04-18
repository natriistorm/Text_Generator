from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter
import random
import re


def tokenization():
    filename = "corpus.txt"
    corpus = open(filename, "r", encoding="utf-8").read()
    tk = WhitespaceTokenizer()
    tokenized_corpus = tk.tokenize(corpus)
    trigrams_corpus = trigrams(tokenized_corpus)
    chains = markovChains(trigrams_corpus)
    print(chains)
    #sentenceGenerator(trigrams_corpus, chains, tokenized_corpus)


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
        seq = str()
        if re.match(r'<s>\S*', corpus[i]):
            cropped = corpus[i][3:]
            seq = f"<s> {cropped}"
            if seq not in trigrams_corpus.keys():
                trigrams_corpus[seq] = []
            trigrams_corpus[seq].append(corpus[i + 1])
        elif re.match(r'\S*</s>$', corpus[i]) or re.match(r'<s>\S*', corpus[i + 2]):
            continue
        elif re.match(r'\S*</s>$', corpus[i + 1]):
            cropped = corpus[i][:-4]
            seq = f"{corpus[i]} {cropped}"
            if seq not in trigrams_corpus.keys():
                trigrams_corpus[seq] = []
            trigrams_corpus[seq].append("</s>")
        else:
            seq = f"{corpus[i]} {corpus[i + 1]}"
            if seq not in trigrams_corpus.keys():
                trigrams_corpus[seq] = []
            trigrams_corpus[seq].append(corpus[i + 2])
    return trigrams_corpus

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
