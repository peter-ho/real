import requests
import re
import os
import gzip
import logging
import logging.config
import logging.handlers
import sys
from lxml import html
#fp = requests.get('http://propaccess.traviscad.org/clientdb/?cid=1')
#cookie = fp.headers['set-cookie'].split(';')[0]

## python parseFiles.py 
def parseFiles(dir, batchCount):
  filenames = os.listdir(dir)
  batchIds = []
  idx = 0
  for filename in filenames:
    filePath = os.path.join(dir, filename)
    logger.info('parsing file: %0s' % filePath)
    with gzip.open(filePath, 'rb') as fi:
      c = fi.read()
      for line in fi:
        batchIds.append(line[:-1])
        idx += 1
        if idx == batchCount:
          getProps(batchIds)
          del batchIds[:]
          idx = 0
      if len(batchIds) > 0:
        getProps(batchIds)
    os.rename(filePath, os.path.join(os.path.join(dir, 'cmp'), filename))

logging.config.fileConfig('log/logging.conf')
logger = logging.getLogger('default')
## python loadFiles.py temp 10
if __name__ == '__main__':
  try:
    dir = sys.argv[1]
    #'test/travis/121703.gz'
    batchCount = sys.argv[2]
    logger.info('parseFiles execution starts: %0s %1s' % (dir, batchCount)) 
    parseFiles(dir, int(batchCount))
  except:
    logger.error('error when running: %0s %1s\t%2s' % (sys.argv[1], sys.argv[2], str(sys.exc_info())))

