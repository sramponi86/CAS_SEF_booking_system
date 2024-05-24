from playwright.async_api import Page, expect
from structures.basePage import BasePage

class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def navigate(self):
        await self.page.goto("http://127.0.0.1:5000/admin", timeout=5000)

    async def check_user_management_header_visible(self):
        await expect(self.page.get_by_role("heading", name="User Management")).to_be_visible()