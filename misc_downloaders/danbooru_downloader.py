from pybooru import Danbooru
from datetime import datetime
from pathlib import Path


class DanbooruDownloader(Danbooru):
    def __init__(self, tags='', *args, **kwargs):
        self.tags = tags
        return super().__init__(site_name='danbooru', *args, **kwargs)

    def get_post_list(self, pages):
        post_list = list()

        for page in pages:
            page_post_list = self.post_list(tags=self.tags,
                                            limit=100,
                                            page=page)
            post_list += page_post_list

        if not post_list:
            print("Post list oopsie")

        return post_list

    @property
    def page_count(self):
        return (self.post_count // 100) + 1

    @property
    def tag_path(self):
        date = datetime.now()
        return Path("{}{}{}{}".format(date.year, date.month, date.day,
                                      self.tags.replace(":", "_")))

    @property
    def post_count(self):
        return int(
            self.client.get(
                "https://danbooru.donmai.us/counts/posts.json?tags={}".format(
                    "%3A".join(self.tags.split(":")))).text.split(
                        '{"counts": {"posts": ')[1].split("}}")[0])
