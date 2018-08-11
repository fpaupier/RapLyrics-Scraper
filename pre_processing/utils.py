#!/usr/bin/python
# -*- coding: utf8 -*-

from collections import Counter


def occurences_counter(filepath, writepath='counts.txt'):
    """Counts occurences of words in a dataset
    Input:
        filepath: file to open
        writepath: file where is written the result of the count, format is:  key | count
    Output:
        Counter dictionary object filled with occurences found in the file opened
    """
    c = Counter()
    with open(filepath,'r') as dataset:
        for line in dataset:
            c.update(line.split())
    with open(writepath,encoding="utf-8-sig", mode='w') as output:
        for k,v in c.items():
            output.write('{}|{}\n'.format(k, v)) #TRY TO USE A SEPARATOR THAT IS NOT PRESENT IN TEXT
    #return the counter anyway, print the writepath
    print("counts saved to: " + writepath +"\nOpen it in excel to sort it and have a quick view" )
    return c


"""The 3 following functions are used after preprocessing a raw dataset."""
#TODO doccument these functions, add purpose

def text2lower(filepath):
    with open(filepath,'r') as dataset:
        lines = [line.lower() for line in dataset]
        print(lines[:3])
        with open(filepath + "_lowered",'w+') as dataset_lowered:
            dataset_lowered.writelines(lines)

def bad_words_remover(filepath,bad_words):
    with open(filepath) as oldfile, open(filepath + "_badwordsremoved", 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                newfile.write(line)

def bad_words_getter(occurences, occurences_min=2):
    """From a dictionnary, returns in a list all keys with lower value than the minimum given in input """
    """In the context: returns all words that appears less than the minimum given"""
    bad_words = []
    for key,value in occurences.items():
        if value < occurences_min:
            bad_words.append(key)
    return bad_words

#occurences_counter('test.txt')
