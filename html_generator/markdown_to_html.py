import re


BOLD = r"(?<!\\)\*\*([^\\]+?(?:\\.[^\\]*?)*?)\*\*"
ITALICS = r"(?<!\\)\*([^*\\]+(?:\\.[^*\\]*)*?)\*"
ORDERED_LIST = r"^[0-9]+\.\s(.+)$"
UNORDERED_LIST = r"^-\s(.+)$"
LINKS = r"\[(.+?)\]\((.+?)\)"


def parse_markdown_to_html(text: str) -> str:
    pass


if __name__ == "__main__":
    test_string = """*This text should be italicized.*
**This text should be bolded**
***This text should be both***
*This text **should be a mix***
[My nifty link](https://google.com)"""

    parse_markdown_to_html(test_string)
