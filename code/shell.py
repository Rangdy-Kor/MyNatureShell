import sys
from logic import Parser
from constants import ErrorCode, CommandList


variable = {}

class Command :
	@staticmethod
	def execute(ast, variables):
		if ast is None:
			return
		
		
		noun = ast["noun"]
		verb = ast["verb"]

		class_name = noun.capitalize()
		method_name = "_" + verb

		if noun not in CommandList.noun_list:
			ErrorCode.UNKNOWN_COMMAND.print_error(noun)
			return None
		
		if noun == "temp":
			class_name = "Tmp"
		elif noun == "variable":
			class_name = "Var"
		elif noun == "system":
			class_name = "Sys"
		
		try :
			CommandClass = globals()[class_name]
			CommandMethod = getattr(CommandClass, method_name)
			result = CommandMethod(ast, variables) 
			return result
		except KeyError:
			ErrorCode.UNKNOWN_COMMAND.print_error(f"Class for '{noun}' not found.")
			return None
		except AttributeError:
			ErrorCode.UNKNOWN_COMMAND.print_error(f"{noun} {verb}")
			return None
		except Exception as e:
			sys.stderr.write(f"Runtime Error during execution: {e}\n")
			return None


class Tmp :
	@staticmethod
	def _echo(ast, variables) :
		output = []
		for word in ast["val"]:
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

class Var :
	@staticmethod
	def _crt(ast, variables) :
		raw_args = ast.get("raw_args", [])

		if len(raw_args) != 3:
			ErrorCode.MISSING_ARGUMENT.print_error("var crt: Expected 'name -in value'")
			return None

		if not (raw_args[1] in CommandList.prep_list):
			ErrorCode.MISSING_ARGUMENT.print_error(f"var crt: Missing or misplaced mandatory flag '{raw_args[1]}'. Expected 'name -in value'")
			return None
		
		var_name = raw_args[0]
		var_value = raw_args[2].strip('"')
		
		variables[var_name] = var_value
		sys.stdout.write(f"Variable '{var_name}' created.\n")
	@staticmethod
	def _create(ast, variables) :
		Var._crt(ast, variables)

	@staticmethod
	def _chg(ast, variables) :
		raw_args = ast.get("raw_args", [])
		if len(raw_args) != 3:
			ErrorCode.MISSING_ARGUMENT.print_error("var chg: Expected 'name -in value'")
			return None
		
		var_name = raw_args[0]

		if var_name not in variables:
			ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
			return None
		
		if raw_args[1] != "-in":
			ErrorCode.MISSING_ARGUMENT.print_error("var chg: Missing or misplaced mandatory flag '-in'. Expected 'name -in value'")
			return None
		
		var_value = raw_args[2].strip('"')
		variables[var_name] = var_value
		sys.stdout.write(f"Variable '{var_name}' changed.\n")
	@staticmethod
	def _change(ast, variables) :
		Var._chg(ast, variables)

	@staticmethod
	def _get(ast, variables) :
		if len(ast["val"]) < 1:
			ErrorCode.MISSING_ARGUMENT.print_error("var get")
			return None
		
		var_name = ast["val"][0]
		if var_name in variables:
			sys.stdout.write(variables[var_name] + "\n")
		else:
			ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)

class Sys :
	@staticmethod
	def _stop(ast, variables) :
		return "exit"

class Run:
	@staticmethod
	def start():
		sys.stdout.write("Nautre Shell ver 0.1.4\n")
		while True :
			sys.stdout.write("\n>>> ")
			cmd = sys.stdin.readline().strip()

			tokens = Parser.tokenize(cmd)
			ast = Parser.parse(tokens)

			result = Command.execute(ast, variable)

			if result == "exit" :
				sys.stdout.write("Exiting My Shell. Goodbye!\n")
				break

if __name__ == "__main__" :
	Run.start()