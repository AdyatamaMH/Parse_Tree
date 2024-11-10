from anytree import Node, RenderTree

class LL1Parser:
    def __init__(self):
        self.grammar = {
            'S': ['A B C'],
            'A': ['ε', 'U 1'],
            'U': ['0 U', '1 U', 'ε'],
            'C': ['ε', '1 U'],
            'B': ['0 D 0', '0 B 0'],
            'D': ['1 U 1', '1']
        }
        self.parsing_table = {
            'S': {'0': 'A B C', '1': 'A B C', '$': 'A B C'},
            'A': {'0': 'U 1', '1': 'U 1', '$': 'ε'},
            'U': {'0': '0 U', '1': '1 U', '$': 'ε'},
            'C': {'1': '1 U', '$': 'ε'},
            'B': {'0': '0 D 0', '$': 'ε'},
            'D': {'1': '1 U 1', '$': '1'}
        }
        self.stack = []
        self.parse_tree_root = Node("S") 
        self.node_counter = 0
        self.error_message = None

    def parse(self, input_string):
        self.stack = [(self.parse_tree_root, 'S')]
        index = 0
        input_string += '$'

        while self.stack:
            current_node, top = self.stack.pop()
            current_input = input_string[index] if index < len(input_string) else None

            if top == 'ε':
                Node("ε", parent=current_node)
                continue

            if top == current_input:
                index += 1
                continue

            if top in self.parsing_table:
                rule = self.parsing_table[top].get(current_input)
                if rule:
                    rule_parts = rule.split()
                    for part in reversed(rule_parts):

                        child_node = Node(part, parent=current_node)
                        self.stack.append((child_node, part))
                else:
                    self.error_message = f"Parse Error: No rule for '{top}' with '{current_input}'"
                    break
            else:
                self.error_message = f"Parse Error: Unexpected symbol '{current_input}' at position {index}"
                break

        if index == len(input_string) - 1 and not self.error_message:
            print("Parse Successful")
            return True
        else:
            if not self.error_message:
                self.error_message = "Parse Error: Incomplete parsing"
            return False

    def display_parse_tree(self):
        print("Parse Tree:")
        for pre, fill, node in RenderTree(self.parse_tree_root):
            print(f"{pre}{node.name}")

        if self.error_message:
            print(self.error_message)

if __name__ == "__main__":
    print("***THIS IS A SIMPLE LL(1) PARSER***")
    input_string = input("Please, input the string: ")
    
    parser = LL1Parser()
    parser.parse(input_string)
    parser.display_parse_tree()

