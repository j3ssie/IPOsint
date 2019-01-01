#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob
import argparse
from pprint import pprint

# from core import execute
# from core import utils

# # import modules 
from modules import core
from modules import whois
from modules import ripe
from modules import arin
try:
	from modules import hurricane
except:
	core.print_bad("You're missing chrome webdrive")
	core.install_webdrive()



# Console colors
W = '\033[1;0m'   # white 
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G,R,B,P,C,O,GR]


#############
# IPSpace
#############

__author__ = '@j3ssiejjj'
__version__ = '1.0'


### Global stuff
current_path = os.path.dirname(os.path.realpath(__file__))
###

options = {
	'target' : '',
	'cwd' : current_path,
	'cidr_regex' : "((\d){1,3}\.){3}(\d){1,3}(\/(\d){1,3})?",
	# gonna match these: 1.2.3.4 - 5.6.7.8
	'range_ip_regex' : '((\d){1,3}\.){3}(\d){1,3}(\/(\d){1,3})?\s\-\s((\d){1,3}\.){3}(\d){1,3}(\/(\d){1,3})?' 
}



def cowsay():
	print ("""{1}
	  -----------------------------
	< You didn't say the {2}MAGIC WORD{1} >
	  ----------------------------- 
	         \   ^__^
	          \  (oo)\_______
	             (__)\       )\/
	             	\||----w |    
	                 ||     ||    Contact: {2}{3}{1}
		""".format(C, G, P, __author__))


def parsing_argument(args):
	if args.target:
		options['target'] = args.target

	if args.output:
		options['output'] = args.output
	else:
		options['output'] = args.target

	if args.target_list:
		if os.path.exists(args.target_list):
			with open(args.target_list, 'r+') as ts:
				targetlist = ts.read().splitlines()
			
			for target in targetlist:
				single_target()
				print("{2}>++('> >++('{1}>{2} Target done: {0} {1}<{2}')++< <')++<".format(target, P, G))

	else:
		single_target()

	# single_target()

	really_uniq()

def single_target():
	whois.Whois(options)
	ripe.Ripe(options)
	arin.Arin(options)
	hurricane.Hurricane(options)




def really_uniq():
	core.print_good("Unique the output")

	with open(options['output'], 'r+') as o:
		output = o.read().splitlines()

	
	with open(options['output'], 'w+') as o:
		for item in set(output):
			o.write(item + "\n")

	core.check_output(options['output'])

def update():
	execute.run1('git fetch --all && git reset --hard origin/master')
	sys.exit(0)

def main():
	cowsay()
	parser = argparse.ArgumentParser(description="Discovery IP Space of the target")
	parser.add_argument('-t','--target' , action='store', dest='target', help='target')
	parser.add_argument('-T','--target_list' , action='store', dest='targetlist', help='list of target')
	parser.add_argument('-o','--output' , action='store', dest='output', help='output')
	parser.add_argument('--update', action='store_true', help='update lastest from git')

	args = parser.parse_args()
	if len(sys.argv) == 1:
		# help_message()
		sys.exit(0)

	# if args.list_module:
	# 	list_module()
	if args.update:
		update()

	parsing_argument(args)


if __name__ == '__main__':
	main()