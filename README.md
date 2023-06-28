# DllProxy

Proxy your dll exports and add some spicy content at the same time!
New version now relies on forwarded exports rather than runtime library load, heavily inspired from [SharpDllProxy](https://github.com/Flangvik/SharpDllProxy)

# Install

```batch
> python3 -m virtualenv venv
> venv\scripts\activate
> pip3 install -r requirements.txt
```


# Use

```batch
> rundll32.exe NormalDLL.dll,test
> rundll32.exe NormalDLL.dll,#2

> python3 dllproxy.py -m calc.exe NormalDLL.dll

> rundll32.exe dist\NormalDLL.dll,test
> rundll32.exe dist\NormalDLL.dll,#2
```