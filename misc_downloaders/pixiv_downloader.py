import pixivpy3

try:
    import dotenv
    dotenv.load_dotenv()
    has_dotenv = True
except ImportError:
    has_dotenv = False


class PixivDownloader(pixivpy3.AppPixivAPI):
    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_info = self.login(username, password)["response"]

    def get_user_gallery(self, *args, **kwargs):
        gallery = self.user_illusts(*args, **kwargs)
        work_list = list()

        work_list += gallery["illusts"]

        next_results = self.parse_qs(gallery["next_url"])
        if next_results:
            results = self.get_user_gallery(**next_results)
            return work_list + results
        else:
            return work_list

    @property
    def username(self):
        return self.user_info["user"]["account"]
