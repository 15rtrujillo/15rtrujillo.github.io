from datetime import datetime


import markdown_to_html as parser


class BlogPost:
    def __init__(self, title: str, date: datetime, post_text: str):
        self.title: str = title
        self.date: datetime = date
        self.post: str = post_text
        self._html_post: str | None = None

    def get_html_title(self, heading_tag: str="h2") -> str:
        """Format the post title with the proper HTML"""
        return f"<{heading_tag} id=\"{self.get_iso_post_date()}\">{self.title}</{heading_tag}>"

    def get_expanded_post_date(self) -> str:
        """Retrive the post's date in the Month d, YYYY format"""
        return self.date.strftime("%B %d, %Y").replace(" 0", " ")
    
    def get_iso_post_date(self) -> str:
        """Retrieve the post's date in the YYYY/mm/dd format"""
        return self.date.strftime("%Y/%m/%d")

    def get_iso_post_date_no_day(self) -> str:
        """Retrieve the post's date in the YYYY-mm format"""
        return self.date.strftime("%Y-%m")
    
    def get_post_year(self) -> int:
        """Get the post's year as an int"""
        return self.date.year
    
    def get_post_month(self) -> int:
        """Get the post's month as an int"""
        return self.date.month

    def get_html_date(self) -> str:
        """Retrive the post's date with the proper HTML tags"""
        return f"<h4>{self.get_expanded_post_date()}</h4>"
    
    def get_html_post(self) -> str:
        if self._html_post is not None:
            return self._html_post
        
        self._html_post = parser.parse_markdown_to_html(self.post)

        return self._html_post
    
    def __str__(self) -> str:
        return f"""{self.title}
{self.get_expanded_post_date()}
{self.post}"""
