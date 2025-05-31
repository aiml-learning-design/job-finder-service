from playwright.async_api import async_playwright
import asyncio
import random


async def fetch_jobs_indeed(domain, skills, experience, country, city):
    query = f"{domain} {' '.join(skills)} {experience} years".replace(' ', '+')
    location_param = f"{city}, {country}".replace(' ', '+')
    search_url = f"https://ae.indeed.com/jobs?q={query}&l={location_param}"

    # Random user agent from common browsers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]

    async with async_playwright() as p:
        # Launch with stealth settings
        browser = await p.chromium.launch(
            headless=False,  # Must be False to solve CAPTCHAs
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        try:
            context = await browser.new_context(
                user_agent=random.choice(user_agents),
                viewport={"width": 1366, "height": 768},
                locale="en-US",
                timezone_id="America/New_York",
                # Reduce automation detection
                bypass_csp=False,
                java_script_enabled=True,
                # Disable WebDriver flag
                ignore_https_errors=False
            )

            # Remove navigator.webdriver flag
            await context.add_init_script("""
                delete Object.getPrototypeOf(navigator).webdriver;
                window.navigator.chrome = {
                    runtime: {},
                };
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            """)

            page = await context.new_page()

            # Random delays to appear human
            await asyncio.sleep(random.uniform(1, 3))

            # Navigate with realistic patterns
            await page.goto(search_url, timeout=60000, wait_until="domcontentloaded")

            # Check for CAPTCHA
            if await page.query_selector("text='Verify you are human'"):
                print("CAPTCHA detected - please solve manually in browser window")
                # Wait for manual solving with 5 minute timeout
                await page.wait_for_selector("text='Verify you are human'", state="hidden", timeout=300000)
                print("CAPTCHA solved, continuing...")

            # Additional human-like behavior
            await asyncio.sleep(random.uniform(2, 5))
            await page.mouse.move(100, 100)
            await page.mouse.wheel(0, 500)

            # Wait for job listings
            try:
                await page.wait_for_selector("div.job_seen_beacon, div.jobsearch-SerpJobCard", timeout=15000)
            except:
                print("No job cards found - may need to adjust selectors")
                return []

            # Extract job data
            job_cards = await page.query_selector_all("div.job_seen_beacon, div.jobsearch-SerpJobCard")
            results = []

            for job in job_cards[:5]:
                try:
                    title = await job.evaluate("""
                        el => el.querySelector('h2.jobTitle')?.innerText?.trim() || 
                              el.querySelector('h3.jobTitle')?.innerText?.trim() || 'N/A'
                    """)

                    company = await job.evaluate("""
                        el => el.querySelector('span.companyName')?.innerText?.trim() || 
                              el.querySelector('div.companyInfo')?.innerText?.trim() || 'N/A'
                    """)

                    location = await job.evaluate("""
                        el => el.querySelector('div.companyLocation')?.innerText?.trim() || 
                              el.querySelector('span.location')?.innerText?.trim() || 'N/A'
                    """)

                    if title != 'N/A':
                        results.append({
                            "title": title,
                            "company": company,
                            "location": location
                        })
                except:
                    continue

            return results if results else []

        except Exception as ex:
            print(f"Error: {str(ex)}")
            return []
        finally:
            await browser.close()
