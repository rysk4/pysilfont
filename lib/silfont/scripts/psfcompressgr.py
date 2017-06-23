#!/usr/bin/env python
'Compress Graphite tables in a font'
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2017 SIL International (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Martin Hosken'

argspec = [
    ('ifont',{'help': 'Input TTF'}, {'type': 'infont'}),
    ('ofont',{'help': 'Output TTF','nargs': '?' }, {'type': 'outfont'}),
]

from silfont.core import execute
from fontTools.ttLib.tables.DefaultTable import DefaultTable
import lz4
import sys, struct

class lz4tuple(object) :
    def __init__(self, start) :
        self.start = start
        self.literal = start
        self.literal_len = 0
        self.match_dist = 0
        self.match_len = 0
        self.end = 0

    def __str__(self) :
        return "lz4tuple(@{},{}+{},-{}+{})={}".format(self.start, self.literal, self.literal_len, self.match_dist, self.match_len, self.end)

def read_literal(t, dat, start, datlen) :
    if t == 15 and start < datlen :
        v = ord(dat[start])
        t += v
        while v == 0xFF and start < datlen :
            start += 1
            v = ord(dat[start])
            t += v
        start += 1
    return (t, start)

def write_literal(num, shift) :
    res = []
    if num > 14 :
        res.append(15 << shift)
        num -= 15
        while num > 255 :
            res.append(255)
            num -= 255
        res.append(num)
    else :
        res.append(num << shift)
    return bytearray(res)

def parseTuple(dat, start, datlen) :
    res = lz4tuple(start)
    token = ord(dat[start])
    (res.literal_len, start) = read_literal(token >> 4, dat, start+1, datlen)
    res.literal = start
    start += res.literal_len
    res.end = start
    if start > datlen - 2 : 
        return res
    res.match_dist = ord(dat[start]) + (ord(dat[start+1]) << 8)
    start += 2
    (res.match_len, start) = read_literal(token & 0xF, dat, start, datlen)
    res.end = start
    return res

def compressGr(dat, version) :
    if ord(dat[1]) < version :
        dat = dat[0] + chr(version) + dat[2:]
    datc = lz4.compressHC(dat[:-4])[4:]  # strip initial length and last 4 bytes
    # now find the final tuple
    end = len(datc)
    start = 0
    curr = lz4tuple(start)
    while curr.end < end :
        start = curr.end
        curr = parseTuple(datc, start, end)
    if curr.end > end :
        print "Sync error: %s" % (curr)
    newend = write_literal(curr.literal_len + 4, 4) + datc[curr.literal:curr.literal+curr.literal_len+1] + dat[-4:]
    lz4hdr = struct.pack(">L", (1 << 27) + (len(dat) & 0x7FFFFFF))
    return dat[0:4] + lz4hdr + datc[0:curr.start] + newend

def doit(args) :
    infont = args.ifont
    for tag, version in (('Silf', 5), ('Glat', 3)) :
        dat = infont.getTableData(tag)
        newdat = compressGr(dat, version)
        table = DefaultTable(tag)
        table.decompile(newdat, infont)
        infont[tag] = table
    return infont

def cmd() : execute('FT', doit, argspec)
if __name__ == "__main__" : cmd()
