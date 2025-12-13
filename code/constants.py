import sys
from enum import Enum

class ErrorCode(Enum):
	VARIABLE_NOT_FOUND = ("E001", "Variable '{}' not found")
	UNKNOWN_COMMAND = ("E002", "Unknown command '{}'")
	MISSING_ARGUMENT = ("E003", "Missing argument for command '{}'")
	MISSING_PART_OF_SPEECH = ("E004", "Missing part of speech for command '{}'")
	
	def __init__(self, code, message):
		self.code = code
		self.message = message
	
	def print_error(self, *args):
		formatted_message = self.message.format(*args)
		sys.stderr.write(f"Error [{self.code}]: {formatted_message}\n")

class CommandList :
	noun_list = ("tmp", "temp", "sys", "system", "var", "variable")
	verb_list = ("chg", "change", "crt", "create", "echo", "stop")
	prep_list = ("-in")