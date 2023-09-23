from collections import deque

class Node:
    def __init__(self, value):
        self.__value = value
        self.children = []
        self.parents = []

    @property
    def value(self):
        return self.__value

    def append_child(self, node, path_cost):
        self.children.append((node, path_cost))
        node.parents.append((self, path_cost))

    def append_parent(self, node, path_cost):
        node.append_child(self, path_cost)

    def __repr__(self):
        values = [node.value for node, _ in self.children]
        return f'{self.__value} -> {values}'

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        return hash(self) == hash(other)


class LinkNode:
    def __init__(self, node, previous_node=None, cost_to_previous=0):
        self._node = node
        self._previous_node = previous_node
        self._cost_to_previous = cost_to_previous

    @property
    def node(self):
        return self._node
    
    @property
    def previous_node(self):
        return self._previous_node

    def get_total_cost(self):
        total_cost = 0
        node = self
        while node.previous_node:
            total_cost += node._cost_to_previous
            node = node.previous_node
        return total_cost

    def solve(self):
        solution = deque()
        node = self
        returned_str = ''
        while node:
           solution.appendleft(f' {node.node.value} |')
           node = node.previous_node
    
        while solution:
            returned_str += solution.popleft()

        return returned_str

    def set_previous_node(self, node, path_cost):
        self._previous_node = node 
        self._cost_to_previous = path_cost

    def __repr__(self):
        returned_string = ''
        if self._previous_node:
            returned_string += f'{str(self._previous_node.node.value)} -> '
        else:
            returned_string += f'| '
        returned_string += f'{str(self._node.value)}'

        return returned_string
