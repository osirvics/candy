from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os



#Load environment variables from .env file
load_dotenv()

#Get specific environment variables
u1 = os.environ['u1']
u2 = os.environ['u2']
u3 = os.environ['u3']
u4 = os.environ['u4']
u5 = os.environ['u5']
p1 = os.environ['p1']
p2 = os.environ['p2']
p3 = os.environ['p3']
p4 = os.environ['p4']
p5 = os.environ['p5']

usernames = [u1, u2, u3, u4, u5]
passwords = [p1, p2, p3, p4, p5]

claimed = 0

def run(p: Playwright, username, password):
    global claimed
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://www.coingecko.com/", timeout=0)
        page.wait_for_timeout(6_000)
    except BaseException:
        print("Could not access https://www.coingecko.com/")
        exit(1001)
    try:
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
        page.wait_for_timeout(10_000)
    except BaseException:
        print('Cannot login')
        exit(1002)
    try:
        page.get_by_role("link", name="coingecko candy jar").click()
        page.wait_for_timeout(5_000)
        #page.query_selector("button[data-action='click->points#claimCandy'][data-target='points.button']").click()
        button = page.query_selector(".btn.btn-primary.col-12.collect-candy-button")
        if button:
            if "disabled" in button.get_attribute("class"):
                print("Button is disabled")
            else:
                # button exist, proceed with clicking the button
                print("This will mined coins working")
                button.click()
                print("Succesfully claimed for today")
                claimed += 1
                print("Claimed: ", claimed)
                page.wait_for_timeout(5_000)
        else:
            # button not found
            print("Button not found")
    except Exception as e:
        print(e)
        print("Cannot access daily reward")
        exit(1003)

    context.close()
    browser.close()


def main():
    with sync_playwright() as p:
        for i, username in enumerate(usernames):
            run(p, username, passwords[i])

if __name__ == '__main__':
    main()