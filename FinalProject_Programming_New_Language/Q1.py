class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program):
        statements = program.split(';')
        for statement in statements:
            result = self.evaluate(statement)
            if result is not None:
                print(result)

    def evaluate(self, statement):
        # Implement the evaluation logic here
        # For simplicity, let's just handle assignments and print statements
        tokens = statement.strip().split()
        if tokens[0] == 'print':
            return self.variables.get(tokens[1], "Variable not found")
        elif '=' in statement:
            variable, _, expr = statement.partition('=')
            variable = variable.strip()
            result = self.evaluate_expression(expr)
            self.variables[variable] = result
            return None
        else:
            return self.evaluate_expression(statement)

    def evaluate_expression(self, expression):
        # Implement arithmetic expression evaluation
        pass

# Example Usage
interpreter = Interpreter()
interpreter.interpret("x = 5; y = x + 3; print(y)")
