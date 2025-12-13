from constants import CommandList, ErrorCode

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

		ast = {
			"noun": "", 
			"verb": "", 
			"prep": [], 
			"val": []
		}

		ast["noun"] = tokens[0]

		if len(tokens) > 1:
			ast["verb"] = tokens[1]
		
			for token in tokens[2:] :
				if token in CommandList.prep_list :
					ast["prep"].append(token)
				else :
					ast["val"].append(token)
		else :
			ErrorCode.MISSING_PART_OF_SPEECH.print_error("verb")
			return None
		
		return ast
		