#!/usr/bin/python
#-*- coding: utf8 -*-
# check_nvidia_temp.py - Plugin for nagios to check nvidia GPU temperature.

# Copyright (C) 2013 by Denis Khabarov aka 'Saymon21'
# E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess, re, argparse, sys

cliparser = argparse.ArgumentParser(description='''check_nvidia_temp.py - Plugin for nagios to check nvidia GPU temperature.
Copyright © 2013 by Denis Khabarov aka \'Saymon21\'
E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)
Homepage: http://opensource.hub21.ru/nagios-check-nvidia-temp
Licence: GNU General Public License version 3
You can download full text of the license on http://www.gnu.org/licenses/gpl-3.0.txt
''',formatter_class=argparse.RawDescriptionHelpFormatter)
cliparser.add_argument("-w", "--warning", dest="warning", metavar="VALUE", help="warning temperature", required=True, type=int)
cliparser.add_argument("-c", "--critical", dest="critical", metavar="VALUE", help="critical temperature", required=True, type=int)
cliparser.add_argument('--nvclockpath', metavar='VALUE', help='path to nvclock (default: /usr/bin/nvclock)', default='/usr/bin/nvclock', type=str)
cliargs = cliparser.parse_args()

def nvclock_call():
	shell="%s -T" % (cliargs.nvclockpath)
	child = subprocess.Popen(shell, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None)
	streamdata = child.communicate()
	return child.returncode, "".join(map(str, streamdata))

def main():
	code,res=nvclock_call()
	if code == 0:
		tmp=re.search('GPU temperature:\s+(\d+)C',res)
		if tmp is not None:
			temp=int(tmp.group(1))
			if temp:
				if temp >= int(cliargs.critical):
					print('CRITICAL - GPU temperature: %s'%(str(temp)))
					sys.exit(2)
				elif temp >= int(cliargs.warning):
					print('WARNING - GPU temperature: %s'%(str(temp)))
					sys.exit(1)
				else:
					print('OK - GPU temperature: %s'%(str(temp)))
					sys.exit(0)
			else:
				print('UNKNOWN - Unable to get information about gpu temperature. (57)')
				sys.exit(3)
		else:
			print('UNKNOWN - Unable to find information about gpu temperature. (60)')
			sys.exit(3)
	elif code == 127:
		print('UNKNOWN - The program \'nvclock\' is currently not installed.')
		sys.exit(3)
	else:
		print('UNKNOWN - nvclock call error.')
		sys.exit(3)
		
if __name__ == "__main__":
	main()
