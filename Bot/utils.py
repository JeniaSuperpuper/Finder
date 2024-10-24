import re
from difflib import SequenceMatcher



def regist_func(text, word:str ):
    res = []
    string = re.split(r'[.?!;]', text)
    for i in string:
        if word.lower() in i.lower():
            res.append(i)
    return res

def accurate_search_func(text, word):
    sentences = re.split(r'(?<=[.!?]) +', text)

    # Функция для проверки сходства слов
    def is_similar(a, b, threshold=0.7):
        return SequenceMatcher(None, a, b).ratio() >= threshold

    # Ищем предложения с введенным словом или его близким вариантом
    found_sentences = []
    for sentence in sentences:
        # Разделяем предложение на слова
        words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())

        # Проверяем, есть ли слово в предложении или его близкий вариант
        if word.lower() in words_in_sentence or any(is_similar(word.lower(), w) for w in words_in_sentence):
            found_sentences.append(sentence)
    return found_sentences

def error_count_func(text, word):
    res = accurate_search_func(text, word)
    res = len(res)
    return res


#Основная функция
def finder(text, word, regist, accurate_search, edit_text, all_texts, many_files):
    res = []
    if many_files == False:
        if regist == True and accurate_search == False:
            res = regist_func(text, word)
        elif accurate_search == True and edit_text == False:
            res = accurate_search_func(text, word)
        elif edit_text == True:
            errors = error_count_func(text, word)
            res = accurate_search_func(text, word)
            res.append(f'\nНайдено ошибок: {errors}')
        else:
            string = re.split(r'[.?!;]', text)
            for i in string:
                if word in i:
                    res.append(i)
    else:
        if regist == True and accurate_search == False:
            s = ''
            for i in all_texts:
                s += i + ' '
            res = regist_func(s, word)
        elif accurate_search == True:
            s = ''
            for i in all_texts:
                s += i + ' '
            res = accurate_search_func(s, word)
        elif edit_text == True:
            s = ''
            for i in all_texts:
                s += i + ' '
            errors = error_count_func(s, word)
            res.append(f'Найдено ошибок: {errors}')
        else:
            s = ''
            for i in all_texts:
                s += i + ' '
            string = re.split(r'[.?!]', s)
            for i in string:
                if word in i:
                    res.append(i)
    return res



def replace_text(text:str, find_word, replace_word):
    res = []
    if find_word in text:
        res = text.replace(find_word, replace_word)
    return res

def replace_first_word(text:str, find_word, replace_word):
    res = []
    if find_word in text:
        res = text.replace(find_word, replace_word, 1)
    return res

def replace_last_word(text:str, find_word, replace_word):
    res = []
    text = text[::-1]
    if find_word[::-1] in text:
        res = text.replace(find_word[::-1], replace_word[::-1], 1)
    res = res[::-1]
    return res

def replace_first_word_amount(text:str, find_word, replace_word, another_amount):
    res = []
    if find_word in text:
        res = text.replace(find_word, replace_word, another_amount)
    return res

def replace_last_word_amount(text:str, find_word, replace_word, another_amount):
    res = []
    text = text[::-1]
    if find_word[::-1] in text:
        res = text.replace(find_word[::-1], replace_word[::-1], another_amount)
    res = res[::-1]
    return res
