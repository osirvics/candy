from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os
import random
import time
import subprocess
import logging
logger = logging.getLogger()
logging.basicConfig(handlers=[logging.FileHandler(filename="./mainlog.txt", 
                    encoding='utf-8', mode='a+'), logging.StreamHandler()],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)
cities = ["Athens", "Nicosia", "Dallas", "Kansas_City", "Manassas",	"Lisbon", "Saint_Louis", "Istanbul",
    "Buffalo",	"Milan", "Denver", "Los_Angeles", "Berlin", "Phoenix", "Frankfurt", "Seattle"]
try:
    server = random.choice(cities)
    subprocess.run(["nordvpn", "connect", server])
    time.sleep(30)
    result = subprocess.run(["nordvpn", "status"], stdout=subprocess.PIPE)
    logger.info(f"The connection status is: {result.stdout.decode()}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
    logger.exception(f"Failed to connect to Nordvpn")

#Load environment variables from .env file
load_dotenv()

#Get specific environment variables
u1 = os.environ['u1']
u2 = os.environ['u2']
u3 = os.environ['u3']
u4 = os.environ['u4']
u5 = os.environ['u5']
u6 = os.environ['u6']
u7 = os.environ['u7']
u8 = os.environ['u8']
u9 = os.environ['u9']
u10 = os.environ['u10']
p1 = os.environ['p1']
p2 = os.environ['p2']
p3 = os.environ['p3']
p4 = os.environ['p4']
p5 = os.environ['p5']
p6 = os.environ['p6']
p7 = os.environ['p7']
p8 = os.environ['p8']
p9 = os.environ['p9']
p10 = os.environ['p10']

usernames = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
passwords = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


failed_indices = []
retried_indices = []

browsers = ["chronium", "firefox", "webkit"]


def get_browser(p: Playwright):
    browser = random.choice(browsers)
    if browser == "chronium":
        return p.chromium.launch()
    elif browser == "firefox":
        return p.firefox.launch()
    else:
        return p.webkit.launch()


claimed = 0

def run(p: Playwright, username, password, index):
    logger.info(f"Attempting to claim for:{username}")
    global claimed
    global failed_indices
    print("Starting script")
    browser = get_browser(p)
    context = browser.new_context()
    page = context.new_page()

    try:
        logger.info("Opening homepage")
        page.goto("https://www.coingecko.com/")
        page.wait_for_timeout(6_000)
        logger.info("Succesfully opened homepage")
    except BaseException:
        failed_indices.append(index)
        logger.exception("Could not access https://www.coingecko.com/")
        context.close()
        browser.close()
        return
    try:
        logger.info("Commencing login action")
        page.locator("span").filter(has_text="Login").click()
        page.wait_for_timeout(5_000)
        page.locator("#signInEmail").click()
        page.wait_for_timeout(5_000)

        page.locator("#signInEmail").fill(username)
        page.wait_for_timeout(5_000)
        page.locator("#signInPassword").click()
        page.wait_for_timeout(6_000)
        page.locator("#signInPassword").fill(password)
        page.wait_for_timeout(5_000)

        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(6_000)
        div_element = page.query_selector(".unobtrusive-flash-message")
        text = div_element.evaluate("element => element.innerText")
        logger.info(text)
    except BaseException:
        failed_indices.append(index)
        logger.exception(f"Login failed for {username} at index {index}")
        context.close()
        browser.close()
        return      

    try:
        page.get_by_role("link", name="coingecko candy jar").click()
        page.wait_for_timeout(5_000)
        button = page.query_selector(".btn.btn-primary.col-12.collect-candy-button")
        if button:
            if "disabled" in button.get_attribute("class"):
                logger.info("Login Button is disabled")
            else:
                button.click()
                logger.info("Succesfully claimed candy for today")
                claimed += 1
                logger.info(f"Claimed for {claimed} account so far")
                page.wait_for_timeout(5_000)
        else:
            logger.info("Button not found")
    except BaseException:
        logger.exception("Failed to claim candy")

    context.close()
    browser.close()
    try:
        # Disconnect from the NordVPN server
        subprocess.run(["nordvpn", "disconnect"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        logger.exception("Failed to disconnect from Nordvpn server")

def main():
    with sync_playwright() as p:
        for i, username in enumerate(usernames):
            run(p, username, passwords[i], i)
        if len(failed_indices)>0:
            logger.info(f"The lenght is: {len(failed_indices)}")
            try:
                server = random.choice(cities)
                subprocess.run(["nordvpn", "connect", server])
                time.sleep(30)
                result = subprocess.run(["nordvpn", "status"], stdout=subprocess.PIPE)
                logger.info(f"The connection status is: {result.stdout.decode()}")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                logger.exception(f"Failed to connect to Nordvpn")   
            retry_claim(p)
        
def retry_claim(p):
    global retried_indices
    logger.info("********************retrying to claim*****************")
    for index in failed_indices:
        if index not in retried_indices:
            run(p, usernames[index], passwords[index], index)
            retried_indices.append(index)

if __name__ == '__main__':
    main()

