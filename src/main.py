#!/usr/bin/env python3
from textnode import TextNode
from textnode import TextType
def main():
    node = TextNode("This is some anchor text", TextType.link, "https://www.boot.dev")
    print(node)

main()
