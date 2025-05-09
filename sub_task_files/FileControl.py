from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import csv
from robocorp import log
import os
from RPA.Archive import Archive
import shutil

def generate_pdf():
    """get receipt details"""
    os.makedirs("output/receipts", exist_ok=True)
    page = browser.page()
    order_number = page.locator("p.badge.badge-success").inner_text().strip()
    pdf_filename = os.path.join("output/receipts/", f"{order_number}.pdf")
    screenshot_path = f"output/receipts/{order_number}_preview.png"


    screenshot(screenshot_path)
    
    receipt_to_pdf(order_number)

    embed_screenshot_to_receipt(screenshot_path,pdf_filename)

    try:
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            print(f"Deleted screenshot: {screenshot_path}")
    except Exception as e:
        print(f"Could not delete screenshot {screenshot_path}: {e}")


def screenshot(screenshot_folder):
    """takes screenshot of robot"""
    page = browser.page()
    robot_preview = page.locator("#robot-preview-image")
    robot_preview.screenshot(path=screenshot_folder)

def receipt_to_pdf(order_number):
    """saves receipt to pdf"""
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf_filename = os.path.join("output/receipts/", f"{order_number}.pdf")

    pdf = PDF()
    pdf.html_to_pdf(receipt_html, pdf_filename)

def embed_screenshot_to_receipt(screenshot_path, pdf_path):
    """appends pdf with screenshot"""
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(
        image_path=screenshot_path, 
        source_path=pdf_path, 
        output_path=pdf_path
        )



def download_orders_csv():
    """downloads orders csv file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def get_orders():
    """Reads csv file contents to table and returns value"""
    data = []
    with open('orders.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
    


def archive_receipts():
    """Zip receipts"""
    receipts_folder = "output/receipts"
    zip_path = "output/receipts.zip"

    os.makedirs("output/receipts", exist_ok=True)
    lib = Archive()
    lib.archive_folder_with_zip("output/receipts/", "output/receipts.zip", recursive=True)
    files = lib.list_archive(zip_path)
    for file in files:
        print(file)

    if os.path.exists(receipts_folder):
        shutil.rmtree(receipts_folder)
        print(f"Deleted folder: {receipts_folder}")