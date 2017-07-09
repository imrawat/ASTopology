# ===================================================================
# @(#)CBGP.py
#
# @author Sebastien Tandel (standel@info.ucl.ac.be)
# @date 29/09/2004
# @lastdate 29/09/2004
# ===================================================================

import os, select, Queue, thread, threading, sys, posix, time;

class CBGP_reader(threading.Thread):
  rHandle = None
  qOutput = None
  def __init__(self, rHandle, qOutput):
    threading.Thread.__init__(self)
    self.rHandle = rHandle
    self.qOutput = qOutput

  def run(self):
    whileTrue = True
    while whileTrue:
      r, w, e = select.select([self.rHandle.fileno()], [], [])
      sNewLines = self.rHandle.readline()
      whileTrue = self.read_condition_stop(sNewLines)
      while (whileTrue and sNewLines):
	self.qOutput.put(sNewLines)
	sNewLines = self.rHandle.readline()
	whileTrue = self.read_condition_stop(sNewLines)
  
  def read_condition_stop(self, sLine):
    if (sLine.find("stop-CBGP_reader") >= 0):
      return False
    else:
      return True

class CBGP:
  wHandle = None
  rHandle = None
  qOutput = None
  ReadingThread = None
  def __init__(self, cbgp):
    cbgp = cbgp + ' 2>/dev/null'
    self.wHandle, self.rHandle = os.popen2(cbgp)
    self.qOutput = Queue.Queue(0)
    self.ReadingThread = CBGP_reader(self.rHandle, self.qOutput)
    self.ReadingThread.start()

  def send(self, sMessage):
    if (self.wHandle != None):
      posix.write(self.wHandle.fileno(), sMessage)
      self.wHandle.flush()

  def expect(self):
    if (self.qOutput != None):
      stringRet = self.qOutput.get()
      return stringRet
    else:
      return None

  def finalize(self):
    self.send('print "stop-CBGP_reader\\n"\n')
    self.ReadingThread.join()
    self.rHandle.close()
    self.wHandle.close()

if __name__ == '__main__':
  cBGP = CBGP("/home/anshika/madhur-work/cbgp-2.3.2/src/cbgp")

  cBGP.send('bgp topology load --addr-sch=local "caida_16bit.txt"')
  cBGP.send('bgp topology install')
  cBGP.send('bgp topology policies')
  cBGP.send('bgp topology run')
  cBGP.send('sim run')
  cBGP.send('bgp router AS24835 add network 196.204.192.0/19')
  
  # cBGP.send('set autoflush on\n')
  # cBGP.send('net add node 0.0.1.1\n')
  # cBGP.send('net add node 0.0.1.2\n')
  # cBGP.send('net add link 0.0.1.1 0.0.1.2 15\n')
  # cBGP.send('net node 0.0.1.1 spf-prefix 0.0.1/24\n')
  # cBGP.send('net node 0.0.1.2 spf-prefix 0.0.1/24\n')
  # cBGP.send('bgp add router 1 0.0.1.1\n')
  # cBGP.send('bgp router 0.0.1.1\n')
  # cBGP.send('  add network 0.0.1/24\n')
  # cBGP.send('  add peer 1 0.0.1.2\n')
  # cBGP.send('  peer 0.0.1.2 up\n')
  # cBGP.send('  exit\n')
  # cBGP.send('bgp add router 1 0.0.1.2\n')
  # cBGP.send('bgp router 0.0.1.2\n')
  # cBGP.send('  add network 0.0.2/24\n')
  # cBGP.send('  add peer 1 0.0.1.1\n')
  # cBGP.send('  peer 0.0.1.1 up\n')
  # cBGP.send('  exit\n')
  # cBGP.send('sim run\n')
  # cBGP.send('print "CONFIGURATION OK\\n"\n')

  # sRet = cBGP.expect()
  # if (sRet == None or sRet.find("CONFIGURATION OK") < 0):
  #   print 'CONFIGURATION KO'
  #   exit()

  # # Request a routing table dump from router 0.0.1.1
  # cBGP.send('print "# This is the RIB of router 0.0.1.1:\\n"\n')
  # cBGP.send('bgp router 0.0.1.1 show rib *\n')
  # cBGP.send('print "done\\n"\n')

  # sRet = cBGP.expect()
  # while (sRet != None and sRet.find("done") < 0):
  #   sys.stdout.write("(1) read:[%s]\n" % sRet.rstrip('\n'))
  #   sys.stdout.flush()
  #   sRet = cBGP.expect()

  # # Request a routing table dump from router 0.0.1.2
  # cBGP.send('print "# This is the RIB of router 0.0.1.2:\\n"\n');
  # cBGP.send('bgp router 0.0.1.2 show rib *\n');
  # cBGP.send('print "done\\n"\n');

  # sRet = cBGP.expect()
  # while (sRet != None and sRet.find("done") < 0): 
  #   sys.stdout.write("(2) read:[%s]\n" % sRet.rstrip('\n'))
  #   sRet = cBGP.expect()

  cBGP.finalize()
