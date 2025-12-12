import sys

sys.stdout.write("My Shell v1.0\n")

variable = {}

class Parser :
	@staticmethod
	def tokenize(command) :
		tokens = []
		current_token = ""
		in_string = False
		i = 0
		while i < len(command) :
			char = command[i]
			if char == '"' :
				in_string = not in_string
				current_token += char
				i += 1
				continue
			elif in_string :
				current_token += char
				i += 1
				continue
			elif char == " ":
				if current_token != "":
					tokens.append(current_token)
					current_token = ""
				i += 1
				continue
			else :
				current_token += char
				i += 1
				continue
		if current_token != "":
			tokens.append(current_token)
		return tokens

class Command :
	while True :
		sys.stdout.write("\n>>> ")
		cmd = sys.stdin.readline().strip()
		parsing = Parser.tokenize(cmd)
	
		if parsing[0] == "echo" :
			if len(parsing) > 1 :
				output_text = " ".join(parsing[1:]) 
				if output_text.startswith('"') and output_text.endswith('"'):
					output_text = output_text[1:-1]
				sys.stdout.write(output_text + "\n")
			else :
				sys.stdout.write("")
		elif parsing[0] == "exit" :
			if len(parsing) == 1 :
				sys.stdout.write("Exiting My Shell. Goodbye!\n")
				break
			else :
				sys.stdout.write("Error: 'exit' command does not take any arguments.\n")
		elif parsing[0] == "set" :
			if len(parsing) > 2 :
				var_name = parsing[1]
				var_value = parsing[2]
				variable[var_name] = var_value
			elif len(parsing) == 2 :
					sys.stdout.write("Error: 'set' command requires a variable name and a value.\n")
			else :
				sys.stdout.write("Error: 'set' command requires arguments.\n")
		elif parsing[0] == "get" :
			if len(parsing) > 1 :
				var_name = parsing[1]
				if var_name in variable :
					sys.stdout.write(f"{variable[var_name]}\n")
				else :
					sys.stdout.write(f"Error: Variable '{var_name}' is not defined.\n")
		else :
			sys.stdout.write("Error: Unknown command\n")