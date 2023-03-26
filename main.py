from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

#Load environment variables from .env file
load_dotenv()

usernames = [os.environ[f"u{i}"] for i in range(1, 11)]
passwords = [os.environ[f"p{i}"] for i in range(1, 11)]

failed_indices = []
retried_indices = []
claimed = 0

def run(p: Playwright, username, password, index):
    logger.info(f"Attempting to claim for:{username}")
    global claimed
    global failed_indices
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        logger.info("Opening homepage")
        page.goto("https://www.coingecko.com/")
        page.wait_for_timeout(1_000)
        logger.info("Succesfully opened homepage")
    except BaseException:
        failed_indices.append(index)
        logger.exception(f"Could not access https://www.coingecko.com for {username}")
        context.close()
        browser.close()
        return

    try:
        logger.info("Commencing login action")
        page.locator("span").filter(has_text="Login").nth(2).click()
        page.wait_for_timeout(1_000)
        page.locator("#signInEmail").click()
        page.wait_for_timeout(1_000)

        page.locator("#signInEmail").fill(username)
        page.wait_for_timeout(1_000)
        page.locator("#signInPassword").click()
        page.wait_for_timeout(1_000)
        page.locator("#signInPassword").fill(password)
        page.wait_for_timeout(1_000)

        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(1_000)
        logger.info("Login succesful")
    except BaseException:
        failed_indices.append(index)
        logger.exception(f"Login failed for {username}")
        context.close()
        browser.close()
        return      
    try:
        page.get_by_role("link", name="coingecko candy jar").click()
        page.wait_for_timeout(2_000)
        button = page.query_selector(".btn.btn-primary.col-12.collect-candy-button")
        if button:
            if "disabled" in button.get_attribute("class"):
                logger.info("Login Button is disabled")
            else:
                button.click()
                logger.info("Succesfully claimed candy for today")
                claimed += 1
                logger.info(f"Claimed for {claimed} account so far")
                page.wait_for_timeout(1_000)
        else:
            logger.info("Already claimed for today")
    except BaseException:
        logger.exception("Failed to claim candy")

    context.close()
    browser.close()

def main():
    with sync_playwright() as p:
        for i, username in enumerate(usernames):
            run(p, username, passwords[i], i)
        if len(failed_indices)>0:
            logger.info(f"The lenght is: {len(failed_indices)}")   
            retry_claim(p)
        
def retry_claim(p):
    global retried_indices
    logger.info("************** retrying candy claim **************")
    for index in failed_indices:
        if index not in retried_indices:
            run(p, usernames[index], passwords[index], index)
            retried_indices.append(index)

if __name__ == '__main__':
    main()