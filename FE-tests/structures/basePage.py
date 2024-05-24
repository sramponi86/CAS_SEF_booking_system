from playwright.async_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def is_title_contains(self, text):
        title = await self.page.title()
        if title.find(text) == -1:
            return False
        else:
            return True

    def is_url_contains(self, text):
        if self.page.url.find(text) == -1:
            return False
        else:
            return True