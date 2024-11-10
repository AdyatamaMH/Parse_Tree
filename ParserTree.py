from anytree import Node, RenderTree

class LL1Parser:
    def __init__(self):
        self.grammar = {
            'S': ['A B C'],
            'A': ['U 1', 'ε'],
            'U': ['0 U', '1 U', 'ε'],
            'B': ['0 D 0', '0 B 0'],
            'D': ['1 U 1', '1'],
            'C': ['1 U', 'ε']
        }
        self.parsing_table = {
            'S': {'0': 'A B C', '1': 'A B C', '$': 'A B C'},
            'A': {'0': 'U 1', '1': 'U 1', '$': 'ε'},
            'U': {'0': '0 U', '1': '1 U', '$': 'ε'},
            'B': {'0': '0 D 0', '$': 'ε'},
            'D': {'1': '1 U 1', '$': '1'},
            'C': {'1': '1 U', '$': 'ε'}
        }
        self.root = Node("S")
        self.error_message = None

    def apply_rule(self, symbol, current_input):
        if symbol in self.parsing_table:
            return self.parsing_table[symbol].get(current_input)
        return None

    def expand_node(self, parent_node, rule):
        rule_parts = rule.split()
        children = []
        for part in rule_parts:
            child_node = Node(part, parent=parent_node)
            children.append(child_node)
        return children

    def parse(self, input_string):
        input_string += '$'
        stack = [(self.root, 'S')]
        index = 0

        while stack:
            current_node, top = stack.pop()
            current_input = input_string[index] if index < len(input_string) else None

            if top == 'ε':
                continue

            if top == current_input:
                index += 1
                continue

            rule = self.apply_rule(top, current_input)
            if rule:
                children = self.expand_node(current_node, rule)
                stack.extend(reversed([(child, child.name) for child in children]))
            else:
                self.error_message = f"Parse Error: No rule for '{top}' with '{current_input}'"
                break

        if index == len(input_string) - 1 and not self.error_message:
            return True
        else:
            if not self.error_message:
                self.error_message = "Parse Error: Incomplete parsing"
            return False

    def display_parse_tree(self):
        print("Parse Tree:")
        for pre, fill, node in RenderTree(self.root):
            print(f"{pre}{node.name}")
        if self.error_message:
            print(self.error_message)

if __name__ == "__main__":
    print("***THIS IS A SIMPLE LL(1) PARSER***")
    input_string = input("Please, input the string: ")

    parser = LL1Parser()
    parser.parse(input_string)
    parser.display_parse_tree()
