#!/usr/bin/python
import sys

## python loadFiles.py temp 3 10
if __name__ == '__main__':
  f = open('/tmp/exeLog.log', 'a')
  for item in sys.argv:
    f.write("%s " % item)
  f.write("\n")
  f.close()
