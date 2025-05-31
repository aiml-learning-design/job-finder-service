from src.scrapers.indeed_scraper import fetch_jobs_indeed
from src.model.JobQuery import JobQuery


async def handle_job_query(query: JobQuery):
    print(f"Agent received Query: {query}")
    jobs = await fetch_jobs_indeed(
        domain=query.domain,
        skills=query.skills,
        experience=query.experience,
        country=query.country,
        city=query.city
    )
    return jobs
