from fastapi import FastAPI, HTTPException
import logging
from requests.exceptions import HTTPError
import backoff
from ratelimit import limits, sleep_and_retry
from functools import wraps
import time

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define rate limit constants
ONE_MINUTE = 60  # seconds
MAX_CALLS_PER_MINUTE = 30

# Initialize request counter
request_counter = 0

def count_requests(func):
    """Decorator to count the number of requests."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global request_counter
        request_counter += 1
        logger.info(f"Number of requests made: {request_counter}")
        return func(*args, **kwargs)
    return wrapper

# Rate limit decorator
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def rate_limited_request(func, *args, **kwargs):
    return func(*args, **kwargs)

# Exponential backoff decorator
@backoff.on_exception(
    backoff.expo, HTTPError,
    max_tries=5, factor=5, logger=logger,
    jitter=None, backoff_log_level=logging.WARNING
)
@count_requests  # Count the number of requests
def _get_document_list(target_date: str):
    """Get document list on specific day"""
    # Simulating an API call with a dummy response
    logger.info(f"Fetching document list for {target_date}")
    return {"documents": ["doc1", "doc2", "doc3"]}

# FastAPI route
@app.get("/documents/{target_date}")
def get_document_list(target_date: str):
    try:
        return rate_limited_request(_get_document_list, target_date)
    except HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test function to simulate multiple requests
def test_rate_limiter():
    import requests

    target_date = "2023-05-30"
    url = f"http://127.0.0.1:8000/documents/{target_date}"

    for _ in range(35):  # Attempt to make 35 requests
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info(f"Documents: {response.json()}")
            else:
                logger.error(f"Failed request with status code: {response.status_code}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    # Run FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Uncomment the following line to run the test
    # test_rate_limiter()