#Add while loops with conditional continuation
class Interpreter:
    def __init__(self, max_code_length=1000, max_result_length=100, max_variables=10):
        self.variables = {}
        self.max_code_length = max_code_length
        self.max_result_length = max_result_length
        self.max_variables = max_variables

    def interpret(self, program):
        if len(program) > self.max_code_length:
            print("Error: Program code exceeds maximum length.")
            return

        statements = [s.strip() for s in program.split(';') if s.strip()]  # Split program into statements
        for statement in statements:
            result = self.evaluate(statement)
            if result is not None:
                result_str = str(result)
                if len(result_str) > self.max_result_length:
                    print("Error: Result length exceeds maximum length.")
                    return
                print(result_str)

    def evaluate(self, statement):
      #  # Updated evaluation logic to handle while loops
        print("Statement:", statement)  # Add this line for debugging
        tokens = statement.strip().split()
     #   print("Tokens:", tokens)
        if tokens[0] == 'print':
            variable_name = tokens[1]
            if variable_name in self.variables:
                print(self.variables[variable_name])
            else:
                print("Variable not found:", variable_name)
            return  # Add this line
        elif '=' in statement:
            variable, _, expr = statement.partition('=')
            variable = variable.strip()
            result = self.evaluate_expression(expr)
            self.variables[variable] = result
        elif tokens[0] == 'if':
            return self.evaluate_if_then(statement)
        elif tokens[0] == 'while':
            return self.evaluate_while_loop(statement)
        else:
            return self.evaluate_boolean_expression(statement)

    def evaluate_while_loop(self, statement):
        # Implement while loop evaluation
        pass

    def evaluate_expression(self, expression):
        # Implement arithmetic expression evaluation
        pass

    def evaluate_boolean_expression(self, expression):
        # Implement Boolean expression evaluation
        pass

    def evaluate_if_then(self, statement):
        # Implement if-then statement evaluation
        pass
