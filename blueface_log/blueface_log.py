#!/usr/local/bin/python2.7
# vim:ts=2:sw=2:expandtab:ft=python:fileencoding=utf-8

# $Id$

# Copyright (c) 2009-2012, Conall O'Brien
# Released under the BSD license
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Conall O'Brien ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


__author__ = "Conall O'Brien (conall@conall.net)"
__version__ = 0.2


import datetime
import gflags as flags
import mechanize
import os
import sys


FLAGS = flags.FLAGS


flags.DEFINE_string("user", None, "Blueface.ie Username", short_name="u")
flags.DEFINE_string("passwd", None, "Blueface.ie Password", short_name="p")
flags.DEFINE_string("ac_code", None, "Blueface.ie Account Code", 
                    short_name="a")
flags.DEFINE_integer("duration", 7, "Time duration in days to lookup", 
                     short_name="d")
flags.DEFINE_bool("reverse", True, "Set order to be cronological",
                  short_name="r")
flags.DEFINE_bool("version", False, "Display version", short_name="V")
# Required Flags
flags.MarkFlagAsRequired("user")
flags.MarkFlagAsRequired("passwd")
flags.MarkFlagAsRequired("ac_code")


def _ParseBluefaceLogs(label, line):
  """Parse the blueface CSV format"""
  output = {}
  header = label.split(",")
  data = line.split(",")
  for k, v in zip(header, data):
    output[k.lower()] = v
  return output


def GetBluefaceLogs(user, passwd, ac_code, duration=7):
  """Log into http://www.blueface.ie and download the call history.

  Args:
    user: (string) Username to log in as.
    passwd: (string) Password to log in with.
    ac_code: (string) Blueface account reference.
    duration: (int) Duration of logs, in days. Default: 7

  Returns:
    data: (list of dicts) Blueface call history, converted into a dict,
          split out per line
  """
  output = []
  now = datetime.datetime.today()
  start = now - datetime.timedelta(days=duration)
  now_format = now.strftime("%d%b%Y")
  start_format = start.strftime("%d%b%Y")
  br = mechanize.Browser()
  br.open("https://customers.blueface.ie")
  br.select_form(nr=0)
  br["username"] = user
  br["password"] = passwd
  bface = br.submit()
  call_log = ("https://customers.blueface.ie/callhistorycsv.csv"
              "?accountcode=%s&startdate=%s&enddate=%s" % (ac_code, 
                                                           start_format, 
                                                           now_format))
  logs = br.open(call_log).read().split("\n")
  for l in range(1, len(logs)):
    output.append(_ParseBluefaceLogs(logs[0], logs[l]))
  return output


def app():
  argv = FLAGS(sys.argv)
  if FLAGS.version:
    print "Version: %1f" % __version__
    sys.exit(0)
  hist = GetBluefaceLogs(user=FLAGS.user,  passwd=FLAGS.passwd,
                         ac_code=FLAGS.ac_code,  duration=FLAGS.duration)
  if FLAGS.reverse:
    hist.reverse()
  for h in hist:
    if "calldirection" not in h:
      continue
    if h["calldirection"] == "Ingress":
      print "%s %s [%s] %s (%s)" % (h["time"], 
                                    h["date"], 
                                    h["calldirection"],
                                    h["callerid"],
                                    h["duration(s)"])
    elif h["calldirection"] == "Egress":
      print "%s %s [%s] %s [%s] (%s)" % (h["time"], 
                                         h["date"], 
                                         h["calldirection"],
                                         h["destination"],
                                         h["description"],
                                         h["duration(s)"])


if __name__ == "__main__":
  app()
