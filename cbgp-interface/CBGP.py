# ===================================================================
# @(#)CBGP.py
#
# @author Sebastien Tandel (standel@info.ucl.ac.be)
# @date 29/09/2004
# @lastdate 29/09/2004
# ===================================================================

import os, select, Queue, thread, threading, sys, posix, time;
import fcntl

import argparse

#local imports
import sys
sys.path.append('./..')
import constants

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

  parser = argparse.ArgumentParser(description = 'create cli for country to country all to all')
  parser.add_argument('-c', '--country_code', help='Country Code', required = True)
  parser.add_argument('-m', '--mode', help='C:Country G2C:Global to Country A2C:Asmatra to Country', required = True)
  parser.add_argument('-p', '--cli_number', help='cli file number', required = True)


  args = parser.parse_args()
  COUNTRY_CODE = args.country_code
  CLI_NUMBER = args.cli_number
  MODE = args.mode

  if MODE == 'C':
    SUFFIX = "_country_"
    SUFFIX_TRACEROUTE = '_country_traceroute_'
  elif MODE == "G2C" or MODE == "g2c":
    SUFFIX = "_g2c_"
    SUFFIX_TRACEROUTE = '_g2c_traceroute_'
  elif MODE == "a2c" or MODE == "A2C":
    SUFFIX = "_a2c_"
    SUFFIX_TRACEROUTE = '_a2c_traceroute_'
  elif MODE == 'T':
    SUFFIX = "_transport_"
    SUFFIX_TRACEROUTE = "_transport_traceroute_"
  elif MODE == "B":
    SUFFIX = "_bank_"
    SUFFIX_TRACEROUTE = "_bank_traceroute_"
  elif MODE == "G":
    SUFFIX = "_govt_"
    SUFFIX_TRACEROUTE = "_govt_traceroute_"
  elif MODE == "D":
    SUFFIX = "_dns_"
    SUFFIX_TRACEROUTE = "_dns_traceroute_"

  loading_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + SUFFIX + CLI_NUMBER + '.cli'
  trace_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + SUFFIX_TRACEROUTE + CLI_NUMBER + '.cli'

  out_cbgp_trace_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_cbgp_trace' + SUFFIX + CLI_NUMBER +'.txt'

  print 'prefix loading file', loading_file
  print 'trace_file', trace_file
  print 'out_cbgp_trace_file', out_cbgp_trace_file


  cBGP = CBGP("/usr/local/bin/cbgp")
  fo = open(out_cbgp_trace_file, 'w')

  cmd_load = 'include ' + loading_file + '\n'
  print 'load cmd', cmd_load
  cBGP.send(cmd_load)
  print 'done loading'
  
  fi = open(trace_file)
  for line in fi:
    cBGP.send(line)
    ret = cBGP.expect()
    fo.write(ret)

  print 'done'

  cBGP.finalize()

