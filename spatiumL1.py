# imports
import text_parser
import utils
import chardet
import sys
import codecs
import time
# Serial Implementation of the spatiumL1 algorithm

# pseudocode

# load Q
#   scan Q for the top 200-300 words
# load A (profile of contested author)

# run formula to calculate delta0

# load other profiles and produce deltam1, deltam2 etc

# get the ratio, then use comparison

# print results

# main function of the program
def main():
    start = time.process_time()
    # Ensure the user has specified a file to use as q (our doc in question)
    # CLEAN THIS UP A BIT
    if(len(sys.argv) != 3):
        print("Please specify the name of the document to test")
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

    # now run this again with author profiles
    # hard code city
    
    # first block of three
    path = "./profiles/austen/austen_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM1 = spatium(qWordCountList , qWordCount , mWordCountList)

    xpath = "./profiles/joyce/joyce_profile.txt"
    xDoc = text_parser.openFile(xpath)
    xDoc = text_parser.splitText(xDoc)
    xWordDict = text_parser.getDictionaryOfUniqueWords(xDoc)
    xWordCountList = text_parser.getUniqueTupleList(xWordDict)
    deltaM2 = spatium(qWordCountList , qWordCount , xWordCountList)

    path = "./profiles/stoker/stoker_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM3 = spatium(qWordCountList , qWordCount , mWordCountList)

    # choose the lowest distance calculate (the least optimistic)
    finalDelta1 = 0
    if(deltaM1 < deltaM2):
        if(deltaM1 < deltaM3):
            finalDelta1 = deltaM1
        else:
            finalDelta1 = deltaM3
    else:
        if(deltaM2 < deltaM3):
            finalDelta1 = deltaM2
        else:
            finalDelta1 = deltaM3

    print("deltaM1: " , deltaM1 , "\ndeltaM2: " , deltaM2 , "\ndeltaM3: " , deltaM3)
    print("our lowest is " , finalDelta1)

    # second block of three
    path = "./profiles/wilde/wilde_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM1 = spatium(qWordCountList , qWordCount , mWordCountList)

    xpath = "./profiles/verne/verne_profile.txt"
    xDoc = text_parser.openFile(xpath)
    xDoc = text_parser.splitText(xDoc)
    xWordDict = text_parser.getDictionaryOfUniqueWords(xDoc)
    xWordCountList = text_parser.getUniqueTupleList(xWordDict)
    deltaM2 = spatium(qWordCountList , qWordCount , xWordCountList)

    path = "./profiles/twain/twain_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM3 = spatium(qWordCountList , qWordCount , mWordCountList)

    # choose the lowest distance calculate (the least optimistic)
    finalDelta2 = 0
    if(deltaM1 < deltaM2):
        if(deltaM1 < deltaM3):
            finalDelta2 = deltaM1
        else:
            finalDelta2 = deltaM3
    else:
        if(deltaM2 < deltaM3):
            finalDelta2 = deltaM2
        else:
            finalDelta2 = deltaM3

    print("deltaM1: " , deltaM1 , "\ndeltaM2: " , deltaM2 , "\ndeltaM3: " , deltaM3)
    print("our lowest is " , finalDelta2)


    # third block of three
    path = "./profiles/bronte_c/bronte_c_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM1 = spatium(qWordCountList , qWordCount , mWordCountList)

    xpath = "./profiles/dickens/dickens_profile.txt"
    xDoc = text_parser.openFile(xpath)
    xDoc = text_parser.splitText(xDoc)
    xWordDict = text_parser.getDictionaryOfUniqueWords(xDoc)
    xWordCountList = text_parser.getUniqueTupleList(xWordDict)
    deltaM2 = spatium(qWordCountList , qWordCount , xWordCountList)

    path = "./profiles/poe/poe_profile.txt"
    mDoc = text_parser.openFile(path)
    mDoc = text_parser.splitText(mDoc)
    mWordDict = text_parser.getDictionaryOfUniqueWords(mDoc)
    mWordCountList = text_parser.getUniqueTupleList(mWordDict)
    deltaM3 = spatium(qWordCountList , qWordCount , mWordCountList)

    # choose the lowest distance calculate (the least optimistic)
    finalDelta3 = 0
    if(deltaM1 < deltaM2):
        if(deltaM1 < deltaM3):
            finalDelta3 = deltaM1
        else:
            finalDelta3 = deltaM3
    else:
        if(deltaM2 < deltaM3):
            finalDelta3 = deltaM2
        else:
            finalDelta3 = deltaM3

    print("deltaM1: " , deltaM1 , "\ndeltaM2: " , deltaM2 , "\ndeltaM3: " , deltaM3)
    print("our lowest is " , finalDelta3)

    finalDeltaAvg = (finalDelta1 + finalDelta2 + finalDelta3) / 3

    ratio = delta0 / finalDeltaAvg

    if(ratio < .975):
        print("same author")
    elif(ratio > 1.025):
        print("not the author")
    else:
        print("inconclusive")
    end = time.process_time()

    elapsed = end - start
    print("This failure all took: " , elapsed)

def spatium(qWordList , qWordCount , aWordList):
    aWordCount = text_parser.getWordCount(aWordList)
    delta = 0
    for i in range(0 , 300):
        # need word coutn/total for q
        qWord = qWordList[len(qWordList)-1-i][0]
        qWordFreq = qWordList[len(qWordList)-1-i][1] / qWordCount
        # need the number of times qword appear in A
        aWordOccur = 0
        for k in range(0 , len(aWordList)):
            if(aWordList[k][0] == qWord):
                aWordOccur = aWordOccur+1
        aWordFreq = aWordOccur / aWordCount
        delta = delta + (qWordFreq - aWordFreq)
    return delta

main();
