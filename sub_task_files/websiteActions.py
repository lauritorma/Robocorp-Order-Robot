from robocorp import browser
from RPA.Robocorp.Vault import Vault
from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import csv
from robocorp import log
import os
from RPA.Archive import Archive
import shutil

_secret = Vault().get_secret("Credentials")

USER_NAME = _secret["Username"]
PASSWORD = _secret["Password"]

def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")
    log_in()
    navigate_to_order_page()

def log_in():
    """"Logs in to the page"""
    page = browser.page()
    page.fill("#username", USER_NAME)
    page.fill("#password", PASSWORD)
    page.click("button:text('Log in')")

def navigate_to_order_page():
    """Navigates to correct page"""
    page = browser.page()
    page.click("a:text('Order your robot!')")
    close_modal()

def close_modal():
    """Clicks ok on popup that triggers when navigating to order page"""
    page = browser.page()
    page.click("button:text('OK')")

def press_order():
    """presses order button"""
    page = browser.page()
    max_retries = 10
    attempt = 0

    while attempt < max_retries:
        try:
            print(f"Attempt {attempt + 1}: Clicking ORDER button...")
            page.click("button:text('ORDER')")

            page.wait_for_timeout(1000)
            if page.locator('div.alert.alert-danger').is_visible(timeout=5000):
                popup_text = page.locator('div.alert.alert-danger').inner_text()
                print(f"Error popup still visible: {popup_text}")
                attempt += 1
            else:
                print("Popup is gone. Proceeding.")
                break  # Exit the loop if the popup is no longer visible

        except TimeoutError:
            print("Timeout checking for alert — assuming it's gone.")
            break

        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            break

    else:
        print("Reached maximum number of retries. Popup did not disappear.")

def press_order_another():
    """presses order another robot button"""
    page = browser.page()
    try:
        page.click("button:text('ORDER ANOTHER ROBOT')")
    except Exception as e:
        print(f"Failed to press 'ORDER ANOTHER ROBOT': {e}")

