import uvicorn
from fastapi import FastAPI

from src.agent_engine import handle_job_query
from src.model.JobQuery import JobQuery

api = FastAPI()


@api.post("/find/jobs")
async def get_jobs(query: JobQuery):
    try:
        result = await handle_job_query(query)
        return {"Job Details": result}
    except Exception as ex:
        print(f"Failed to find job {ex}")


@api.get("/")
async def health():
    return {f"Message": "Job find App is running!"}


if __name__ == "__main__":
    uvicorn.run("api.main:api", host="127.0.0.1", port=6500, reload=True)