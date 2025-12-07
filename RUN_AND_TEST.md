# How to Run and Test the Application

## 1. Set up the Environment

- Make sure you have Python 3.10 or higher installed.
- Create a virtual environment:
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment:
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```
  - On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```
- Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Set up the Database

- Make sure you have a PostgreSQL server running.
- Create a database for the application.
- Create a `.env` file in the root of the project and add the following line:
  ```
  DATABASE_URL=postgresql://<YOUR_USER>:<YOUR_PASSWORD>@<YOUR_HOST>:<YOUR_PORT>/<YOUR_DATABASE_NAME>
  ```
  Replace the placeholders with your actual database credentials.
  
  **Important:** If your password contains special characters like `@`, `#`, `$`, etc., you need to URL-encode them. For example, `@` should be replaced with `%40`.

## 3. Run the Application

- Use the following command to run the application:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```
- The application will be available at `http://127.0.0.1:8001`.

## 4. Running Tests (Optional)

- If you have `pytest` installed, you can run the tests with the following command:
  ```bash
  pytest
  ```
