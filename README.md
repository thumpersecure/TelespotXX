# TeleSpotter Web Application

A comprehensive phone number OSINT (Open Source Intelligence) web application. Search phone numbers across multiple search engines and people search databases, with automatic pattern extraction and analysis.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Multi-Engine Search**: Query Google, Bing, and DuckDuckGo simultaneously
- **People Search Integration**: Search Whitepages, TruePeopleSearch, FastPeopleSearch, Spokeo, BeenVerified
- **Pattern Analysis**: Automatically extract names, emails, addresses, usernames, and social profiles
- **Real-Time Updates**: WebSocket-powered live progress and result updates
- **Export Options**: Download results as JSON, CSV, or formatted text reports
- **Modern UI**: Responsive dark-themed interface with Tailwind CSS
- **Easy Deployment**: Docker support for quick deployment

## Quick Start

### Option 1: Run Locally

```bash
# Clone the repository
git clone https://github.com/thumpersecure/TelespotXX.git
cd TelespotXX/webapp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

### Option 2: Docker

```bash
cd webapp

# Build and run
docker-compose up --build

# Or just build
docker build -t telespotter .
docker run -p 5000:5000 telespotter
```

## Usage

### 1. Enter Phone Number

Enter any phone number in the search box. Supported formats:
- International: `+1 (555) 123-4567`
- US Standard: `(555) 123-4567`
- Dashed: `555-123-4567`
- Dotted: `555.123.4567`
- Plain: `5551234567`

### 2. Configure Options (Optional)

Click "Advanced Options" to customize your search:

**Search Engines:**
- Google
- Bing
- DuckDuckGo

**People Search Sites:**
- Whitepages
- TruePeopleSearch
- FastPeopleSearch
- Spokeo
- BeenVerified

**Analysis Options:**
- Extract Names
- Extract Emails
- Extract Addresses
- Find Social Profiles

### 3. View Results

Results are displayed in real-time as searches complete:

- **Phone Information**: Country, location, carrier, line type
- **Extracted Names**: Names associated with the number
- **Email Addresses**: Found email addresses
- **Physical Addresses**: Street addresses and locations
- **Usernames**: Social media handles
- **Social Profiles**: Links to social media profiles
- **Associated Phones**: Related phone numbers

### 4. Export Results

Export your findings in multiple formats:
- **JSON**: Full structured data for programmatic use
- **CSV**: Spreadsheet-compatible format
- **TXT**: Human-readable report

## Project Structure

```
webapp/
├── app.py                 # Main Flask application
├── modules/
│   ├── __init__.py
│   ├── phone_utils.py     # Phone number parsing
│   ├── search_engines.py  # Search engine modules
│   ├── people_search.py   # People search modules
│   └── pattern_analysis.py # Pattern extraction
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   └── js/
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose config
├── .env.example          # Environment variables template
└── .gitignore
```

## API Endpoints

### Start Search
```
POST /api/search
Content-Type: application/json

{
  "phone_number": "+1 555-123-4567",
  "options": {
    "google": true,
    "bing": true,
    "duckduckgo": true,
    "whitepages": true,
    "truepeoplesearch": true
  }
}
```

### Get Search Status
```
GET /api/search/<session_id>
```

### Export Results
```
GET /api/search/<session_id>/export?format=json|csv|txt
```

### Validate Phone Number
```
POST /api/validate
Content-Type: application/json

{
  "phone_number": "+1 555-123-4567"
}
```

## WebSocket Events

Connect to receive real-time updates:

```javascript
const socket = io();

// Join a search session
socket.emit('join', { session_id: 'search_123' });

// Listen for progress
socket.on('progress', (data) => {
  console.log(`${data.progress}% - ${data.message}`);
});

// Listen for results
socket.on('result', (data) => {
  console.log('New result:', data);
});
```

## Configuration

Copy `.env.example` to `.env` and configure:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

## Deployment

### Production with Gunicorn

```bash
gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
         --workers 1 --bind 0.0.0.0:5000 app:app
```

### Docker Production

```bash
docker-compose --profile production up -d
```

## Disclaimer

This tool is intended for **legitimate OSINT research purposes only**. Users are responsible for ensuring their use complies with all applicable laws and regulations.

**Do NOT use this tool for:**
- Harassment or stalking
- Identity theft
- Any illegal purposes
- Unauthorized surveillance

Results are aggregated from public sources and may not always be accurate or up-to-date.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Telespotter](https://github.com/thumpersecure/Telespotter) CLI tool
- Built with Flask, Socket.IO, and Tailwind CSS
