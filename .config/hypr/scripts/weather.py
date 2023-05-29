#!/usr/bin/env python3

from os import system,path
from sys import exit
import re

location = "Kolkata"
tmplogfile = "/tmp/weather.log"

def escape_ansi(line):
        re1 = re.compile(r'\x1b\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]')
        re2 = re.compile(r'\x1b[PX^_].*?\x1b\\')
        re3 = re.compile(r'\x1b\][^\a]*(?:\a|\x1b\\)')
        re4 = re.compile(r'\x1b[\[\]A-Z\\^_@]')
        re5 = re.compile(r'[\x00-\x1f\x7f-\x9f\xad]+')

        for r in [re1, re2, re3, re4, re5]:
            line = r.sub('', line)

        return line


if path.exists(tmplogfile):
    system("rm /tmp/weather.log")

system(f"curl -s https://en.wttr.in/{location} >> {tmplogfile}")

lines = []
status = ""
temp = ""

with open(tmplogfile,'r') as file:
    lines = file.readlines()
    
    lines[0] = escape_ansi(lines[0])

    if lines[0][0] == '>':
        print("Unable to fetch temperature for " + location)
        sys.exit(-1)

    file.close()
    
i = 16

while lines[2][i] != '\n':
    status = status + lines[2][i]
    i = i + 1
    
i = 16

while lines[3][i] != '(':
    temp = temp + lines[3][i]
    i = i + 1

iTemp = escape_ansi(temp)
temp = iTemp.split("  ")[1]

print(f"{location},{status},{temp}")

exit(0)
