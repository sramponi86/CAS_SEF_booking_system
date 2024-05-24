from playwright.async_api import Page, expect
from structures.basePage import BasePage

class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def navigate(self):
        await self.page.goto("http://127.0.0.1:5000", timeout=5000)

    async def click_admin_button(self):
        await self.page.get_by_role("link", name="Open Admin Panel").click()

    async def click_user_button(self):
        await self.page.locator("").click()

    async def check_user_button_visible(self):
        await expect(self.page.locator("")).to_be_visible()

    async def check_admin_button_visible(self):
        await expect(self.page.get_by_role("link", name="Open Admin Panel")).to_be_visible()