from playwright.sync_api import sync_playwright

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 👈 headless = True = no browser window
      #  browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://realpython.github.io/fake-jobs/")

        # Get all job titles
        job_elements = page.query_selector_all("div.card-content h2.title")
        print("Job Titles:\n")
        for job in job_elements:
            print("-", job.inner_text())

        browser.close()

if __name__ == "__main__":
    scrape_jobs()