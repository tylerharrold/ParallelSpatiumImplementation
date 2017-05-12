# imports
import text_parser
import utils
import chardet
import sys
import codecs
import time
import threading
from threading import Thread

# parallel Implementation of the spatiumL1 algorithm

# pseudocode

# load Q
#   scan Q for the top 200-300 words
# load A (profile of contested author)

# run formula to calculate delta0

# load other profiles and produce deltam1, deltam2 etc

# get the ratio, then use comparison

# print results

# shared memory for the calculation of delta m
results = [None] * 3

# main function of the program
def main():
    start = time.process_time()
    
    # Ensure the user has specified a file to use as q (our doc in question)
    # CLEAN THIS UP A BIT
    if(len(sys.argv) != 3):
        print("Please specify the path to the document in question, and the path to the suspected author's profile")
        sys.exit();
        
    # load our q text into a list of words
    qPath = sys.argv[1]
    qDoc = text_parser.openFile(qPath)
    qDoc = text_parser.splitText(qDoc)

    #-----------------------------------------
    # get the top 300 most commonly used words in Q
    #-----------------------------------------
    # using a dictionary data structure, we obtain a set of
    # unique words (the indecies) and the number of times they appear
    qWordDict = text_parser.getDictionaryOfUniqueWords(qDoc)

    # now we would like to have this dictionary as a list, so that we
    # can easily sort
    qWordCountList = text_parser.getUniqueTupleList(qWordDict)

    # sort this list by word count
    qWordCountList = utils.mergeSortNumeric(qWordCountList)

    # get the total word count of q
    qWordCount = text_parser.getWordCount(qWordCountList)

    #----------------------------------------------------
    # open A, profile of the suspected author
    #   A should contain between 1 and 5 known works
    # ---------------------------------------------------
    # load
    aPath = sys.argv[2]
    aDoc = text_parser.openFile(aPath)
    aDoc = text_parser.splitText(aDoc)

    #----------------------------------------------------
    # split entirety of used words into tuple list pairing
    # the word with its count
    #----------------------------------------------------
    # using a dictionary data structure, we obtain a set of
    # unique words in tuple list form
    aWordDict = text_parser.getDictionaryOfUniqueWords(aDoc)
    aWordCountList = text_parser.getUniqueTupleList(aWordDict)

    # get word count for A
    aWordCount = text_parser.getWordCount(aWordCountList)

    # run summation. Right now we'll use a linear search wich is messed
    # up but it will have to do until we implement binary search
    delta0 = 0
    for i in range(0 , 300):
        # need word count/total words for q
        qWord = qWordCountList[len(qWordCountList)-1-i][0]
        qWordFreq = qWordCountList[len(qWordCountList)-1-i][1] / qWordCount
        # need the number of times qWord appears in A
        aWordOccur = 0
        for k in range(0 , len(aWordCountList)):
            if(aWordCountList[k][0] == qWord):
                aWordOccur= aWordOccur+1
        aWordFreq = aWordOccur / aWordCount
        delta0 = delta0 + (qWordFreq - aWordFreq)

    print("our total delta is: " , delta0)

    # now run this again with author profiles, this time using threads
    # paths for the threads
    paths = [["./profiles/austen/austen_profile.txt" , "./profiles/joyce/joyce_profile.txt" , "./profiles/stoker/stoker_profile.txt"]
             , ["./profiles/wilde/wilde_profile.txt" , "./profiles/verne/verne_profile.txt" , "./profiles/twain/twain_profile.txt"]
             , ["./profiles/bronte_c/bronte_c_profile.txt" , "./profiles/dickens/dickens_profile.txt" , "./profiles/poe/poe_profile.txt"]]
    threads = []
    for i in range(3): # hard coded three for testing
        threads.append(Thread(target=analyzeImposterGroup , args=(i, qWordCountList , qWordCount , paths[i]))) # need args here
        threads[i].start()
    # need all the sums, so we are forced to join
    for j in range(3):
        threads[j].join()

    # we now have the lowest of the three deltas from every r group, we need to average these
    rDeltaAvg = 0
    for i in range(3):
        rDeltaAvg = rDeltaAvg + results[i]
    rDeltaAvg = rDeltaAvg / 3
    
    # our final ratio
    ratio = delta0 / rDeltaAvg

    if(ratio < .975):
        print("same author")
    elif(ratio > 1.025):
        print("not the author")
    else:
        print("inconclusive")
    end = time.process_time()

    elapsed = end - start
    print("This failure all took: " , elapsed) # TODO print more positive message

# function that represents a thread. Each thread will be responsible for finding three deltas for 3 authors
# when compared to the original text. It will then place the smallest of the three deltas in the array at the
# index of the thread id provided it
def analyzeImposterGroup(threadID , qWordList , qWordCount , paths):
    # we loop three times, once for each path given to us
    deltas = [0 , 0 , 0]
    for i in range(3):
        # open the file pertaining to path
        path = paths[i]
        mDoc = text_parser.openFile(path)
        mDoc = text_parser.splitText(mDoc) #TODO - maybe also split here
        mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
        # our all important word/word count tuple list
        mWordList = text_parser.getUniqueTupleList(mWordDict)
        mWordCount = text_parser.getWordCount(mWordList)
        # now we can run spatium
        for j in range(0 , 300):
            qWord = qWordList[len(qWordList) - 1 - j][0]
            qWordFreq = qWordList[len(qWordList) - 1 - j][1] / qWordCount
            # see how many times qword appears in our imposter profile
            mWordOccur = 0
            for k in range(0 , len(mWordList)):
                if(mWordList[k][0] == qWord):
                    mWordOccur = mWordOccur+1
            mWordFreq = mWordOccur / mWordCount
            deltas[i] = deltas[i] + (qWordFreq - mWordFreq)
    # now we have our three deltas, return the smallest of the three
    smallestDelta = 0
    if(deltas[0] < deltas[1] and deltas[0]<deltas[2]):
        smallestDelta = deltas[0]
    elif(deltas[1] < deltas[0] and deltas[1] < deltas[2]):
        smallestDelta = deltas[1]
    else:
        smallestDelta = deltas[2]
    results[threadID] = smallestDelta
    
# run program
main();
