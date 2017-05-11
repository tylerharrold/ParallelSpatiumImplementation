# imports
import text_parser
import utils
import chardet
import sys
import codecs

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
    # Ensure the user has specified a file to use as q (our doc in question)
    if(len(sys.argv) != 2):
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
    wordDict = text_parser.getDictionaryOfUniqueWords(qDoc)

    # now we would like to have this dictionary as a list, so that we
    # can easily sort
    wordCountList = text_parser.getUniqueTupleList(wordDict)

    # sort this list by word count
    wordCountList = utils.mergeSortNumeric(wordCountList)

    # test print the first 300 words, but know that this should be
    # controlled if there happen to be fewer than 300 words
    with codecs.open("testoutput.txt" , "w" , encoding="utf-8") as f:
        for i in range(len(wordCountList)-300 , len(wordCountList)):
            f.write(wordCountList[i][0] + ":" + str(wordCountList[i][1])+"\n")
        f.close()


main();
