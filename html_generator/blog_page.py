from blog_post import BlogPost
from calendar import month_name as month_names


class BlogPage:
    def __init__(self, year: int, month: int, file_name: str):
        self.posts: list[BlogPost] = []
        self.year: int = year
        self.month: int = month
        self.month_name: str = month_names[self.month]
        self.file_name: str = file_name
