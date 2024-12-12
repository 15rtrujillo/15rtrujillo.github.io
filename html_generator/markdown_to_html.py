import re


BOLD = r"(?<!\\)\*\*([^\\]+?(?:\\.[^\\]*?)*?)\*\*"
RE_BOLD = re.compile(BOLD)
UNDERLINED = r"(?<!\\)__([^\\]+?(?:\\.[^\\]*?)*?)__"
RE_UNDERLINED = re.compile(UNDERLINED)
ITALICS = r"(?<!\\)\*([^*\\]+(?:\\.[^*\\]*)*?)\*"
RE_ITALICS = re.compile(ITALICS)
ORDERED_LIST = r"^[0-9]+\.\s(.+)$"
RE_ORDERED_LIST = re.compile(ORDERED_LIST)
UNORDERED_LIST = r"^-\s(.+)$"
RE_UNORDERED_LIST = re.compile(UNORDERED_LIST)
LINKS = r"\[(.+?)\]\((.+?)\)"
RE_LINKS = re.compile(LINKS)


def parse_text_decoration(text: str, tag: str, pattern: re.Pattern[str]) -> str:
    matches = re.finditer(pattern, text)
    for found in matches:
        print(found.string, found.group(1))


def parse_markdown_to_html(text: str) -> str:
    for line in text.split("\n"):
        parse_text_decoration(line, "em", RE_ITALICS)


if __name__ == "__main__":
    test_string = """*This text should be italicized.*
**This text should be bolded**
***This text should be both***
*This text **should be a mix***
[My nifty link](https://google.com)"""

    parse_markdown_to_html(test_string)
