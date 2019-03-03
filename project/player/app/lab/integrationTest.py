import os
import sys
import time


def progressbar(current, total, prefix="", size=60, file=sys.stdout):
    count = total
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    show(current)
    file.write("\n")
    file.flush()



def show_multiple_progressbar(downloads_meta, size = 60):
   #downloads_meta [ ["computing", 10, 20] ]
   for meta in downloads_meta :
      progressbar(int(meta[1]),int(meta[2]), meta[0], size)


for i in range(1,10) :
   os.system("clear")
   downloads_meta = [["lib012233", i,10],["lib012233", i*4,100] ,["lib012233", i*2,50]]
   show_multiple_progressbar(downloads_meta)
   time.sleep(2)