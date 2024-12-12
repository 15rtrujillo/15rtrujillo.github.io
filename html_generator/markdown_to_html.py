import re


# Text decorations
ASTERISKS = r"\*+(?<!\\)(.+?)(?<!\\)\*+"
RE_ASTERISKS = re.compile(ASTERISKS)
UNDERLINED = r"(?<!\\)__([^\\]+?(?:\\.[^\\]*?)*?)__"
RE_UNDERLINED = re.compile(UNDERLINED)

# Lists
ORDERED_LIST = r"^[0-9]+\.\s(.+)$"
RE_ORDERED_LIST = re.compile(ORDERED_LIST)
UNORDERED_LIST = r"^-\s(.+)$"
RE_UNORDERED_LIST = re.compile(UNORDERED_LIST)

# Misc
LINKS = r"\[(.+?)\]\((.+?)\)"
RE_LINKS = re.compile(LINKS)


def parse_text_decoration(line: str, pattern: re.Pattern[str]) -> str:
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

        new_line = new_line.replace(found.group(0), html)
    
    return new_line


def parse_markdown_to_html(text: str) -> str:
    for line in text.split("\n"):
        print(parse_text_decoration(line, RE_ASTERISKS))


if __name__ == "__main__":
    test_string = """This should not match *This text should be italicized.*
**This text should be bolded**
***This text should be both***
*This text* ***should be a mix***
[My nifty link](https://google.com)"""

    parse_markdown_to_html(test_string)
