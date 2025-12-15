import sys
from logic import Parser, Condition
from constants import ErrorCode, CommandList


variable = {}

class Command: 
	@staticmethod
	def execute(ast, variables) :
		if ast is None:
			return

		if ast.get("type") == "condition":
			result = Condition.evaluate_condition(ast["condition"], variables)
			
			if result:
				if_block = ast["if_block"]
				clean_block = if_block[1:-1]
				block_ast = Parser.parse(clean_block, variables)
				Command.execute(block_ast, variables)
			else:
				if ast.get("else_block"):
					else_block = ast["else_block"]
					clean_block = else_block[1:-1]
					block_ast = Parser.parse(clean_block, variables)
					Command.execute(block_ast, variables)
			return
		
		elif ast.get("type") == "while":
			from logic import Loop
			Loop.execute_while(ast, variables, Command.execute)
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
	
class PreProcessing :
	@staticmethod
	def _add_space(string) :
		string = " ".join(string.split())
		
		string = string.replace("**", " TMP ")
		string = string.replace("+", " + ")
		string = string.replace("-", " - ")
		string = string.replace("*", " * ")
		string = string.replace("/", " / ")
		string = string.replace("%", " % ")
		string = string.replace(" TMP ", " ** ")
		
		string = " ".join(string.split())
		return string

	@staticmethod
	def _evaluate_expression(*values, variables) :
		evaluated = []
		for val in values:
			if val.startswith("$"):
				var_name = val[1:]
				if var_name in variables:
					evaluated.append(variables[var_name])
				else:
					ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
					evaluated.append(None)
			else:
				evaluated.append(val)
		expression_string = " ".join(evaluated)
		return expression_string

	@staticmethod
	def _calc (expression) :
		expression_list = expression.split(" ")
		result = None
  
		i = 0
		try :
   
			if expression_list[0] == "-" :
				if len(expression_list) > 1 :
					try:
						float_val = float(expression_list[1]) 
						expression_list[0] = str(-float_val)
						del expression_list[1]
					except ValueError:
						pass
			
   
			i = 1
			while i < len(expression_list) - 1 :
				op = expression_list[i]
				if op == "**":
					try:
						val1 = float(expression_list[i-1])
						val2 = float(expression_list[i+1])
						result = val1 ** val2
						
						expression_list[i-1] = str(result)
						del expression_list[i+1]
						del expression_list[i]
	  
					except ValueError:
						i += 1
				else:
					i += 1
			
   
			i = 1
			while i < len(expression_list) - 1: 
				op = expression_list[i]
				
				if op in ["*", "/", "%"]:
	 
					if len(expression_list) > i + 3:
						if expression_list[i+1] == "-" and expression_list[i+2] == "-" :
							try :
								float_val = float(expression_list[i+3]) 
								expression_list[i+1] = str(float_val)
								del expression_list[i+2]
								del expression_list[i+2]
							except ValueError:
								pass
						
					if len(expression_list) > i + 2 :
						if expression_list[i+1] == "-" :
							try:
								float_val = float(expression_list[i+2]) 
								expression_list[i+1] = str(-float_val)
								del expression_list[i+2]
							except ValueError:
								pass
	
					try :
						val1 = float(expression_list[i-1])
						val2 = float(expression_list[i+1])
						
						if op == "*":
							result = val1 * val2
						elif op == "/": 
							if val2 == 0:
								sys.stderr.write("Error: Division by zero.\n")
								return None
							result = val1 / val2
						elif op == "%":
							if val2 == 0:
								sys.stderr.write("Error: Modulo by zero.\n")
								return None
							result = val1 % val2
						
						expression_list[i-1] = str(result)
						del expression_list[i+1]
						del expression_list[i] 
					except ValueError :
						i += 1
				else:
					i += 1
   
			i = 1
			while i < len(expression_list) - 1 :
				op = expression_list[i]
				
				if op == "+" or op == "-":
					try :
						val1 = float(expression_list[i-1])
						val2 = float(expression_list[i+1])
						
						if op == "+":
							result = val1 + val2
						else: 
							result = val1 - val2
						
						expression_list[i-1] = str(result)
						del expression_list[i+1]
						del expression_list[i] 
					except ValueError :
						i += 1
				else:
					i += 1
	 
			if len(expression_list) == 1:
				final_result = float(expression_list[0])

				if final_result.is_integer():
					return int(final_result)
				else:
					return final_result
			else:
				sys.stderr.write("Error: Invalid expression format (did not resolve to single value).\n")
				return None
 
		except ValueError :	
			sys.stderr.write("Error: Non-numeric value in expression.\n")
			return None
		except ZeroDivisionError :
			sys.stderr.write("Error: Division by zero.\n")
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
	def _crt(ast, variables):
		raw_args = ast.get("raw_args", [])
		
		if len(raw_args) < 3:
			ErrorCode.MISSING_ARGUMENT.print_error("var crt")
			return None
		
		var_name = raw_args[0]
		var_value_tokens = raw_args[2:]
		var_value = " ".join(var_value_tokens).strip('"')
	
		adjectives = ast.get("adjectives", [])
		if adjectives:
			var_type = adjectives[0]
			
			if var_type == "int":
				try:
					var_value = str(int(float(var_value)))
				except ValueError:
					sys.stderr.write(f"Error: Cannot convert '{var_value}' to int\n")
					return None
			elif var_type == "float":
				try:
					var_value = str(float(var_value))
				except ValueError:
					sys.stderr.write(f"Error: Cannot convert '{var_value}' to float\n")
					return None
			elif var_type == "str":
				var_value = str(var_value)
		
		variables[var_name] = var_value
		sys.stdout.write(f"Variable '{var_name}' created.\n")
	
	@staticmethod
	def _create(ast, variables) :
		Var._crt(ast, variables)

	@staticmethod
	def _chg(ast, variables) :
		raw_args = ast.get("raw_args", [])
		if len(raw_args) < 3:
			ErrorCode.MISSING_ARGUMENT.print_error("var chg: Expected 'name -in value'")
			return None
		
		var_name = raw_args[0]

		if var_name not in variables:
			ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
			return None
		
		if raw_args[1] != "-in":
			ErrorCode.MISSING_ARGUMENT.print_error("var chg: Missing or misplaced mandatory flag '-in'. Expected 'name -in value'")
			return None
		
		var_value_tokens = raw_args[2:]
		var_value = " ".join(var_value_tokens).strip('"')
		
		var_value = PreProcessing._add_space(var_value)
		var_tokens = var_value.split(" ")
		var_value = PreProcessing._evaluate_expression(*var_tokens, variables=variables)
		var_value = PreProcessing._calc(var_value)
		var_value = str(var_value)
  
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
		while True :
			global variable
			sys.stdout.write("\n>>> ")
			cmd = sys.stdin.readline().strip()

			tokens = Parser.tokenize(cmd)
			ast = Parser.parse(tokens, variable)

			result = Command.execute(ast, variable)

			if result == "exit" :
				sys.stdout.write("Exiting My Shell. Goodbye!\n")
				break

	@staticmethod
	def run_file(filename):
		try:
			with open(filename, 'r', encoding='utf-8') as f:
				lines = f.readlines()
			
			for line in lines:
				line = line.strip()
				
				if not line or line.startswith(('//', '##', 'cmt')):
					continue
				
				tokens = Parser.tokenize(line)
				ast = Parser.parse(tokens, variable)
				result = Command.execute(ast, variable)
				
				if result == "exit":
					break
		
		except FileNotFoundError:
			sys.stderr.write(f"Error: File '{filename}' not found\n")
		except Exception as e:
			sys.stderr.write(f"Error: {e}\n")

if __name__ == "__main__" :
	Run.start()