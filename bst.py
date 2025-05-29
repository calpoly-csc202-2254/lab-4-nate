import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree: TypeAlias = Union[None, "Node"]

@dataclass(frozen=True)
class Node:
    val: Any
    left: BinTree
    right: BinTree

# Binary tree class with built-in methods
@dataclass(frozen=True)
class frozenBinarySearchTree:
    tree: BinTree
    comes_before: Callable[[Any, Any], bool]

    # Determines if binary tree is empty
    def is_empty(self) -> bool:
        return self.tree == None
    
    # Returns tree with inserted element
    def insert(self, val, cur_tree: BinTree = "BR") -> BinTree:
        if cur_tree == "BR":
            cur_tree = self.tree
        match cur_tree:
            case None:
                return Node(val, None, None)
            case Node(v, l, r):
                if self.comes_before(v, val):
                    return Node(v, self.insert(val, cur_tree.left), r)
                else:
                    return Node(v, l, self.insert(val, cur_tree.right))
                
    # Determines if binary tree has value
    def lookup(self, val, cur_tree: BinTree = "BR") -> bool:
        if cur_tree == "BR":
            cur_tree = self.tree
        match cur_tree:
            case None:
                return False
            case Node(v, l, r):
                if not self.comes_before(v, val) and not self.comes_before(val, v):
                    return True
                elif self.comes_before(v, val):
                    return self.lookup(val, l)
                else:
                    return self.lookup(val, r)


class TestCase(unittest.TestCase):
    def test_none(self):
        empty = frozenBinarySearchTree(None, lambda a, b : a < b)
        not_empty = frozenBinarySearchTree(Node(0, None, None), lambda a, b : a < b)
        self.assertEqual(empty.is_empty(), True)
        self.assertEqual(not_empty.is_empty(), False)

    def test_insert(self):
        my_class = frozenBinarySearchTree(None, lambda a, b : a < b)
        self.assertEqual(Node(5, None, None), my_class.insert(5))
        new_class = frozenBinarySearchTree(Node(5, Node(4, None, None), Node(6, None, None)), lambda a, b : a > b)
        self.assertEqual(Node(5, Node(4, None, None), Node(6, None, Node(8, None, None))), new_class.insert(8))

        tr = frozenBinarySearchTree(None, lambda a, b : a > b)
        tr = frozenBinarySearchTree(tr.insert(5), lambda a, b : a > b)
        tr = frozenBinarySearchTree(tr.insert(10), lambda a, b : a > b)
        tr = frozenBinarySearchTree(tr.insert(3), lambda a, b : a > b)
        tr = frozenBinarySearchTree(tr.insert(2), lambda a, b : a > b)
        tr = frozenBinarySearchTree(tr.insert(7), lambda a, b : a > b)
        self.assertEqual(Node(5,Node(3,Node(2,None,None),None),Node(10,Node(7,None,None),None)), tr.tree)

        self.assertEqual(tr.lookup(9), False)
        self.assertEqual(tr.lookup(5), True)
        self.assertEqual(tr.lookup(3), True)
        self.assertEqual(tr.lookup(2), True)
        self.assertEqual(tr.lookup(7), True)
        self.assertEqual(tr.lookup(10), True)
        self.assertEqual(tr.lookup(-1), False)
        self.assertEqual(tr.lookup(10000), False)


if __name__ == '__main__':
    unittest.main()

new_class = frozenBinarySearchTree(Node(5, Node(4, None, None), Node(6, None, None)), lambda a, b : a > b)
print(Node(5, Node(4, None, None), Node(6, None, Node(8, None, None))))
print(new_class.insert(8))

