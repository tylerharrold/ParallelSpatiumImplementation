import chardet 
import codecs

# opens our file into a giant array of bytes
def openFile(fileName):
    # load file into a binary dataset
    binData = open(fileName , "rb").read()
    encoding = chardet.detect(binData) # analyze the binary data
    encoding = encoding['encoding']
    text = codecs.open(fileName , "r" , encoding=encoding).read()
    return text

# splits a document (array of bytes) into a list of words
def splitText(text):
    text = text.split()
    return text

# function that makes all chars lowercase and strips punctuation
# this function is probably not necessary, but may be employed later
def stripWords(words):
    for i in range(len(words)):
        words[i] = words[i].lstrip("(.\"!, \'")
        words[i] = words[i].rstrip(").\"!, \':;")
        words[i] = words[i].lower()
    return words

# function creates a dictionary of unique words, which serve
# as an index which is paired by a numeric representation of
# how many times each word was inserted into the dictionary
# (effectively providing a count of the appearances)
def getDictionaryOfUniqueWords(words):
    dictionary = {}
    for i in range(len(words)):
        if(words[i] in dictionary):
            dictionary[words[i]] = dictionary[words[i]] + 1
        else:
            dictionary[words[i]] = 1

    return dictionary

# this function translates our dictionary into a 2 tuple list
# of word / wordcount pairs
def getUniqueTupleList(dictionary):
    tupleList = list(dictionary.items())
    return tupleList

def formatTextIntoDictionary(fileName):
    text = openFile(fileName)
    text = splitText(text)
    text = stripWords(text)
    text = getDictionaryOfUniqueWords(text)
    return text

# function that, given the word/word count tuple list, returns total
# unique words
def getWordCount(wordList):
    count = 0
    for i in range(len(wordList)):
        count = count + wordList[i][1]
    return count
