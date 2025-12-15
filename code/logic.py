import sys
from constants import CommandList, ErrorCode

class Parser:
	@staticmethod
	def tokenize(command):
		if command.strip().startswith(('//','##','cmt')):
			return []
		tokens = []
		current_token = ""
		in_string = False
		i = 0
		
		operators = ['<', '>', '=', '!', '{', '}']
		
		while i < len(command):
			char = command[i]
			
			if char == '"':
				if in_string:
					tokens.append(current_token)
					current_token = ""
					in_string = False
				else:
					if current_token:
						tokens.append(current_token)
						current_token = ""
					in_string = True
				i += 1
				continue
			
			if in_string:
				current_token += char
				i += 1
				continue
			
			if char in operators:
				if current_token:
					tokens.append(current_token)
					current_token = ""
				
				if i + 1 < len(command) and command[i+1] == '=':
					tokens.append(char + '=')
					i += 2
					continue
				
				tokens.append(char)
				i += 1
				continue
			
			if char == " ":
				if current_token:
					tokens.append(current_token)
					current_token = ""
				i += 1
				continue
			
			current_token += char
			i += 1
		
		if current_token:
			tokens.append(current_token)
		
		return tokens

	@staticmethod
	def parse(tokens, variables):
		if not tokens:
			return None
		
		if "-if" in tokens:
			return Condition.parse_condition(tokens, variables)
		
		if "-while" in tokens:
			return Loop.parse_while(tokens, variables)
		
		ast = {
			"noun": "",
			"adjectives": [],
			"verb": "",
			"prep": [],
			"val": [],
			"raw_args": []
		}
		
		first_token = tokens[0]
		if ':' in first_token:
			parts = first_token.split(':')
			ast["noun"] = parts[0]
			ast["adjectives"] = parts[1:]
		else:
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

class Loop:
    @staticmethod
    def parse_while(tokens, variables):
        while_index = tokens.index("-while")
        condition_tokens = tokens[:while_index]
        block_tokens = tokens[while_index + 1:]
        
        return {
            "type": "while",
            "condition": condition_tokens,
            "block": block_tokens
        }
    
    @staticmethod
    def execute_while(ast, variables, execute_func):
        max_iterations = 1000
        iterations = 0
        
        while iterations < max_iterations:
            result = Condition.evaluate_condition(
                ast["condition"], 
                variables
            )
            
            if not result:
                break
            
            block = ast["block"]
            clean_block = block[1:-1]
            block_ast = Parser.parse(clean_block, variables)
            execute_func(block_ast, variables)
            
            iterations += 1
        
        if iterations >= max_iterations:
            sys.stderr.write("Warning: Loop exceeded maximum iterations\n")

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