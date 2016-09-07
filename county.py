import requests
import re
import os
import gzip
import logging
import logging.config
import logging.handlers

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
