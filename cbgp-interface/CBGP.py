# ===================================================================
# @(#)CBGP.py
#
# @author Sebastien Tandel (standel@info.ucl.ac.be)
# @date 29/09/2004
# @lastdate 29/09/2004
# ===================================================================

import os, select, Queue, thread, threading, sys, posix, time;
import fcntl

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
  # cBGP = CBGP("/home/madhurubuntu/madhur-work/cbgp-2.3.2/src/cbgp")
  cBGP = CBGP("/usr/local/bin/cbgp")
  fo = open('temp.txt', 'w')
  cmd = "include /home/anshika/madhur-work/Test_Data/IL/IL_bank_1.cli\n"
  cBGP.send(cmd)
  print 'done loading'  
  fi = open('/home/anshika/madhur-work/Test_Data/IL/IL_bank_traceroute_1.cli')
  for line in fi:
    print line
    cBGP.send(line)
    ret = cBGP.expect()
    print ret
    fo.write(ret)



  cBGP.finalize()
