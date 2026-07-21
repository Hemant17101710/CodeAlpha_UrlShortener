
A simple URL Shortener backend built with **Flask** and **SQLite**, made for the CodeAlpha Backend Development Internship (Task 1).

## Features
- Backend server built with Flask (Python)
- API endpoint to accept long URLs and generate a unique short code
- SQLite database to store the mapping between short codes and original URLs
- Redirect route: visiting the short URL takes you to the original long URL
- Basic frontend to input a long URL and view/copy the shortened version
- Bonus: click-tracking stats endpoint

## Project Structure
```
CodeAlpha_UrlShortener/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── README.md
```

## Setup & Run

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/CodeAlpha_UrlShortener.git
   cd CodeAlpha_UrlShortener
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000/`

## API Endpoints

### 1. Shorten a URL
`POST /api/shorten`

Request body:
```json
{ "url": "https://www.example.com/some/very/long/link" }
```

Response:
```json
{
  "original_url": "https://www.example.com/some/very/long/link",
  "short_code": "aZ3kP9",
  "short_url": "http://127.0.0.1:5000/aZ3kP9"
}
```

### 2. Redirect
`GET /<short_code>`

Redirects to the original long URL.

### 3. Stats (bonus)
`GET /api/stats/<short_code>`

Returns metadata: original URL, creation time, and number of clicks.

## Tech Stack
- Python
- Flask
- SQLite3
- HTML/CSS/JavaScript (frontend)

## Author
Built as part of the CodeAlpha Backend Development Internship.
