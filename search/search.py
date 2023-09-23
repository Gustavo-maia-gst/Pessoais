from node import Node, LinkNode
from tree import *
from collections import deque


def in_collection(collection, node):
    for element in collection:
        if element.node == node:
            return True
    return False


def find(collection, node):
    for element in collection:
        if element.node == node:
            return element
    return None


def search(root, desired):
    frontier = deque([LinkNode(root)])
    explored = set()

    while frontier:
        frontier = deque(sorted(frontier, key=lambda node: node.get_total_cost()))
        link_node = frontier.popleft()
        node = link_node.node
        if node.value == desired:
            return link_node.solve()
        if node.children:
            children = sorted(node.children, key=lambda child: child[1])
            for child, path_cost in children:
                if in_collection(explored, child):
                    continue
                if (link_child := find(frontier, child)):
                    current_path = link_child.get_total_cost()
                    eventual_link_child = LinkNode(child, link_node, path_cost)
                    eventual_path = eventual_link_child.get_total_cost()
                    if eventual_path < current_path:
                        link_child.set_previous_node(link_node, path_cost)
                    continue

                frontier.append(LinkNode(child, link_node, path_cost)) 

        explored.add(link_node)

    return 'Não existe caminho'

returned = search(arad, bucharest)
print(returned)
