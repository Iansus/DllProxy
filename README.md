# DllProxy

# Install

```batch
> python3 -m virtualenv venv
> venv\scripts\activate
> pip3 install -r requirements.txt
```


# Use

**Warning:** currently limited to 64-bit DLLs
**Info:** DLL is output in the `x64\Release\` directory under the name `DLLProxy.dll`

```batch
> rundll32.exe NormalDLL.dll,test
> rundll32.exe NormalDLL.dll,#2

> python3 dllproxy.py -o ProxiedDLL.dll NormalDLL.dll
> REM Build with VS
> DLLproxy.sln

> REM retrieve DLL
> copy x64\Release\DLLProxy.dll ProxyfyingDll.dll

> rundll32.exe ProxyfyingDll.dll,test
> rundll32.exe ProxyfyingDll.dll,#2
```