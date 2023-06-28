#!/usr/bin/python3

# DLLMAIN.h
DLLMAIN_H = '''#ifndef DLLMAIN_H
#define DLLMAIN_H

#define MALICIOUS_CMD "%(MALICIOUS_CMD)s"
%(PRAGMA_COMMENTS)s

#endif'''