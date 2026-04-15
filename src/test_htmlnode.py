#!/usr/bin/env python3

import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("a", "test", [], {"href": "https://www.google.com"})
        print(node.props_to_html())

    def test_leaf(self):
        node = LeafNode("a", "test", {"href": "https://www.google.com"})
        print(node.to_html())
if __name__ == "__main__":
    unittest.main()
