from blog_page import BlogPage
from blog_post import BlogPost
from copy import copy


class Blog:
    def __init__(self):
        # dict[year, dict[month, BlogPage]]
        self.pages: dict[int, dict[int, BlogPage]] = {}

    def add_blog_post(self, post: BlogPost):
        year = post.get_post_year()
        month = post.get_post_month()

        if not year in self.pages.keys():
            self.pages[year] = {}

        if not month in self.pages[year].keys():
            page = BlogPage(year, month, post.get_iso_post_date_no_day() + ".html")
            self.pages[year][month] = page

        self.pages[year][month].posts.append(post)

    def get_pages_in_year(self, year: int) -> list[BlogPage]:
        return [page for page in self.pages[year].values()]

    def get_index_page(self) -> BlogPage:
        max_year = max(self.pages.keys())
        max_month = max(self.pages[max_year].keys())

        index = copy(self.pages[max_year][max_month])
        index.file_name = "index.html"
        
        return index
