class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

# Build the tree
A = Node('A')
B = Node('B')
C = Node('C')
D = Node('D')
E = Node('E')
F = Node('F')
G = Node('G')
H = Node('H')

A.children = [B, C, D]
B.children = [E, F]
C.children = [G]
G.children = [H]

def dls(node, target, depth, visited_at_level):
    if node is None:
        return None
    visited_at_level.append(node.value)
    if node.value == target:
        return node
    if depth == 0:
        return None
    for child in node.children:
        found = dls(child, target, depth - 1, visited_at_level)
        if found:
            return found
    return None

def iddfs(root, target, max_depth):
    found_node = None
    for depth in range(max_depth + 1):
        visited_at_level = []
        dls(root, target, depth, visited_at_level)
        print(f"Depth {depth}: Visited nodes -> {', '.join(visited_at_level)}")
        if target in visited_at_level:
            found_node = target
            break
    if found_node:
        print(f"\nResult: Found '{target}' at depth {depth}")
    else:
        print(f"\nResult: '{target}' not found within depth {max_depth}")

# Example usage
target = 'H'
iddfs(A, target, max_depth=4)
