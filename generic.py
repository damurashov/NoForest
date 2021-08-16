#!/usr/bin/python3

import subprocess
from collections import Counter
import re
import asyncio as async
import sys
import shlex


def command_run(command, verbose=True):
	command = shlex.split(command)
	if not verbose:
		return subprocess.Popen(command, stdout=subprocess.PIPE)
	else:
		return subprocess.Popen(command)


def command_output(command, verbose=False) -> str and int:
	"""
	:param command: command to execute
	:return: console output, string
	"""
	proc = command_run(command, verbose)
	proc.wait()

	if verbose:
		return "", proc.returncode

	return proc.stdout.read().decode("utf-8"), proc.returncode


def dialog_yn(text) -> bool:
	while True:
		ans = input(text)
		if 'y' in ans and 'n' not in ans:
			print('y')
			return True
		elif 'n' in ans and 'y' not in ans:
			print('n')
			return False


def smart_split(string):
	NEWLINE = '\n'

	string = string.strip()
	hist = Counter(string)

	if NEWLINE in hist:
		return string.split(NEWLINE)
	else:
		return re.split('\s+', string)
