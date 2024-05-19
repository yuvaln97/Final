#Demonstrate the capabilities with a complex program
from Q7 import Interpreter

program = """
 x = 5;
 y = 0;
 while x > 0 do
     if x > 3 then
         y = y + x;
     end
     x = x - 1;
 end
 print(y);
 """

program2 = """
result = 0;
for i = 1 to 10 do
    if i % 2 == 0 then
        result = result + i;
    end
end
print(result);
"""

program3 = """
a = 5;
b = 3;
if a > b then
    max_value = a;
else
    max_value = b;
end
print(max_value);
"""


interpreter = Interpreter()
interpreter.interpret(program)
