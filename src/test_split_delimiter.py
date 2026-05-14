import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_bold_basic(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_italic_basic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_code_basic(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_no_delimiter(self):
        node = TextNode("plain text with no special formatting", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_multiple_delimiters_bold(self):
        node = TextNode("**first** and **second** bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], TextNode("first", TextType.BOLD))
        self.assertEqual(result[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("second", TextType.BOLD))
        self.assertEqual(result[3], TextNode(" bold", TextType.TEXT))

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_early_return_on_first_non_text(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("**should be ignored**", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 2)

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at the beginning", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[1], TextNode(" at the beginning", TextType.TEXT))

    def test_delimiter_at_end(self):
        node = TextNode("ends with **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("ends with ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))

    def test_empty_input_list(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("**bold**", TextType.TEXT),
            TextNode("plain text", TextType.TEXT),
            TextNode("_italic_", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # Only first node is split; second and third stay as-is
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[1], TextNode("plain text", TextType.TEXT))
        self.assertEqual(result[2], TextNode("_italic_", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()
