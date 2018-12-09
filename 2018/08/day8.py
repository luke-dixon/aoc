
from collections import namedtuple


with open('input8.txt') as f:
  data = [int(x) for x in f.read().split()]


Node = namedtuple('Node', [
  'num_children',
  'num_metadata',
  'children',
  'metadata',
  'parent'])

def build_tree(data, parent=None):
  # create the node
  node = Node(data.pop(0), data.pop(0), [], [], parent)

  # base case is that there are no more children
  for n in range(node.num_children):
    # The length of data will be less than what we started with
    node.children.append(build_tree(data, node))

  # Add the metadata to the node
  for n in range(node.num_metadata):
    node.metadata.append(data.pop(0))

  # return the node so we can append it to the parent's children list
  return node


tree_head = build_tree(data, None)


def sum_metadata(node):
  return sum(node.metadata) + sum([sum_metadata(child) for child in node.children])


print('Day 8 Part 1 Answer: %d' % (sum_metadata(tree_head)))


def calc_value(node):
  if node.num_children == 0:
    # base case
    return sum(node.metadata)

  # calculate the value only for children described in the metadata
  value = 0
  for n in node.metadata:
    try:
      value += calc_value(node.children[n - 1])
    except IndexError:
      # skip children that don't exist
      pass

  return value


print('Day 8 Part 2 Answer: %d' % (calc_value(tree_head)))
