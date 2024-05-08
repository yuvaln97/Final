import re


class ScriptInterpreter:
    def __init__(self):
        self.variables = {}

    def evaluate_expression(self, expression):
        if expression[0:5] == 'print':
            print(expression[5:])

        tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)|[a-zA-Z_]\w*|==|!=|<=|>=|<|>|and|or|not', expression)
        operator_stack = []
        operand_stack = []

        for token in tokens:
            if token.isdigit():
                operand_stack.append(int(token))
            elif token in self.variables:
                operand_stack.append(self.variables[token])
            elif token in ['+', '-', '*', '/', '==', '!=', '<=', '>=', '<', '>', 'and', 'or', 'not']:
                while (operator_stack and
                       self.precedence(operator_stack[-1]) >= self.precedence(token)):
                    self.apply_operation(operator_stack.pop(), operand_stack)
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    self.apply_operation(operator_stack.pop(), operand_stack)
                operator_stack.pop()
            elif token not in self.variables and not token.isdigit():
                self.variables[token] = self.evaluate_expression(tokens[1])
            else:
                print(f"var {token} is not defined")
                break

        while operator_stack:
            self.apply_operation(operator_stack.pop(), operand_stack)

        if operand_stack:
            return operand_stack[0]  # Return the result if the operand stack is not empty
        else:
            return None  # Return None if the operand stack is empty

    def precedence(self, op):
        if op in ['+', '-']:
            return 1
        elif op in ['*', '/']:
            return 2
        elif op in ['==', '!=', '<=', '>=', '<', '>', 'and', 'or', 'not']:
            return 3
        else:
            return 0

    def apply_operation(self, op, operand_stack):
        if op == 'and':
            operand_stack.append(operand_stack.pop() and operand_stack.pop())
        elif op == 'or':
            operand_stack.append(operand_stack.pop() or operand_stack.pop())
        elif op == 'not':
            operand_stack.append(not operand_stack.pop())
        else:
            b = operand_stack.pop()
            a = operand_stack.pop()
            if op == '+':
                operand_stack.append(a + b)
            elif op == '-':
                operand_stack.append(a - b)
            elif op == '*':
                operand_stack.append(a * b)
            elif op == '/':
                if b == 0:
                    print("You can't divide by 0")
                else:
                    operand_stack.append(a / b)
            elif op == '==':
                operand_stack.append(a == b)
            elif op == '!=':
                operand_stack.append(a != b)
            elif op == '<=':
                operand_stack.append(a <= b)
            elif op == '>=':
                operand_stack.append(a >= b)
            elif op == '<':
                operand_stack.append(a < b)
            elif op == '>':
                operand_stack.append(a > b)

    def interpret(self, code):
        lines = code.split('\n')
        new_commands = []
        expr_if=[]
        output = []
        try:
            if_num = 0
            for line in lines:
                if line.startswith('IF'):
                    parts = re.split(r'\sTHEN\s', line.strip())
                    for part in parts:
                        if 'IF' in part:
                            if_num += 1
                    if if_num > 3:
                        print("Can't support more than 3 nested IF statements")
                        return None
                    elif if_num == 1:
                        condition = parts[0][3:].strip()# grabbing the condition
                        if self.evaluate_expression(condition):
                            new_parts = parts[len(parts)-2].split(' ')
                            for part in new_parts:
                                self.interpret(part)
                        if len(parts) > 2:
                            expr_if = parts[1:]

                            for expr in expr_if and expr_if:
                                if ' ' in expr:
                                    new_commands = new_commands+expr.split(' ')
                                else:
                                    new_commands.append(expr)
                            for command in new_commands:
                                self.interpret(command)

                        else:
                            expr_if = parts[1]
                            self.interpret(expr_if)

                    else:  # 2 to 3 conditions
                        for index in range(if_num):
                            current_condition = parts[index][3:].strip()
                            if not self.evaluate_expression(current_condition):
                                if not parts[len(parts) - index - 1].isdigit():
                                    exec(parts[len(parts) - index - 1])
                                else:
                                    return parts[len(parts) - index - 1]
                            if index != if_num - 1:
                                pass
                            else:  # Condition is true
                                if not parts[len(parts) - index - 2].isdigit():
                                    exec(parts[len(parts) - index - 2])
                                else:
                                    return parts[len(parts) - index - 2]

                    # Handle 'AND/OR' in conditions
                    if 'AND' in condition:
                        cond_parts = condition.split('AND')
                        condition = '(' + cond_parts[0].strip() + ') and (' + cond_parts[1].strip() + ')'
                    elif 'OR' in condition:
                        cond_parts = condition.split('OR')
                        condition = '(' + cond_parts[0].strip() + ') or (' + cond_parts[1].strip() + ')'

                    if self.evaluate_expression(condition):
                        result = self.evaluate_expression(expr_if)
                        output.append(result)
                        return result
                    else:
                        return None
                elif 'AND' in line:
                    separated_line = line.split(' AND ')
                    for item in separated_line:
                        item.strip()
                    for item in separated_line:
                        if not self.interpret(item):
                            return False
                    return True
                elif 'OR' in line:
                    separated_line = line.split('OR')
                    for item in separated_line:
                        item.strip()
                    for item in separated_line:
                        if self.interpret(item):
                            return True
                    return False
                elif '==' in line:
                    res = 0
                    var_length = 0
                    num_length = 0
                    seperated_line = line.split('==')
                    for item in seperated_line:
                        if item in self.variables:
                            var_length += 1

                        elif item.isdigit():
                            num_length += 1
                        elif '+' or '-' or '*' or '/' in item:
                            res = self.evaluate_expression(item)
                        if var_length == 1:
                            if res:
                                item1, item2 = seperated_line
                                if item1 in self.variables:
                                    return self.variables[item1] == int(item2)
                                elif item1.isdigit():
                                    return int(item1) == self.variables[item2]
                        elif var_length == 0:
                            num1, num2 = seperated_line
                            return int(num1) == int(num2)

                        if var_length == 1 and num_length == 1:
                            if seperated_line[0] in self.variables:
                                return self.variables[seperated_line[0]] == int(seperated_line[1])
                            elif seperated_line[0].isdigit():
                                return seperated_line[0] == self.variables[seperated_line[1]]
                            else:
                                print("can't evaluate Whether it's True or False")
                        if num_length == 2:
                            num1, num2 = seperated_line
                            return int(num1) == int(num2)
                        elif var_length == 2:
                            var1, var2 = seperated_line
                            return self.variables[var1] == self.variables[var2]


                elif '=' in line:
                    seperated_line = line.split('=')
                    if seperated_line[0] in self.variables:
                        self.variables[seperated_line[0]] = self.evaluate_expression(seperated_line[1])
                    elif seperated_line[0] not in self.variables and not seperated_line[0].isdigit():
                        self.variables[seperated_line[0]] = self.evaluate_expression(seperated_line[1])
                    else:
                        print("can't evaluate this expression")

                elif '>' in line:
                    separated_line = line.split('>')
                    if separated_line[0] in self.variables:
                        res = self.variables[separated_line[0]] > self.evaluate_expression(separated_line[1])
                        if res:
                            return res
                    elif separated_line[0].isdigit() and separated_line[1] in self.variables:
                        res = self.evaluate_expression(separated_line[0]) > self.variables[separated_line[1]]
                        if res:
                            return res
                    else:
                        res = self.evaluate_expression(separated_line[0]) > self.evaluate_expression(separated_line[1])
                        if res:
                            return res



                elif '<' in line:
                    separated_line = line.split('<')
                    if separated_line[0] in self.variables:
                         res = self.variables[separated_line[0]] < self.evaluate_expression(separated_line[1])
                         if res:
                             return res
                    elif seperated_line[0].isdigit() and seperated_line[1] in self.variables:
                        res = self.evaluate_expression(seperated_line[0]) < self.variables[seperated_line[1]]
                        if res:
                            return res
                    else:
                        res = self.evaluate_expression(seperated_line[0]) < self.evaluate_expression(seperated_line[1])
                        if res:
                            return res
                elif line in self.variables:
                    return self.variables[line]

                else:
                    return self.evaluate_expression(line)
        except Exception as e:
            print(f"Exception: {e}")
            return None


if __name__ == "__main__":
    input_user = []
    interpreter = ScriptInterpreter()
    try:

        while True:
            i = 0
            answer = input("Hi, Do u want to enter more than 1 line of code ? (yes/no)\n")
            if answer.lower() == 'yes':
                while True:
                    i += 1
                    input_line = input("enter here line "+str(i)+" below: (type done to end)\n")
                    if input_line.lower() == 'done':
                        break
                    input_user.append(input_line)
                for line in input_user:
                    interpreter.interpret(line)

            else:

                code = input(">> ")
                if code == "exit":
                    break
                output = interpreter.interpret(code)
                if output is not None:
                    print(output)
        print("Thank you for using our cool interpreter!")

    except KeyboardInterrupt:
        print("Thank you for using our cool interpreter!")
