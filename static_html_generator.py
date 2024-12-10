import datetime
import os
import shutil


with open("template.html", "r") as template_file:
    BLOG_HTML_TEMPLATE = template_file.read()
BLOGPOST_DIRECTORY = os.path.join(os.getcwd(), "blogposts")


class BlogPost:
    def __init__(self, title: str, date: datetime.datetime, post_text: str):
        self._title: str = title
        self._date: datetime.datetime = date
        self._post: str = post_text
        self._html_post: str | None = None

    def get_html_title(self) -> str:
        """Format the post title with the proper HTML"""
        return f"<h2>{self._title}</h2>"

    def get_expanded_post_date(self) -> str:
        """Retrive the post's date in the Month d, YYYY format"""
        return self._date.strftime("%B %d, %Y").replace(" 0", " ")
    
    def get_post_month_name(self) -> str:
        """Retrive the post's month"""
        return self._date.strftime("%B")
    
    def get_iso_post_date_no_day(self) -> str:
        """Retrieve the post's date in the YYYY-mm format"""
        return self._date.strftime("%Y-%m")
    
    def get_post_year(self) -> int:
        """Get the post's year as an int"""
        return self._date.year
    
    def get_post_month(self) -> int:
        """Get the post's month as an int"""
        return self._date.month

    def get_html_date(self) -> str:
        """Retrive the post's date with the proper HTML tags"""
        return f"<h4>{self.get_expanded_post_date()}</h4>"
    
    def get_html_post(self) -> str:
        if self._html_post is not None:
            return self._html_post
        
        # Replace * with <em></em> tags
        new_post = self._replace_symbol_with_tag(self._post, "*", "em")

        # Create <p></p> tags
        final_post = "<p>"
        final_post += new_post.replace("\n\n", "</p>\n<p>")
        final_post += "</p>"

        self._html_post = final_post

        return self._html_post
    
    @staticmethod
    def _replace_symbol_with_tag(post: str, symbol: str, tag: str) -> str:
        post_list: list[str] = []
        start_index = 0
        end_index = post.find(symbol)
        first = True
        while end_index != -1:
            # If the symbol is preceeded with a \, we want to ignore the symbol.
            # We also don't want to consume the \.
            if post[end_index-1] == "\\":
                post_list.append(post[start_index:end_index-1])
                post_list.append(post[end_index:end_index+len(symbol)])
                start_index = end_index + len(symbol)
                end_index = post.find(symbol, start_index)
                continue

            # Add everything up to the symbol
            post_list.append(post[start_index:end_index])

            # If this is the "opening" occurence of the symbol, do an open tag
            if first:
                post_list.append(f"<{tag}>")
            else:
                post_list.append(f"</{tag}>")
            
            # Reset
            first = not first
            start_index = end_index + len(symbol)
            end_index = post.find(symbol, start_index)

        if not first:
            print(f"Error! Unclosed {symbol} in post starting with {post_list[0]}")

        post_list.append(post[start_index:])
        return "".join(post_list)

    def __str__(self) -> str:
        return f"""{self._title}
{self.get_expanded_post_date()}
{self._post}"""


def get_blogpost_files() -> list[str]:
    """
    Get a list of the names of all the files in a directory (including extensions)
    """
    files = [os.path.join(BLOGPOST_DIRECTORY, f) for f in os.listdir(BLOGPOST_DIRECTORY) if os.path.isfile(os.path.join(directory, f))]
    return files


def read_blogpost(file_name: str) -> BlogPost:
    """Read a text file and create a BlogPost object"""
    file = open(file_name, "r")

    # Get the first line as the title and remove the \n
    title = file.readline().rstrip()

    # Try to grab the date formatted as YYYY/mm/dd
    try:
        date = datetime.datetime.strptime(file.readline().rstrip(), "%Y/%m/%d")
    except ValueError:
        print(f"Error converting datetime in blogpost {file_name}. Terminating.")
        file.close()
        exit()

    # Grab the rest of the post with no processing
    post_text = "".join(file.readlines())
    file.close()

    return BlogPost(title, date, post_text)


def sort_posts(posts: list[BlogPost]) -> dict[int, dict[str, list[BlogPost]]]:
    sorted_posts: dict[int, dict[str, list[BlogPost]]] = {}

    current_year: int = -1
    current_month: int = -1
    current_month_name: str = ""
    for post in posts:
        if current_year == -1 or current_year != post.get_post_year():
            current_year = post.get_post_year()
            sorted_posts[current_year] = {}
        
        if current_month == -1 or current_month != post.get_post_month():
            current_month = post.get_post_month()
            current_month_name = post.get_post_month_name()
            sorted_posts[current_year][current_month_name] = []

        sorted_posts[current_year][current_month_name].append(post)

    return sorted_posts


def generate_archive(sorted_posts: dict[int, dict[str, list[BlogPost]]]) -> str:
    archive_html = ""
    for year in sorted_posts:
        archive_html += f"<li><details><summary>{year}</summary>\n<ul>\n"
        for month in sorted_posts[year]:
            # The page's name should be YYYY-mm
            page_name = f"{sorted_posts[year][month][0].get_iso_post_date_no_day()}.html"

            # Unless this is the page for this month/year, then it should be index.html.
            if year == datetime.datetime.now().year and month == datetime.datetime.now().strftime("%B"):
                page_name = "index.html"

            archive_html += f"<li><a href=\"{page_name}\">{month}</a></li>\n"

        archive_html += f"</ul>\n</details></li>\n"

    return archive_html


def generate_month_page(posts: list[BlogPost], archive: str) -> str:
    page_html = BLOG_HTML_TEMPLATE
    page_html = page_html.replace("<!--@ARCHIVE HERE@-->", archive)

    full_post = f"""{post.get_html_title()}
{post.get_html_date()}
{post.get_html_post()}"""

    page_html = page_html.replace("<!--@POST HERE@-->", full_post)

    return page_html

def main():
    print("Reading post files...")
    posts: list[BlogPost] = []
    file_names = get_blogpost_files(BLOGPOST_DIRECTORY)
    for file_name in file_names:
        post = read_blogpost(file_name)
        posts.append(post)
    posts.reverse()

    print("Sorting posts by year and month...")
    sorted_posts = sort_posts(posts)
    # print("Recreating blogposts/html directory...")
    # recreate_html_directory()

    print("Generating archive list for month pages...")
    archive = generate_archive(sorted_posts)

    print("Creating monthly blogpost pages...")
    for post in posts:
        html = generate_month_page(posts, archive)
        with open(os.path.join(HTML_DIRECTORY, post.get_iso_post_date() + ".html"), "w") as file:
            file.write(html)

    input("Press ENTER to exit...")


if __name__ == "__main__":
    main()
