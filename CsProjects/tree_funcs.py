""" File: tree_funcs.py.py
    Author: Kyle Walker
    Purpose: A collection of functions relating to binary tree operations.
            Some have use loops while others use recursion, but they all
            take a root node as an argument to solve a simple function.

"""

from tree_node import TreeNode

def tree_count(root):
    '''
        This function returns the number of nodes in the binary tree.
        Arguments: root: The root node of the binary tree.
        Returns: recursive sum of all nodes, or None when empty.
        PreCondtions: None
    '''
    if root is None:
        return 0
    else:
        return (tree_count(root.left) + 1 + tree_count(root.right))

def tree_count_1_child(root):
    '''
        This function returns the number of nodes in the binary tree
        that only have one child.
        Arguments: root: The root node of the binary tree.
        Returns: recursive sum of all single child root nodes, or
        None when empty.
        PreConditions: None
    '''
    if root is None:
        return 0
    if root.right is None and root.left is not None:
        return tree_count_1_child(root.left) + 1
    if root.left is None and root.right is not None:
        return tree_count_1_child(root.right) + 1
    return tree_count_1_child(root.left) + tree_count_1_child(root.right)

def tree_sum(root):
    '''
        This function returns the total value of all nodes in the
        binary tree.
        Arguments: root: The root node of the binary tree.
        Returns: recursive sum of all node values, or 0 when empty.
        PreConditions: None
    '''
    if root is None:
        return 0
    return root.val + tree_sum(root.left) + tree_sum(root.right)

def tree_print(root):
    '''
        This function prints each value of the binary tree's nodes
        Arguments: root: The root node of the binary tree.
        Returns: None, only prints root.val for each node
        PreConditions: None
    '''
    if root is None:
        return
    tree_print(root.right)
    tree_print(root.left)
    print(root.val)

def tree_print_leaves(root):
    '''
        This function prints the values of only the leaf nodes of
        the tree (nodes with no children)
        Arguments: root: The root node of the binary tree.
        Returns: None, only prints root.val for leaves.
        PreConditions: None
    '''
    if root is None:
        return
    if root.left is None and root.right is None:
        print(root.val)
    tree_print_leaves(root.right)
    tree_print_leaves(root.left)

def bst_search_loop(root, val):
    '''
        This function runs a binary search algorithm through
        the sorted tree to locate the node containing the given
        value.
        Arguments: root: The root node of the binary tree.
        val: the value to be found in the tree.
        Returns: root (node) pointer to node with value,
        or None when empty.
        PreConditions: Binary tree must be in sorted BST order
    '''
    if root is None:
        return None
    while root is not None:
        if root.val == val:
            return root
        elif root.val < val:
            root = root.right
        elif root.val > val:
            root = root.left

def tree_search(root, val):
    '''
        This function runs a recursive search through any binary
        tree to locate the node containing the argued value.
        Arguments: root: The root node of the binary tree.
        val: the value to be found in the tree.
        Returns: root (node) pointer to node with value,
        or None when empty.
        PreConditions: None
    '''
    if root is not None:
        if root.val == val:
            return root
        elif tree_search(root.left, val) is not None:
            return tree_search(root.left, val)
        elif tree_search(root.right, val) is not None:
            return tree_search(root.right, val)
        else:
            return None
    else:
        return None

def bst_max_loop(root):
    '''
        This function uses a loop to find the node with the
        largest value in a sorted Binary Search Tree.
        Arguments: root: The root node of the binary tree.
        Returns: root.val of node with maximum value.
        or None when empty.
        PreConditions: Tree must be sorted in BST format.
    '''
    if root is None:
        return None
    while root is not None:
        if root.right is None:
            return root.val
        else:
            root = root.right

def tree_max(root):
    '''
        This function uses recursion to find the node with the
        largest value in any binary tree.
        Arguments: root: The root node of the binary tree.
        Returns: max_val: the maximum value present in the
        tree's nodes, or None when empty.
        PreConditions: None
    '''
    if root is None:
        return None
    max_val = root.val
    max_left = tree_max(root.left)
    max_right = tree_max(root.right)
    if max_left is not None and max_left > max_val:
        max_val = max_left
    if max_right is not None and max_right > max_val:
        max_val = max_right
    return max_val

def inOrderChildren(root):
    nodes = []
    if root is not None:
        if root.left is None and root.right is not None:
            nodes.append(root)
        elif root.right is None and root.left is not None:
            nodes.append(root)
        return inOrderChildren(root.left)
        return inOrderChildren(root.right)
    print(nodes)
    return nodes


def pre_order_array(root):
    if root is None:
        return []
    return [root.val] + \
        pre_order_array(root.left) + \
        pre_order_array(root.right)

root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(5)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)

def get_depth_of_val(root, val, soFar=0):
     if root is None:
         return -1
     if root.val == val:
         return soFar
     if val < root.val:
         get_depth_of_val(root.left, val, soFar+1)
     else:
         get_depth_of_val(root.right, val, soFar+1)

get_depth_of_val(root, 3, soFar=0)