import datetime


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
