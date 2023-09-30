# From Lark's Documentation:
# The transfomer processes the parse tree bottom-up, starting from the leaves and going up to the root.
# For each node it calls the related method according to the nodes's data, and uses the returned value to replace the
# node, creating a new structure. When the transformer doesn't find the method for a node, it simply returns the node

# A transformer without methods essentially performs a non-memorized partial deepcopy


from lark.visitors import Transformer
from SymbolTable import symbol_table

# TODO capire se mettere v_args inline=True o no
# con v_args si possono specificare una serie di parametri: inline (i children dell'albero sono passati come *args e non come una lista)
#  meta (if meta=True) dà una serie di info come riga e colonna a cui ci troviamo
# TODO l'interpreter sembra una sorta di estensione del transformer, dove ad esempio si aggiunge la gestione dell'if o del while



class TreeToJS(Transformer):
    """
    This class extends Lark's transformer class, which provides a convenient interface to process the parse tree that
    Lark returns. Each method of the class corresponds to one of the rules in the grammar.
    """
    def print_statement(self, args):
        print(args[0])

    def input_statement(self, args):
        return input(args[0])

    def variable_statement(self, args):
        if len(args) == 2:  # variable declaration (es. let a)
            symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': 'undefined', 'type': 'undefined'})
            return 'undefined'
        elif len(args) == 3:  # variable assignment (es. a = 2)
            #TODO gestire SyntaxError identifier already declared (es. const a = 2; let a = 3;) fai check su symbol_table[args[0].value]['declaration'] == 'const'
            if args[0].value in symbol_table.table.keys():
                symbol_table.update(args[0].value, {'declaration': symbol_table.find(args[0].value)['declaration'], 'value': args[2], 'type': type(args[2])})
            else:  # the variable has not been declared yet
                symbol_table.insert(args[0].value, {'declaration': 'var', 'value': args[2], 'type': type(args[2])})
            return args[2]
        elif len(args) == 4:  # variable declaration and assignment (es. let a = 2)
            #TODO gestire SyntaxError identifier already declared (es. const a = 2; let a = 3;)
            symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': args[3], 'type': type(args[3])})
            return args[3]

    def variable_assignment(self, args):
        #TODO gestire se la variabile non è stata dichiarata, se il valore non è un numero
        if args[0] == '++':
            symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': symbol_table.find(args[1])['value'] + 1, 'type': type(symbol_table.find(args[1])['value'] + 1)})
            return symbol_table.find(args[1])['value']
        elif args[0] == '--':
            symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': symbol_table.find(args[1])['value'] - 1, 'type': type(symbol_table.find(args[1])['value'] - 1)})
        elif args[1] == '+=':
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] + args[2], 'type': type(symbol_table.find(args[0])['value'] + args[2])})
        elif args[1] == '-=':
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] - args[2], 'type': type(symbol_table.find(args[0])['value'] - args[2])})
        elif args[1] == '*=':
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] * args[2], 'type': type(symbol_table.find(args[0])['value'] * args[2])})
        elif args[1] == '/=':
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] / args[2], 'type': type(symbol_table.find(args[0])['value'] / args[2])})
        elif args[1] == '++':
            value = symbol_table.find(args[0])['value']
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] + 1, 'type': type(symbol_table.find(args[0])['value'] + 1)})
            return value
        elif args[1] == '--':
            value = symbol_table.find(args[0])['value']
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': symbol_table.find(args[0])['value'] - 1, 'type': type(symbol_table.find(args[0])['value'] - 1)})
            return value
        return symbol_table.find(args[0])['value']

    def return_statement(self, args):
        return args[1]

    def logical_and(self, args):
        return args[0] and args[1]

    def logical_or(self, args):
        return args[0] or args[1]

    def equality(self, args):
        return args[0] == args[1]

    def inequality(self, args):
        return args[0] != args[1]

    def greater_than(self, args):
        return args[0] > args[1]

    def greater_than_or_equal(self, args):
        return args[0] >= args[1]

    def less_than(self, args):
        return args[0] < args[1]

    def less_than_or_equal(self, args):
        return args[0] <= args[1]

    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    def negative(self, args):
        return -int(args[0])

    def logical_not(self, args):
        return not args[0]

    def template_literal(self, args):
        temp = ""
        for arg in args: #TODO rendi più efficiente modificando la grammatica
            if type(arg) in [float, int, bool]:
                temp += str(arg) + " "
            else:
                temp += str(arg)
        return temp

    def factor(self, args):
        """
        Substitute the value in the explored nodes
        :param args:
        :return:
        """
        if args[0].type == 'NUMBER':
            return float(args[0].value)
        elif args[0].type == 'STRING':
            return str(args[0].value[1:-1])
        elif args[0].type == 'BOOL':
            if args[0].value == 'true':
                return True
            else:
                return False
        elif args[0].type == 'IDENTIFIER':
            return symbol_table.find(args[0].value)['value']
        return args[0].value

    def term(self, args):
        return args[0]

    def expression(self, args):
        return args[0]