import sys
from enum import Enum

sys.stdout.write("My Shell v1.0\n")

variable = {}

class ErrorCode(Enum):
	VARIABLE_NOT_FOUND = ("E001", "Variable '{}' not found")
	UNKNOWN_COMMAND = ("E002", "Unknown command '{}'")
	MISSING_ARGUMENT = ("E003", "Missing argument for command '{}'")
	
	def __init__(self, code, message):
		self.code = code
		self.message = message
	
	def print_error(self, *args):
		formatted_message = self.message.format(*args)
		sys.stderr.write(f"Error [{self.code}]: {formatted_message}\n")

class Parser:
	@staticmethod
	def tokenize(command):
		tokens = []
		current_token = ""
		in_string = False
		i = 0
		while i < len(command):
			char = command[i]
			if char == '"':
				in_string = not in_string
				current_token += char
				i += 1
				continue
			elif in_string:
				current_token += char
				i += 1
				continue
			elif char == " ":
				if current_token != "":
					tokens.append(current_token)
					current_token = ""
				i += 1
				continue
			else:
				current_token += char
				i += 1
				continue
		if current_token != "":
			tokens.append(current_token)
		return tokens
	
	@staticmethod
	def parse(tokens):
		if not tokens:
			return None

		command = tokens[0]

		if command == "echo":
			return {
				"type": "echo",
				"args": tokens[1:]
			}
		elif command == "set":
			return {
				"type": "set",
				"var_name": tokens[1],
				"var_value": tokens[2]
			}
		elif command == "get":
			return {
				"type": "get",
				"var_name": tokens[1]
			}
		elif command == "exit":
			return {
				"type": "exit"
			}
		else:
			return {
				"type": "unknown",
				"command": command
			}

class Command:
	@staticmethod
	def execute(ast, variables):
		if ast is None:
			return
		
		if ast["type"] == "echo":
			Command._execute_echo(ast, variables)

		elif ast["type"] == "set":
			Command._execute_set(ast, variables)
		
		elif ast["type"] == "get":
			return Command._execute_get(ast, variables)
		
		elif ast["type"] == "exit":
			return Command._execute_exit()
		
		elif ast["type"] == "unknown":
			ErrorCode.UNKNOWN_COMMAND.print_error(ast['command'])

	@staticmethod
	def _execute_echo(ast, variables):
		output = []
		for word in ast["args"]:
			if word.startswith("$"):
				var_name = word[1:]
				if var_name in variables:
					output.append(variables[var_name])
				else:
					output.append(word)
			else:
				output.append(word)

		result = " ".join(output)
		if result.startswith('"') and result.endswith('"'):
			result = result[1:-1]

		sys.stdout.write(result + "\n")

	@staticmethod
	def _execute_set(ast, variables):
		variables[ast["var_name"]] = ast["var_value"]

	@staticmethod
	def _execute_get(ast, variables):
		if ast["var_name"] in variables:
			sys.stdout.write(variables[ast["var_name"]] + "\n")
		else:
			ErrorCode.VARIABLE_NOT_FOUND.print_error(ast["var_name"])
	
	@staticmethod
	def _execute_exit():
		return "exit"

class Run:
	@staticmethod
	def start():
		while True:
			sys.stdout.write("\n>>> ")
			cmd = sys.stdin.readline().strip()

			tokens = Parser.tokenize(cmd)
			ast = Parser.parse(tokens)

			result = Command.execute(ast, variable)

			if result == "exit":
				sys.stdout.write("Exiting My Shell. Goodbye!\n")
				break

Run.start()