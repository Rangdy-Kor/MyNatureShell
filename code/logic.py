from constants import CommandList, ErrorCode

class Parser:
	@staticmethod
	def tokenize(command):
		tokens = []
		current_token = ""
		in_string = False
		i = 0
  
		operators = ['<', '>', '=', '!', '{', '}']
  
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

			elif char in operators:
				if current_token != "":
					tokens.append(current_token)
					current_token = ""
     
				if char in ['=', '!'] and i + 1 < len(command) and command[i+1] == '=':
					tokens.append(char + '=')
					i += 2
					continue
				
				tokens.append(char)
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

		if "-if" in tokens :
			return Condition.parse_condition(tokens)
		ast = {
			"noun": "", 
			"verb": "", 
			"prep": [], 
			"val": [],
			"raw_args": []
		}

		ast["noun"] = tokens[0]

		if len(tokens) > 1:
			ast["verb"] = tokens[1]

			ast["raw_args"] = tokens[2:]
		
			for token in tokens[2:] :
				if token in CommandList.prep_list :
					ast["prep"].append(token)
				else :
					ast["val"].append(token)
		else :
			ErrorCode.MISSING_PART_OF_SPEECH.print_error("verb")
			return None
		
		return ast

	@staticmethod
	def _is_number(value):
		try:
			float(value)
			return True
		except ValueError:
			return False
		

class Condition :
	@staticmethod
	def parse_condition(tokens):
		if_index = tokens.index("-if")
		condition_tokens = tokens[:if_index]
		block_tokens = tokens[if_index + 1:]
  
		return {
			"type": "condition",
			"condition": condition_tokens,
			"block": block_tokens
		}
  
	@staticmethod
	def extract_block(tokens):
		if tokens[0] != "{" :
			return None

		start = 0
		end = tokens.index("}")
  
		return tokens[start+1:end]
  
	@staticmethod
	def evaluate_condition(condition_tokens, variables) :
		left = condition_tokens[0]
		if left.startswith("$") :
			var_name = left[1:]
			if var_name in variables :
				left_value = variables[var_name]
			else :
				ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
				return False
		else :
			left_value = left
		operator = condition_tokens[1]
  
		right = condition_tokens[2]
		
		left_num = float(left_value) if Parser._is_number(left_value) else None
		right_num = float(right) if Parser._is_number(right) else None
		
		if operator == "<" :
			if left_num is not None and right_num is not None :
				return left_num < right_num
			else :
				return left_value < right
		elif operator == ">" :
			if left_num is not None and right_num is not None :
				return left_num > right_num
			else :
				return left_value > right
		elif operator == "==" :
			if left_num is not None and right_num is not None :
				return left_num == right_num
			else :
				return left_value == right
		elif operator == "!=" :
			if left_num is not None and right_num is not None :
				return left_num != right_num
			else :
				return left_value != right