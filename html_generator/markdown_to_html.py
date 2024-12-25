import re


class HTMLList:
    def __init__(self):
        self.start: int | None = None
        self.end: int | None = None
        self.start_number: int | None = None
        self.elements: list[str] = []


# Text decorations
ASTERISKS = r"\*+(?<!\\)(.+?)(?<!\\)\*+"
RE_ASTERISKS = re.compile(ASTERISKS)
UNDERLINED = r"(?<!\\)__([^\\]+?(?:\\.[^\\]*?)*?)__"
RE_UNDERLINED = re.compile(UNDERLINED)

# Lists
ORDERED_LIST = r"^([0-9])+\.\s(.+)$"
RE_ORDERED_LIST = re.compile(ORDERED_LIST)
UNORDERED_LIST = r"^-\s(.+)$"
RE_UNORDERED_LIST = re.compile(UNORDERED_LIST)

# Misc
LINKS = r"\[(.+?)\]\((.+?)\)"
RE_LINKS = re.compile(LINKS)


def parse_text_decoration(line: str, pattern: re.Pattern[str]) -> str:
    """Parses a line for underline, italics, and bold"""
    new_line = line
    
    matches = re.finditer(pattern, line)
    for found in matches:
        match_text = found.group(0)
        group_text = found.group(1)
        html = ""
        if pattern == RE_ASTERISKS:
            if match_text.startswith("***"):
                html += "<em><strong>"
                html += group_text
                html += "</em></strong>"
            elif match_text.startswith("**"):
                html += "<strong>"
                html += group_text
                html += "</strong>"
            else:
                html += "<em>"
                html += group_text
                html += "</em>"
        elif pattern == RE_UNDERLINED:
            html += "<u>"
            html += group_text
            html += "</u>"
        else:
            raise ValueError("Unrecognized text decoration pattern!")

        new_line = new_line.replace(match_text, html)
    
    return new_line


def parse_links(line: str) -> str:
    """Parses a line for links"""
    new_line = line
    matches = re.finditer(RE_LINKS, line)
    for found in matches:
        match_text = found.group(0)
        link_text = found.group(1)
        link_url = found.group(2)
        new_line = new_line.replace(match_text, f"<a href=\"{link_url}\">{link_text}</a>")
    return new_line


def parse_numbered_list(text: str) -> str:
    """Parses text for numbered lists"""
    lists: list[HTMLList] = []
    current_list: HTMLList | None = None
    # Loop through each line in the text
    for line in text.split("\n"):
        found = re.match(RE_ORDERED_LIST, line)
        if found is None:
            if current_list is not None:
                lists.append(current_list)
                current_list = None
            continue

        if current_list is None:
            current_list = HTMLList()

        if current_list.start is None:
            current_list.start = found.start()

        if current_list.end is None or current_list.end < found.end():
            current_list.end = found.end()

        if current_list.start_number is None:
            current_list.start_number = found.group(1)

        current_list.elements.append(found.group(2))

    if len(lists) == 0:
        return text

    new_text = ""
    for i in range(len(lists)):
        current_list = lists[i]
        # Grab all the text from that isn't part of the list
        if i == 0:
            new_text = text[:current_list.start]
        else:
            new_text += text[lists[i-1].end:current_list.start]

        new_text += "</p>\n"
        new_text += "<ol>\n" if current_list.start_number == 1 else f"<ol start=\"{current_list.start_number}\">\n"
        for element in current_list.elements:
            new_text += "<li>" + element + "</li>\n"
        new_text += "</ol>\n<p>"

    # Grab the rest of the text
    new_text += text[current_list.end:]
    return new_text


def parse_markdown_to_html(text: str) -> str:
    new_text = ""
    for line in text.split("\n"):
        new_line = line
        new_line = parse_text_decoration(new_line, RE_ASTERISKS)
        new_line = parse_text_decoration(new_line, RE_UNDERLINED)
        new_line = parse_links(new_line)
        new_text += new_line + "\n"
    print(parse_numbered_list(new_text))


if __name__ == "__main__":
    test_string = """This should not match *This text should be italicized.*
**This text \*should be bolded**
***This text should be both***
*This text* ***should be a mix***
__Underlined__
1. Numbered
2. List
- Bullet
- List
2. New
3. list
[My nifty link](https://google.com)"""

    parse_markdown_to_html(test_string)
