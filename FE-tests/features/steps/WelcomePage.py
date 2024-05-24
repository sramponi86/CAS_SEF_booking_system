from playwright.async_api import Page, expect, async_playwright
from behave import *
from structures.welcomePage import WelcomePage
from structures.adminPage import AdminPage
from behave.api.async_step import async_run_until_complete

use_step_matcher("cfparse")

@given('i navigate to the Welcome page')
@async_run_until_complete
async def admin_welcome_navigation(context):
    welcome_page = WelcomePage(context.page)
    await welcome_page.navigate()
    #pass

@then('admin button should be visible')
@async_run_until_complete
async def admin_button_check(context):
    welcome_page = WelcomePage(context.page)
    await welcome_page.check_admin_button_visible()
    #pass

@when('i click to admin button')
@async_run_until_complete
async def admin_button_click(context):
    welcome_page = WelcomePage(context.page)
    await welcome_page.click_admin_button()
    #pass

@then('user management section is visible')
@async_run_until_complete
async def admin_button_check(context):
    admin_page = AdminPage(context.page)
    await admin_page.check_user_management_header_visible()
    #pass