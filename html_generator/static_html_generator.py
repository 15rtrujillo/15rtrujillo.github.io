from blog_page import BlogPage
from blog_post import BlogPost


import datetime
import os


with open(os.path.join(os.getcwd(), "template.html"), "r") as template_file:
    BLOG_HTML_TEMPLATE = template_file.read()
BLOGPOST_DIRECTORY = os.path.join(os.getcwd(), "blogposts")


def get_blogpost_files() -> list[str]:
    """
    Get a list of the names of all the files in a directory (including extensions)
    """
    files = [os.path.join(BLOGPOST_DIRECTORY, f) for f in os.listdir(BLOGPOST_DIRECTORY) if os.path.isfile(os.path.join(BLOGPOST_DIRECTORY, f))]
    files.sort()
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


def sort_posts(posts: list[BlogPost]) -> dict[int, dict[int, BlogPage]]:
    sorted_posts: dict[int, dict[int, BlogPage]] = {}

    current_year: int = -1
    current_month: int = -1
    for post in posts:
        if current_year == -1 or current_year != post.get_post_year():
            current_year = post.get_post_year()
            sorted_posts[current_year] = {}
        
        if current_month == -1 or current_month != post.get_post_month():
            current_month = post.get_post_month()

            page = BlogPage()
            page.year = current_year
            page.month = current_month
            page.month_name = post.get_post_month_name()

            now = datetime.datetime.now()
            page.file_name = "index.html" if current_year == now.year and current_month == now.month else f"{post.get_iso_post_date_no_day()}.html"

            sorted_posts[current_year][current_month] = page

        sorted_posts[current_year][current_month].posts.append(post)

    return sorted_posts


def generate_archive(sorted_posts: dict[int, dict[int, BlogPage]]) -> str:
    archive_html = ""
    for year in sorted_posts:
        archive_html += f"<li><details><summary>{year}</summary>\n<ul>\n"
        for page in sorted_posts[year].values():
            archive_html += f"<li><a href=\"{page.file_name}\">{page.month_name}</a></li>\n"

        archive_html += f"</ul>\n</details></li>\n"

    return archive_html


def generate_month_page(page: BlogPage, archive: str) -> str:
    page_html = BLOG_HTML_TEMPLATE
    page_html = page_html.replace("<!--@ARCHIVE HERE@-->", archive)

    all_posts = ""
    for i in range(len(page.posts)):
        post = page.posts[i]
        all_posts += f"""{post.get_html_title()}
{post.get_html_date()}
{post.get_html_post()}"""
        if i < len(page.posts)-1:
            all_posts += "\n<p><a href=\"#top\">Back to the top</a></p><hr />\n"

    page_html = page_html.replace("<!--@POST HERE@-->", all_posts)

    return page_html

def main():
    print("Reading post files...")
    posts: list[BlogPost] = []
    file_names = get_blogpost_files()
    for file_name in file_names:
        post = read_blogpost(file_name)
        posts.append(post)
    posts.reverse()

    print("Sorting posts by year and month...")
    sorted_posts = sort_posts(posts)
    # print("Recreating blogposts/html directory...")
    # recreate_html_directory()

    print("Generating archive list...")
    archive = generate_archive(sorted_posts)
    
    print("Creating monthly blogpost pages...")
    for year in sorted_posts:
        for page in sorted_posts[year].values():
            html = generate_month_page(page, archive)
            with open(page.file_name, "w") as file:
                file.write(html)


if __name__ == "__main__":
    main()
