import sys
from pyparsing import (
    Word, alphas, alphanums, QuotedString, Literal, Optional, 
    ZeroOrMore, Regex, pyparsing_common, Group, Suppress,
    restOfLine, lineEnd
)
from constants import CommandList, ErrorCode


class Parser:
    """pyparsing을 사용한 파서"""
    
    @staticmethod
    def _is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def parse_command(command_str):
        """명령어 문자열을 파싱"""
        # 주석 처리
        if command_str.strip().startswith(('//','##','cmt')):
            return None
        
        # 기본 요소 정의
        identifier = Word(alphas + "_", alphanums + "_")
        # 변수: $ + identifier를 하나의 토큰으로 합침
        variable = Regex(r'\$[a-zA-Z_][a-zA-Z0-9_]*')
        number = pyparsing_common.number()
        quoted_string = QuotedString('"', escChar='\\')
        
        # 연산자
        comparison_op = (
            Literal("==") | Literal("!=") | 
            Literal("<=") | Literal(">=") | 
            Literal("<") | Literal(">")
        )
        logical_op = Literal("-and") | Literal("-or")
        
        # 값 (변수는 $를 포함해서 하나의 문자열로)
        value_with_var = (variable | quoted_string | number | identifier)
        
        # 조건식 (단순 비교)
        simple_condition = Group(
            value_with_var("left") + 
            comparison_op("op") + 
            value_with_var("right")
        )
        
        # 복합 조건식 (and/or 포함)
        condition = simple_condition + ZeroOrMore(
            logical_op("logical") + simple_condition
        )
        
        # 블록 { ... }
        block_content = Suppress("{") + ZeroOrMore(
            ~Literal("}") + (value_with_var | comparison_op | logical_op | Literal("-in"))
        )("block") + Suppress("}")
        
        # if-else 문
        if_stmt = (
            condition("condition") + 
            Suppress("-if") + 
            block_content("if_block") +
            Optional(Suppress("-else") + block_content("else_block"))
        )
        
        # while 문
        while_stmt = (
            condition("condition") + 
            Suppress("-while") + 
            block_content("while_block")
        )
        
        # 일반 명령어: noun[:type] verb [args...]
        noun_part = identifier("noun") + Optional(
            Suppress(":") + identifier("adjective")
        )
        prep_flag = Literal("-in")
        arg_value = variable | quoted_string | number | identifier
        
        command = (
            noun_part + 
            identifier("verb") + 
            ZeroOrMore(prep_flag | arg_value)("args")
        )
        
        # 전체 문법
        statement = if_stmt | while_stmt | command
        
        try:
            result = statement.parseString(command_str, parseAll=True)
            return result
        except Exception as e:
            sys.stderr.write(f"Parse error: {e}\n")
            return None
    
    @staticmethod
    def to_ast(parsed, variables):
        """pyparsing 결과를 AST로 변환"""
        if parsed is None:
            return None
        
        # if 문 처리
        if "if_block" in parsed:
            # condition을 평평한 리스트로 변환
            condition_list = []
            for item in parsed.condition:
                if hasattr(item, '__iter__') and not isinstance(item, str):
                    condition_list.extend(str(x) for x in item)
                else:
                    condition_list.append(str(item))
            
            return {
                "type": "condition",
                "condition": condition_list,
                "if_block": list(parsed.if_block),
                "else_block": list(parsed.else_block) if "else_block" in parsed else None
            }
        
        # while 문 처리
        if "while_block" in parsed:
            # condition을 평평한 리스트로 변환
            condition_list = []
            for item in parsed.condition:
                if hasattr(item, '__iter__') and not isinstance(item, str):
                    condition_list.extend(str(x) for x in item)
                else:
                    condition_list.append(str(item))
            
            return {
                "type": "while",
                "condition": condition_list,
                "block": list(parsed.while_block)
            }
        
        # 일반 명령어 처리
        ast = {
            "noun": parsed.noun,
            "adjectives": [parsed.adjective] if "adjective" in parsed else [],
            "verb": parsed.verb,
            "prep": [],
            "val": [],
            "raw_args": []
        }
        
        if "args" in parsed:
            args = list(parsed.args)
            ast["raw_args"] = args
            
            for arg in args:
                if arg in CommandList.prep_list:
                    ast["prep"].append(arg)
                else:
                    ast["val"].append(str(arg))
        
        # verb 검증
        if not ast["verb"]:
            ErrorCode.MISSING_PART_OF_SPEECH.print_error("verb")
            return None
        
        return ast


class Loop:
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
            
            # 블록 실행
            block_tokens = ast["block"]
            # 블록을 명령어 문자열로 재구성
            block_str = " ".join(str(t) for t in block_tokens)
            
            parsed = Parser.parse_command(block_str)
            if parsed:
                block_ast = Parser.to_ast(parsed, variables)
                if block_ast:
                    execute_func(block_ast, variables)
            
            iterations += 1
        
        if iterations >= max_iterations:
            sys.stderr.write("Warning: Loop exceeded maximum iterations\n")


class Condition:
    @staticmethod
    def evaluate_condition(condition_tokens, variables):
        """조건식 평가"""
        # -and 처리
        if '-and' in condition_tokens:
            and_index = condition_tokens.index('-and')
            left_condition = condition_tokens[:and_index]
            right_condition = condition_tokens[and_index + 1:]
            
            left_result = Condition.evaluate_condition(left_condition, variables)
            right_result = Condition.evaluate_condition(right_condition, variables)
            
            return left_result and right_result
        
        # -or 처리
        elif '-or' in condition_tokens:
            or_index = condition_tokens.index('-or')
            left_condition = condition_tokens[:or_index]
            right_condition = condition_tokens[or_index + 1:]
            
            left_result = Condition.evaluate_condition(left_condition, variables)
            right_result = Condition.evaluate_condition(right_condition, variables)
            
            return left_result or right_result
        
        # 단순 비교
        if len(condition_tokens) < 3:
            return False
        
        left = str(condition_tokens[0])
        operator = str(condition_tokens[1])
        right = str(condition_tokens[2])
        
        # 변수 값 가져오기 ($ 처리)
        if left.startswith("$"):
            var_name = left[1:]
            if var_name in variables:
                left_value = variables[var_name]
            else:
                ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
                return False
        else:
            left_value = left
        
        if right.startswith("$"):
            var_name = right[1:]
            if var_name in variables:
                right_value = variables[var_name]
            else:
                ErrorCode.VARIABLE_NOT_FOUND.print_error(var_name)
                return False
        else:
            right_value = right
        
        # 숫자 비교
        left_num = float(left_value) if Parser._is_number(str(left_value)) else None
        right_num = float(right_value) if Parser._is_number(str(right_value)) else None
        
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
            # 문자열 비교
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