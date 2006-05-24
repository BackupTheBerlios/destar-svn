#!/usr/bin/env python

# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2006 by Anthony PIRON
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


"""
An unittest Suite for i18n using module unittest
"""



import unittest, os, fnmatch, re

def grep(seq, regex):
    regex = re.compile(regex,re.M )
    for line in seq:
        if regex.search(line,0):
            yield line

class TestI18n(unittest.TestCase):
    
    def setUp(self):
        self.files = fnmatch.filter(os.listdir("lang/"),"*.po")

    def testAllStringsDynamic(self):

        def chomp(s):
            if s[-2:] == '\r\n':
                return s[:-2]
            if s[-1:] == '\r' or s[-1:] == '\n':
                return s[:-1]
            return s

        msgidRegex = re.compile(r'^msgid "(.*)"$')
        msgstrRegex = re.compile(r'^msgstr "(.*)"$')
        strRegex = re.compile(r'^"(.*)"$')

        success = 1
        for fi in self.files:
            print "Checking %s" % fi
            state = 0
            partialSuccess = 0
            lineCount = 1
            msgIdCount = 0
            msgNotTrans = 0
            for line in file("lang/" + fi):
                # Eating some msgid's miam
                if state == 0:
                    s = msgstrRegex.search(line)
                    s2 = msgidRegex.search(line)
                    if s:
                        if s.group(1) != "":
                            partialSuccess = 1
                        state = 1
                    elif s2:
                        msgIdCount += 1
                # After msgstr 
                elif state == 1:
                    s = strRegex.search(line)
                    if s:
                        if s.group(1) != "":
                            partialSuccess = 1
                            #print "%d: str %s" % (lineCount,line)
                    else:
                        success = success and partialSuccess
                        
                        if not partialSuccess:
                            msgNotTrans += 1
                            #print "%d: Partial %s" % (lineCount,line)
                        state = 0
                        partialSuccess = 0
                    
                lineCount += 1

            print "%d on %d not translated (%d %%)" % (msgNotTrans,
                                                       msgIdCount,
                                                       msgNotTrans * 100 / msgIdCount)
                
        self.assert_(success)

