#!/usr/bin/env python3
import unittest
from functions import split_nodes_images, split_nodes_links
from textnode import TextNode, TextType

class TestSplitNodesImages(unittest.TestCase):
    """Tests for split_nodes_images (using corrected implementation)."""

    def test_empty_list(self):
        self.assertEqual(split_nodes_images([]), [])

    def test_no_images(self):
        node = TextNode("Plain text with no images", TextType.TEXT)
        self.assertEqual(split_nodes_images([node]), [node])

    def test_non_text_node_passthrough(self):
        bold_node = TextNode("**bold**", TextType.BOLD)
        result = split_nodes_images([bold_node])
        self.assertEqual(result, [bold_node])

    def test_single_image_middle(self):
        node = TextNode("This is an image ![alt text](https://example.com/img.jpg) here.", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_image_at_start(self):
        node = TextNode("![logo](https://example.com/logo.png) Welcome!", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
            TextNode(" Welcome!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_image_at_end(self):
        node = TextNode("Check this out: ![photo](https://example.com/photo.jpg)", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("Check this out: ", TextType.TEXT),
            TextNode("photo", TextType.IMAGE, "https://example.com/photo.jpg"),
        ]
        self.assertEqual(result, expected)

    def test_only_image(self):
        node = TextNode("![sole](https://example.com/sole.png)", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [TextNode("sole", TextType.IMAGE, "https://example.com/sole.png")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode("![first](url1) middle text ![second](url2) end text", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2"),
            TextNode(" end text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_images(self):
        node = TextNode("![a](1)![b](2)![c](3)", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("a", TextType.IMAGE, "1"),
            TextNode("b", TextType.IMAGE, "2"),
            TextNode("c", TextType.IMAGE, "3"),
        ]
        self.assertEqual(result, expected)

    def test_empty_alt_text(self):
        node = TextNode("![](https://example.com/empty-alt.jpg) caption", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("", TextType.IMAGE, "https://example.com/empty-alt.jpg"),  # alt can be empty
            TextNode(" caption", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_special_characters_in_alt(self):
        node = TextNode('![alt with spaces & symbols!](https://ex.com/i.jpg) text', TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode('alt with spaces & symbols!', TextType.IMAGE, "https://ex.com/i.jpg"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLinks(unittest.TestCase):
    """Tests for split_nodes_links (using corrected implementation)."""

    def test_empty_list(self):
        self.assertEqual(split_nodes_links([]), [])

    def test_no_links(self):
        node = TextNode("Plain text with no links", TextType.TEXT)
        self.assertEqual(split_nodes_links([node]), [node])

    def test_non_text_node_passthrough(self):
        italic_node = TextNode("*italic*", TextType.ITALIC)
        result = split_nodes_links([italic_node])
        self.assertEqual(result, [italic_node])

    def test_single_link_middle(self):
        node = TextNode("Click [here](https://example.com) for more.", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" for more.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_link_at_start(self):
        node = TextNode("[Home](https://example.com/home) page content", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Home", TextType.LINK, "https://example.com/home"),
            TextNode(" page content", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_link_at_end(self):
        node = TextNode("Visit our [site](https://example.com/site)", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Visit our ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://example.com/site"),
        ]
        self.assertEqual(result, expected)

    def test_only_link(self):
        node = TextNode("[only link](https://example.com/only)", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [TextNode("only link", TextType.LINK, "https://example.com/only")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("[Google](https://google.com) and [GitHub](https://github.com) are great", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(" are great", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_links(self):
        node = TextNode("[one](1)[two](2)[three](3)", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("one", TextType.LINK, "1"),
            TextNode("two", TextType.LINK, "2"),
            TextNode("three", TextType.LINK, "3"),
        ]
        self.assertEqual(result, expected)

    def test_link_with_special_text(self):
        node = TextNode('See [our "awesome" page!](https://ex.com) now', TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode('our "awesome" page!', TextType.LINK, "https://ex.com"),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(result, expected)




if __name__ == "__main__":
    unittest.main(verbosity=2)
