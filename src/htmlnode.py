#!/usr/bin/env python3

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_list = []
        if self.props == None or self.props == "":
            return ""

        for item in self.props:
             props_list.append(f' {item}="{self.props[item]}"')

        return props_list

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All Leaf Nodes must have a value")

        if self.tag == None:
            return self.value

        html_props = self.props_to_html()
        html = f"<{self.tag}"
        for prop in html_props:
            string = f"{prop}"
            html += string

        html += f">{self.value}</{self.tag}>"
        return html

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
