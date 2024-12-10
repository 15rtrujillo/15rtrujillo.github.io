from blog_post import BlogPost


class BlogPage:
    def __init__(self):
        self.posts: list[BlogPost] = []
        self.year: int = -1
        self.month: int = -1
        self.month_name: str = ""
        self.file_name: str = ""
