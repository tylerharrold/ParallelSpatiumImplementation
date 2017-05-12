import text_parser
import utils
import chardet
import sys
import codecs
import time
import threading
from threading import Thread

start = time.process_time()
qPath = sys.argv[1]
qDoc = text_parser.openFile(qPath)
end = time.process_time()
print("duration:" , end-start)
