import random
import sys

def genSeq(filenameFormat, length, splitCount):
  print 'filename: %0s; length: %1s; splitCount: %2s' % (filenameFormat, str(length), str(splitCount))
  seq = list(range(1, 10**length))
  random.shuffle(seq)
  format = '%0' + str(length) + 'd\n'
  i = 0
  fileIdx = 0
  file = open(filenameFormat % str(fileIdx), 'aw')
  for s in seq:
    if i==splitCount:
      file.close()
      fileIdx += 1
      file = open(filenameFormat % str(fileIdx), 'aw')
      i = 0
    file.write(format % s)
    i += 1
  if not file.closed: file.close()

## python genSeq.py out/test%0s.txt 5 100
if __name__ == '__main__':
  genSeq(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

