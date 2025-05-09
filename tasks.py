from robocorp.tasks import task
from robocorp import browser
from sub_task_files.websiteActions import open_the_intranet_website, close_modal, press_order, press_order_another
from sub_task_files.FileControl import generate_pdf, download_orders_csv, get_orders, archive_receipts

@task


def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )

    """Open and login to intranet website and navigate to the order page"""
    open_the_intranet_website()

    """Download csv sourcefile containing orders,
       fill and submit the orders,
       generate pdf receipt of each order,
       pdf contains receipt and preview image of the robot"""
    submit_orders()

    """Compress receipts to zip file and remove the receipts folder that was not zipped"""
    archive_receipts()

def submit_orders():
    """submit orders"""
    download_orders_csv()
    orders = get_orders()
    
    for a in orders:
        fill_order_form(a)
        make_order()


def fill_order_form(details):
    """fills order form with details"""
    page = browser.page()
    page.select_option("#head", str(details["Head"]))
    body = "#id-body-" + str(details["Body"])
    page.check(body)
    page.fill("text=3. Legs:", str(details["Legs"]))
    page.fill("#address", str(details["Address"]))
    
def preview_robot():
    page = browser.page()
    page.click("button:text('Preview')")

def make_order():
    """completes order"""
    press_order()
    generate_pdf()
    press_order_another()
    close_modal()

    

