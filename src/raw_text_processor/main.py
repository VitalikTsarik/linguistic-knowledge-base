import os
import re

from constants import RAW_DIR_PATH, PROCESSED_DIR_PATH

if __name__ == '__main__':
    for filename in os.listdir(RAW_DIR_PATH):
        with open(os.path.join(PROCESSED_DIR_PATH, filename), 'w') as raw_file:
            with open(os.path.join(RAW_DIR_PATH, filename), 'r', encoding='utf-8', errors='ignore') as processed_file:
                for line in processed_file:
                    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!])', line)
                    for sentence in sentences:
                        sentence = sentence.strip(' .?!"\'\n')
                        sentence = sentence.replace('..', '')
                        sentence = sentence.replace('--', '')
                        if len(sentence) < 2:
                            continue
                        sentence = sentence[0].lower() + sentence[1:]
                        sentence = re.sub(r'[^A-Za-z\' .-]', '', sentence)
                        sentence = re.sub(r' +', ' ', sentence)
                        words = sentence.split(' ')
                        for word in words:
                            word = word.strip('\' -')
                            if word != '':
                                if len(word) > 1 and not re.search(r'[A-Z]+[a-z]+$', word):
                                    word = word.lower()
                                raw_file.write(f'{word}\n')
