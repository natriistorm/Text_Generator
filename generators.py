import re
import random

#BASIC_GENERATORS

def generator_trigrams(trigrams: dict, size: int):
    possible_starts = trigrams["<s> <s>"]
    start_word = random.choice(possible_starts)
    while start_word == '':
        start_word = random.choice(possible_starts)
    sent = str()
    sent += start_word + " "
    start_trigrams = trigrams[f"<s> {start_word}"]
    current_tail = random.choice(start_trigrams)
    word_cnt = 1
    while word_cnt != size:
        while word_cnt != size:
            sent += current_tail + " "
            word_cnt += 1
            next_tails = trigrams.get(f"{start_word} {current_tail}")
            if next_tails is None:
                sent = str()
                word_cnt = 0
                start_word = random.choice(possible_starts)
                sent += start_word + " "
                word_cnt += 1
                current_tail = random.choice(trigrams[f"<s> {start_word}"])
            else:
                start_word = current_tail
                current_tail = random.choice(next_tails)
            if current_tail == "</s>":
                sent = str()
                word_cnt = 0
                start_word = random.choice(possible_starts)
                sent += start_word + " "
                word_cnt += 1
                current_tail = random.choice(trigrams[f"<s> {start_word}"])
    return sent

def generator_bigrams(bigrams: dict, size):
    possible_starts = bigrams["<s>"]
    start_word = random.choice(possible_starts)
    while start_word == '':
        start_word = random.choice(possible_starts)
    sent = str()
    sent += start_word + " "
    current_tail = random.choice(bigrams[start_word])
    word_cnt = 1
    while word_cnt != size:
        sent += current_tail + " "
        word_cnt += 1
        next_tails = bigrams.get(current_tail)
        if next_tails is None:
            sent = str()
            word_cnt = 0
            start_word = random.choice(possible_starts)
            sent += start_word + " "
            word_cnt += 1
            current_tail = random.choice(bigrams[start_word])
        else:
            current_tail = random.choice(next_tails)
        if current_tail == "</s>":
            sent = str()
            word_cnt = 0
            start_word = random.choice(possible_starts)
            sent += start_word + " "
            word_cnt += 1
            current_tail = random.choice(bigrams[start_word])
    return sent

def generator_unigrams(unigrams: list):
    sent = str()
    start_word = random.choice(unigrams)
    while (start_word == "</s>"):
        start_word = random.choice(unigrams)
    if re.match(r'\S*</s>$', start_word):
        start_word = start_word[:-4]
    elif re.match(r'^<s>\S*', start_word):
        start_word = start_word[3:]
    sent += start_word + " "
    current_tail = random.choice(unigrams)
    while current_tail != "</s>" and not current_tail.endswith("</s>"):
        if re.match(r'^<s>\S*', current_tail):
            current_tail = current_tail[3:]
        sent += current_tail + " "
        current_tail = random.choice(unigrams)
    return sent


def smart_generator(chains: dict):
    possible_starts = chains["<s> <s>"]
    keys = list(possible_starts.keys())
    start_word = random.choice(keys)
    sent = str()
    sent += start_word + " "
    start_trigrams = chains[f"<s> {start_word}"]
    current_tail = max(start_trigrams, key=start_trigrams.get)
    while current_tail != "</s>":
        sent += current_tail + " "
        next_tails = chains.get(f"{start_word} {current_tail}")
        if next_tails is None:
            for i in range(3):
                temp_current_tail = max(possible_starts, key=possible_starts.get)
                next_tails = chains.get(f"{start_word} {temp_current_tail}")
                if next_tails is not None:
                    break
            else:
                break
        possible_starts = chains[f"{start_word} {current_tail}"]
        start_word = current_tail
        current_tail = max(next_tails, key=next_tails.get)
    return sent