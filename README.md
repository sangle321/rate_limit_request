# FastAPI Rate Limited Application

This FastAPI application demonstrates how to implement rate limiting and exponential backoff for API endpoints. The application includes two endpoints with shared rate limiting logic and request counting, which resets every minute.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Requests
- Ratlimit
- Backoff

## Installation

1. Clone the repository or download the source code.
2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirement.txt
    ```

## Running the Application
- Run the script with the following command:
   ```bash
    uvicorn main:app --reload
    ```

    
## Test limit request api
- Run the script:
    ```bash
    python test_request.py
    ```