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
	  
				if i + 1 < len(command) and command[i+1] == '=':
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
	def parse(tokens, variables):
		if not tokens:
			return None

		if "-if" in tokens :
			return Condition.parse_condition(tokens, variables)
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
	def parse_condition(tokens, variables):
		if_index = tokens.index("-if")
		condition_tokens = tokens[:if_index]
  
		if "-else" in tokens:
			else_index = tokens.index("-else")
			if_block = tokens[if_index + 1:else_index]
			else_block = tokens[else_index + 1:]
		else:
			if_block = tokens[if_index + 1:]
			else_block = None
		
		return {
			"type": "condition",
			"condition": condition_tokens,
			"if_block": if_block,
			"else_block": else_block
		}

	
	@staticmethod
	def extract_block(tokens):
		if tokens[0] != "{" :
			return None

		start = 0
		end = tokens.index("}")
  
		return tokens[start+1:end]
  
	@staticmethod
	def evaluate_condition(condition_tokens, variables):
	 
		if '-and' in condition_tokens:
			and_index = condition_tokens.index('-and')
			
			left_condition = condition_tokens[:and_index]
			right_condition = condition_tokens[and_index + 1:]
			
			left_result = Condition.evaluate_condition(left_condition, variables)
			right_result = Condition.evaluate_condition(right_condition, variables)
			
			return left_result and right_result
		
		elif '-or' in condition_tokens:
			or_index = condition_tokens.index('-or')
			
			left_condition = condition_tokens[:or_index]
			right_condition = condition_tokens[or_index + 1:]
			
			left_result = Condition.evaluate_condition(left_condition, variables)
			right_result = Condition.evaluate_condition(right_condition, variables)
			
			return left_result or right_result
		else :
			left = condition_tokens[0]
			if left.startswith("$"):
				var_name = left[1:]
				if var_name in variables:
					left_value = variables[var_name]
				else:
					ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
					return False
			else:
				left_value = left
		
			right = condition_tokens[2]
			if right.startswith("$"):
				var_name = right[1:]
				if var_name in variables:
					right_value = variables[var_name]
				else:
					ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
					return False
			else:
				right_value = right
				
			operator = condition_tokens[1]
			right = condition_tokens[2]
			
			left_num = float(left_value) if Parser._is_number(left_value) else None
			right_num = float(right_value) if Parser._is_number(right_value) else None
			
			if left_num is not None and right_num is not None:
				if operator == "<":
					return left_num < right_num
				elif operator == ">":
					return left_num > right_num
				elif operator == "<=":
					return left_num <= right_num
				elif operator == ">=":
					return left_num >= right_num
				elif operator == "==":
					return left_num == right_num
				elif operator == "!=":
					return left_num != right_num
			else:
				if operator == "<":
					return left_value < right_value
				elif operator == ">":
					return left_value > right_value
				elif operator == "<=":
					return left_value <= right_value
				elif operator == ">=":
					return left_value >= right_value
				elif operator == "==":
					return left_value == right_value
				elif operator == "!=":
					return left_value != right_value
		
			return False