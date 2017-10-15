import requests
#import re
import os
#import gzip
import logging
import logging.config
import logging.handlers
import sys
import county
import random
import traceback
#fp = requests.get('http://propaccess.traviscad.org/clientdb/?cid=1')
'''
class County(object):
  def __init__(self, session, name, logger):
    self.sess = session
    self.name = name
    self.patt = re.compile('\s+')
    self.log = logger
    if not os.path.exists(name):
      os.makedirs(name)
  def close(self):
    self.sess = None
  def formatUrl(self, pid):
    return pid
  def isValidResponse(self, resp):
    return resp.status_code == requests.codes.ok
  def getProp(self, pids):
    for pid in pids:
      resp = self.sess.get(self.formatUrl(pid))
      if self.isValidResponse(resp):
        self.log.info('%0s - prop id %1s' % (self.name, pid))
        #file = open(os.path.join(self.name, pid), 'wb')
        #for chunk in resp.iter_content(10000):
        #  file.write(chunk)
        with gzip.open(os.path.join(self.name, pid+'.gz'), 'wb') as f:
          f.write(self.patt.sub(' ', resp.content))
      else:
        self.log.warn('%0s - invalid prop id %1s' % (self.name, pid))
      resp.close()

class CountyTravis(County):
  def __init__(self, session, log):
    super(CountyTravis, self).__init__(session, 'travis', log)
    r = self.sess.get('http://propaccess.traviscad.org/clientdb/?cid=1')
    r.close()
  def formatUrl(self, pid):
    return 'http://propaccess.traviscad.org/clientdb/Property.aspx?prop_id=%0s' % pid
  def isValidResponse(self, resp):
    return super(CountyTravis,self).isValidResponse(resp) and resp.content.find('Property not found.') == -1

class CountyWilliamson(County):
  def __init__(self, session, log):
    super(CountyWilliamson, self).__init__(session, 'williamson', log)
  def formatUrl(self, pid):
    return 'http://search.wcad.org/Property-Detail?PropertyQuickRefID=R%0s' % pid
  def isValidResponse(self, resp):
    return super(CountyWilliamson,self).isValidResponse(resp) and resp.content.find(' could not be loaded.') == -1
'''
def getProps(ids):
  logger.info('get prop ids: %0s' % ids)
  s = requests.Session()
  cs = [county.CountyTravis(s, logger), county.CountyWilliamson(s, logger)]
  for c in cs:
    #c.getProp(['41', '571461', '822241', '524832', '002209'])
    c.getProp(ids)
  s.close()

## python loadFiles.py 
def loadFiles(dir, minBatchCount, maxBatchCount):
  filenames = os.listdir(dir)
  batchIds = []
  for filename in filenames:
    if filename.endswith('cmp'):
      continue
    filePath = os.path.join(dir, filename)
    logger.info('parsing file: %0s' % filePath)
    batchCount = random.randrange(minBatchCount, maxBatchCount)
    idx = 0
    with open(filePath, 'r') as fi:
      for line in fi:
        batchIds.append(line[:-1])
        idx += 1
        if idx == batchCount:
          getProps(batchIds)
          del batchIds[:]
          idx = 0
          batchCount = random.randrange(minBatchCount, maxBatchCount)
      if len(batchIds) > 0:
        getProps(batchIds)
    os.rename(filePath, os.path.join(os.path.join(dir, 'cmp'), filename))

logging.config.fileConfig('log/logging.conf')
logger = logging.getLogger('loadFiles')
## python loadFiles.py temp 3 10
if __name__ == '__main__':
  try:
    dir = sys.argv[1]
    minBatchCount = sys.argv[2]
    maxBatchCount = sys.argv[3]
    logger.info('loadFiles execution starts: %0s %1s %2s' % (dir, minBatchCount, maxBatchCount)) 
    loadFiles(dir, int(minBatchCount), int(maxBatchCount))
  except Exception, err:
    exc_info = sys.exc_info()
    logger.error('error when running: %0s %1s %2s\t%3s' % (sys.argv[1], sys.argv[2], sys.argv[3], str(exc_info)))
    traceback.print_exception(*exc_info)
    del exc_info

