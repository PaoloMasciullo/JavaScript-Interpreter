# JavaScript-Interpreter in Python
A JavaScript Interpreter coded in Python using Lark parsing and lexing library

Lark: https://lark-parser.readthedocs.io/en/stable/# \
JavaScript grammar reference: https://tc39.es/ecma262/ \
JavaScript Error Reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors?retiredLocale=it

## Restriction of the grammar adopted 
### Data types
- Number
- Boolean
- String
- Array

### Arithmetic Operations (with type coercition simulation)
- addition (+)
- subtraction (-)
- multiplication (*)
- division (/)

### Arithmetic Operations (with type coercition simulation)
- equal (==)
- not equal (!=)
- strict equal (===)
- strict not equal (!==)
- greater than (>)
- less than (<)
- greater than or equal to (>=)
- less than or equal to (<=)

### Assignment operations
- identifier += expression
- identifier -= expression
- identifier *= expression
- identifier /= expression
- identifier ++
- ++ identifier
- identifier --
- -- identifier

### Logical operations (with type coercition simulation)
- not (!)
- or (||)
- and (&&)

### Branching operations
- if
- if else
- operatore condizionale ternario (condition ? true : false)

### Loop operations
- while

### Input instruction
-  keyboard input (prompt)

### Output instruction:
- print in console (console.log)
- template literals

### Function declaration
- function ID (parameters) { body }

### Function call
- ID (arguments)

### Array
- array declaration
- array access

### Managed errors
- lexical errors (typing errors)
- syntax error
    - non-matched parenthesis
- semantic errors
    - Reference error
