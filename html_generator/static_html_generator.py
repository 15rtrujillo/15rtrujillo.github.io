from blog import Blog
from blog_page import BlogPage
from blog_post import BlogPost
from datetime import datetime
from shutil import rmtree


import os


with open(os.path.join(os.getcwd(), "template.html"), "r") as template_file:
    BLOG_HTML_TEMPLATE = template_file.read()
BLOGPOST_DIRECTORY = os.path.join(os.getcwd(), "blogposts")
HTML_DIRECTORY = os.path.join(BLOGPOST_DIRECTORY, "html")
INDEX_HTML = """<!DOCTYPE html>
<head>
    <title>Ryan's Website</title>
    <meta http-equiv="refresh" content="0; url=@NEWEST@" />
</head>
"""


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
        date = datetime.strptime(file.readline().rstrip(), "%Y/%m/%d")
    except ValueError:
        print(f"Error converting datetime in blogpost {file_name}. Terminating.")
        file.close()
        exit()

    # Grab the rest of the post with no processing
    post_text = "".join(file.readlines())
    file.close()

    return BlogPost(title, date, post_text)


def recreate_html_directory():
    if os.path.exists(HTML_DIRECTORY):
        rmtree(HTML_DIRECTORY)
    os.mkdir(HTML_DIRECTORY)


def generate_archive(blog: Blog) -> str:
    archive_html = ""
    for year in blog.pages:
        archive_html += f"<li><details><summary>{year}</summary>\n<ul>\n"
        for page in blog.get_pages_in_year(year):
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
        if i > 0:
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
    blog = Blog()
    for post in posts:
        blog.add_blog_post(post)

    print("Recreating blogposts/html directory...")
    recreate_html_directory()

    print("Generating archive list...")
    archive = generate_archive(blog)
    
    print("Creating monthly blogpost pages...")
    for year in blog.pages:
        for page in blog.get_pages_in_year(year):
            html = generate_month_page(page, archive)
            with open(os.path.join(HTML_DIRECTORY, page.file_name), "w") as file:
                file.write(html)

    print("Creating index page...")
    newest_page = blog.get_newest_page()
    html = INDEX_HTML.replace("@NEWEST@", f"blogposts/html/{newest_page.file_name}")
    with open("index.html", "w") as file:
        file.write(html)

    print("\nDone!")


if __name__ == "__main__":
    main()
