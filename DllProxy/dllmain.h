#ifndef DLLMAIN_H
#define DLLMAIN_H

typedef struct {
    unsigned int ordinal;
    const char* name;
    void* proxy_function;
} PROXY_IAT_ENTRY;


PROXY_IAT_ENTRY* getIAT();
unsigned int getIATSize();

#endif