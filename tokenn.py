from playwright.sync_api import sync_playwright

username = "victor46539@gmail.com"
password = "Aa25da90@"
password2 = "aa25da90"

def main():
    with sync_playwright() as p:
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
            page.wait_for_timeout(5_000)
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
            page.locator('.collect-candy-button').click()
            page.query_selector("button[data-action='click->points#claimCandy'][data-target='points.button']").click()
            print("Succesfully claimed for today")
            page.wait_for_timeout(10_000)
        except Exception as e:
            print(e)
            print("Cannot access daily reward")
            exit(1003)

        context.close()
        browser.close()

if __name__ == '__main__':
    main()