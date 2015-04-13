# Steven Bradley
# CSE 140 AA
# Homework 8

import os
import sys
from collections import defaultdict


#Everything to be removed to clean subtitle text
NON_TEXT =['<i>', '</i>','<font color=#00FF00>','<font color=#00FFFF>'
            ,'<font color="#00ff00">' ,'<font color="#ff0000">','</font>'
            ,'#','-','(',')','\xe2\x99\xaa','www.AllSubs.org','http://DJJ.HOME.SAPO.PT/'
           ,'Downloaded','Shared','Sync','www.addic7ed.com','n17t01','"']

def main():
    check_cmd_args()
    args = sys.argv[1:]
    ##1 - Gram
    #Get word lists from both authetic and test sources
    auth_words1 = get_all_subtexts(args[0], 1)
    test_words1 = get_all_subtexts(args[1], 1)

    #Get word lists frequencies from both authentic and test
    auth_freq1 = frequency_of_words(auth_words1)
    test_freq1 = frequency_of_words(test_words1)

    ##2 - Gram
    #Get word lists from both authetic and test sources
    auth_words2 = get_all_subtexts(args[0], 2)
    test_words = get_all_subtexts(args[1], 2)

    #Get word lists frequencies from both authentic and test
    auth_freq2 = frequency_of_words(auth_words2)
    test_freq2 = frequency_of_words(test_words2)

    

#Compare Vocabulary
#Compare Phrases
    #Bigram output
#Verify solution

def check_cmd_args():
    """
    Checks that there are two arguments given to program.
    Prints helpful tip if wrong and exits program.
    Otherwise prints the given arguments.
    """
    args = sys.argv[1:]
    if len(args) != 2:
        print "Arguments must be valid paths that have only script data files."
        sys.exit()
    else:
        return args

def lineIsSubtext(line):
    """
    Returns True if the given line is a line containing subtext.
    """
    if not (('-->' in line) or (line.strip("\n").isdigit()) or (len(line)==0)):
        return True
    return False

def get_all_subtexts(path, n):
    """
    Goes through all the subtitle data files in the given path and creates a
    list of tuples with n word groupings.
    """
    files = os.listdir(path)
    total_subtexts = []
    for doc in files:
        doc_path = os.path.join(path, doc)
        [total_subtexts.append(word) for word in get_file_subtext(doc_path)]
    grouped_word_list = [el for el in group_words(total_subtexts, n)]
    return grouped_word_list

def group_words(lst, n):
    """
    Takes the given list and creates a new list of tuples that group n elements.
    i.e. when n=1 [1,2,3] --> [(1),(2),(3)]
         when n=2 [1,2,3] --> [(1,2),(2,3)]
         
    """
    grouped_list = []
    for i in range(len(lst)):
        if n ==1:
            group = tuple(lst[i])
        else:
            group = tuple(lst[i:i+1])
        grouped_list.append(group)
    return grouped_list

def get_file_subtext(path):
    """
    Goes through the given file and gets only the subtitle text.
    Returns the subtitle text as a list in which each element
    is one word(String) of subtitle text.
    """
    subtext = []
    subtext_file = open(path)
    for line in subtext_file:
        if lineIsSubtext(line):
            subtext.append(line)
    clean_subtext = clean_subtitle_lines(subtext)
    return clean_subtext
            
def clean_subtitle_lines(subtext):
    """
    Goes through the given list of subtitle text lines and removes the
    elements in NON_TEXT(See top of file). Returns a list of words
    in the subtitle text.
    """
    clean_subtext = []
    for line in subtext:
        for elt in NON_TEXT:
            line = line.replace(elt,"")
        words = line.split()
        for word in words:
            clean_subtext.append(word)
    return clean_subtext

def frequency_of_words(lst):
    """
    Passes over the given list of words and returns a dictionary mapping
    each unique word to its frequency in the list.
    """
    frequencies = defaultdict(int)
    for word in lst:
        frequencies[word] += 1
    return frequencies


main()
