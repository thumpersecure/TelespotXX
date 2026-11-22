<p align="center">
  <img src="https://img.icons8.com/fluency/96/phone-disconnected.png" alt="TeleSpotter Logo" width="96" height="96">
</p>

<h1 align="center">🔍 telespotXX Web</h1>

<p align="center">
  <strong>The Ultimate Phone Number Intelligence Platform</strong>
</p>

<p align="center">
  <em>Transform any phone number into actionable intelligence with our powerful OSINT web application. Search across multiple engines, extract patterns, and uncover connections — all in real-time.</em>
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick%20Start-blue?style=for-the-badge" alt="Quick Start"></a>
  <a href="#-features"><img src="https://img.shields.io/badge/Features-green?style=for-the-badge" alt="Features"></a>
  <a href="#-documentation"><img src="https://img.shields.io/badge/Documentation-orange?style=for-the-badge" alt="Documentation"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Socket.IO-Real--Time-010101?style=flat-square&logo=socket.io&logoColor=white" alt="Socket.IO">
  <img src="https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
</p>

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📱 Supported Phone Formats](#-supported-phone-formats)
- [🔧 How to Use](#-how-to-use)
- [🗂️ Project Structure](#️-project-structure)
- [🔌 API Reference](#-api-reference)
- [⚡ WebSocket Events](#-websocket-events)
- [🐳 Docker Deployment](#-docker-deployment)
- [⚙️ Configuration](#️-configuration)
- [🛡️ Security & Privacy](#️-security--privacy)
- [⚠️ Disclaimer](#️-disclaimer)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

**TeleSpotter Web** is a powerful, user-friendly web application designed for **Open Source Intelligence (OSINT)** research on phone numbers. Whether you're a security researcher, investigator, or just curious about an unknown caller, TeleSpotter provides comprehensive insights by aggregating data from multiple sources.

### 🎯 What Can TeleSpotter Do?

| Capability | Description |
|------------|-------------|
| 🔎 **Multi-Source Search** | Query Google, Bing, and DuckDuckGo simultaneously |
| 👥 **People Database Lookup** | Search across 5+ major people search platforms |
| 🧠 **Intelligent Extraction** | Automatically identify names, emails, addresses from results |
| 📍 **Location Intelligence** | Identify country, region, carrier information |
| 🔗 **Social Discovery** | Find linked social media profiles and usernames |
| 📊 **Real-Time Results** | Watch results populate live via WebSocket |
| 📁 **Flexible Export** | Download findings as JSON, CSV, or TXT reports |

---

## ✨ Features

### 🔍 **Search Engines Integration**

<table>
<tr>
<td align="center" width="33%">
<img src="https://img.icons8.com/color/48/google-logo.png" width="48"><br>
<strong>Google</strong><br>
<sub>World's largest search engine</sub>
</td>
<td align="center" width="33%">
<img src="https://img.icons8.com/color/48/bing.png" width="48"><br>
<strong>Bing</strong><br>
<sub>Microsoft's search platform</sub>
</td>
<td align="center" width="33%">
<img src="https://img.icons8.com/color/48/duckduckgo--v2.png" width="48"><br>
<strong>DuckDuckGo</strong><br>
<sub>Privacy-focused search</sub>
</td>
</tr>
</table>

### 👥 **People Search Platforms**

| Platform | Features |
|----------|----------|
| 📘 **Whitepages** | Names, addresses, relatives, background info |
| 🔵 **TruePeopleSearch** | Free comprehensive people search |
| ⚡ **FastPeopleSearch** | Quick lookup with detailed records |
| 🟣 **Spokeo** | Aggregated public records |
| ✅ **BeenVerified** | Background check integration |

### 🧠 **Pattern Analysis Engine**

Our intelligent pattern analyzer extracts valuable information from search results:

- 👤 **Names** — Identifies potential owner names with confidence scores
- 📧 **Emails** — Extracts associated email addresses
- 🏠 **Addresses** — Finds physical addresses and locations
- 🔗 **Usernames** — Discovers social media handles
- 📱 **Associated Phones** — Finds related phone numbers
- 🌐 **Social Profiles** — Links to Facebook, Twitter, LinkedIn, Instagram, and more

### 💻 **Modern User Interface**

- 🌙 **Dark Theme** — Easy on the eyes, perfect for extended research sessions
- 📱 **Fully Responsive** — Works seamlessly on desktop, tablet, and mobile
- ⚡ **Real-Time Updates** — Live progress and results via WebSocket
- 🎨 **Beautiful Design** — Modern UI built with Tailwind CSS

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.11+** or **Docker**
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 🖥️ Option 1: Run Locally

```bash
# 📥 Clone the repository
git clone https://github.com/thumpersecure/TelespotXX.git
cd TelespotXX/webapp

# 🐍 Create virtual environment
python -m venv venv

# 🔌 Activate virtual environment
source venv/bin/activate        # Linux/macOS
# OR
venv\Scripts\activate           # Windows

# 📦 Install dependencies
pip install -r requirements.txt

# 🚀 Launch the application
python app.py
```

🎉 **That's it!** Open your browser and visit: **http://localhost:5000**

### 🐳 Option 2: Docker (Recommended for Production)

```bash
# 📥 Navigate to webapp directory
cd TelespotXX/webapp

# 🏗️ Build and run with Docker Compose
docker-compose up --build

# OR build manually
docker build -t telespotter .
docker run -p 5000:5000 telespotter
```

🎉 **Done!** Access the app at: **http://localhost:5000**

---

## 📱 Supported Phone Formats

TeleSpotter is **flexible** and accepts phone numbers in virtually any format:

| Format Type | Example | ✅ Supported |
|-------------|---------|:------------:|
| **International** | `+1 (555) 123-4567` | ✅ |
| **International (no spaces)** | `+15551234567` | ✅ |
| **US Standard** | `(555) 123-4567` | ✅ |
| **Dashed** | `555-123-4567` | ✅ |
| **Dotted** | `555.123.4567` | ✅ |
| **Spaced** | `555 123 4567` | ✅ |
| **Plain Digits** | `5551234567` | ✅ |
| **With Country Code** | `1-555-123-4567` | ✅ |
| **UK Format** | `+44 20 7946 0958` | ✅ |
| **Other International** | `+49 30 12345678` | ✅ |

> 💡 **Pro Tip:** TeleSpotter automatically normalizes and validates phone numbers, so don't worry about formatting!

---

## 🔧 How to Use

### Step 1️⃣ — Enter Phone Number

Type or paste any phone number into the search box. The app will automatically validate it and show a ✅ checkmark when the format is recognized.

### Step 2️⃣ — Configure Search Options *(Optional)*

Click **"Advanced Options"** to customize your search:

<details>
<summary><strong>🔍 Search Engines</strong></summary>

| Engine | Default | Description |
|--------|:-------:|-------------|
| Google | ✅ On | Most comprehensive results |
| Bing | ✅ On | Good for different perspectives |
| DuckDuckGo | ✅ On | Privacy-focused, unique results |

</details>

<details>
<summary><strong>👥 People Search Sites</strong></summary>

| Site | Default | Description |
|------|:-------:|-------------|
| Whitepages | ✅ On | Comprehensive phone directory |
| TruePeopleSearch | ✅ On | Free detailed lookups |
| FastPeopleSearch | ✅ On | Quick results |
| Spokeo | ✅ On | Aggregated records |
| BeenVerified | ✅ On | Background checks |

</details>

<details>
<summary><strong>🧠 Analysis Options</strong></summary>

| Option | Default | What it Extracts |
|--------|:-------:|------------------|
| Extract Names | ✅ On | Owner names, associated people |
| Extract Emails | ✅ On | Email addresses |
| Extract Addresses | ✅ On | Physical locations |
| Find Social Profiles | ✅ On | Social media links |

</details>

### Step 3️⃣ — Start the Search

Click the **"🔍 Start Search"** button and watch the magic happen!

- 📊 **Progress Bar** — Shows real-time search progress
- 📝 **Live Log** — Displays what's happening at each step
- ⚡ **Instant Results** — Data appears as soon as it's found

### Step 4️⃣ — Review Results

Results are organized into easy-to-navigate tabs:

| Tab | Contents |
|-----|----------|
| 🧠 **Extracted Data** | Names, emails, addresses, usernames, social profiles |
| 🔍 **Search Results** | Links from Google, Bing, DuckDuckGo |
| 👥 **People Search** | Records from people search databases |

### Step 5️⃣ — Export Your Findings

Download your research in your preferred format:

| Format | Best For | Icon |
|--------|----------|:----:|
| **JSON** | Developers, automation, APIs | 📄 |
| **CSV** | Excel, Google Sheets, data analysis | 📊 |
| **TXT** | Reports, documentation, sharing | 📝 |

---

## 🗂️ Project Structure

```
📁 TelespotXX/
├── 📄 README.md                    # You are here!
├── 📄 LICENSE                      # MIT License
│
└── 📁 webapp/                      # Main application
    ├── 🐍 app.py                   # Flask application & WebSocket
    │
    ├── 📁 modules/                 # Core functionality
    │   ├── 📱 phone_utils.py       # Phone parsing & validation
    │   ├── 🔍 search_engines.py    # Google, Bing, DuckDuckGo
    │   ├── 👥 people_search.py     # People search integrations
    │   └── 🧠 pattern_analysis.py  # Pattern extraction engine
    │
    ├── 📁 templates/
    │   └── 🌐 index.html           # Web interface
    │
    ├── 📁 static/                  # CSS, JS, images
    │   ├── 📁 css/
    │   └── 📁 js/
    │
    ├── 📦 requirements.txt         # Python dependencies
    ├── 🐳 Dockerfile               # Docker configuration
    ├── 🐳 docker-compose.yml       # Docker Compose setup
    ├── ⚙️ .env.example             # Environment template
    └── 🚫 .gitignore               # Git ignore rules
```

---

## 🔌 API Reference

TeleSpotter provides a RESTful API for programmatic access:

### 🔍 Start a Search

```http
POST /api/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone_number": "+1 555-123-4567",
  "options": {
    "google": true,
    "bing": true,
    "duckduckgo": true,
    "whitepages": true,
    "truepeoplesearch": true,
    "fastpeoplesearch": true,
    "spokeo": true,
    "beenverified": true
  }
}
```

**Response:**
```json
{
  "session_id": "search_1704567890123_1234",
  "status": "started",
  "phone_number": "+1 555-123-4567"
}
```

### 📊 Get Search Status

```http
GET /api/search/{session_id}
```

**Response:** Full results object with progress and all extracted data.

### 📥 Export Results

```http
GET /api/search/{session_id}/export?format={json|csv|txt}
```

Returns downloadable file in specified format.

### ✅ Validate Phone Number

```http
POST /api/validate
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone_number": "+1 555-123-4567"
}
```

**Response:**
```json
{
  "valid": true,
  "formatted": "+1 (555) 123-4567",
  "country": "United States/Canada",
  "country_code": "1",
  "location": "California",
  "line_type": "Mobile"
}
```

---

## ⚡ WebSocket Events

Connect to receive real-time updates during searches:

```javascript
// 🔌 Connect to WebSocket
const socket = io();

// 🚪 Join a search session
socket.emit('join', { session_id: 'search_123' });

// 📊 Listen for progress updates
socket.on('progress', (data) => {
  console.log(`Progress: ${data.progress}%`);
  console.log(`Status: ${data.message}`);
});

// 📦 Listen for new results
socket.on('result', (data) => {
  console.log(`New ${data.type} result:`, data.data);
});

// ✅ Handle completion
socket.on('complete', (data) => {
  console.log('Search complete!', data);
});
```

### 📡 Event Types

| Event | Description | Data |
|-------|-------------|------|
| `progress` | Search progress update | `{ progress: 0-100, message: string, status: string }` |
| `result` | New result found | `{ type: string, data: object }` |
| `joined` | Successfully joined session | `{ session_id: string }` |

---

## 🐳 Docker Deployment

### 🏃 Quick Start

```bash
cd webapp
docker-compose up -d
```

### 🏭 Production Deployment

```bash
# Build optimized production image
docker build -t telespotter:prod .

# Run with production settings
docker run -d \
  --name telespotter \
  -p 80:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-super-secret-key \
  --restart unless-stopped \
  telespotter:prod
```

### 🔧 Docker Compose Options

```yaml
# docker-compose.yml
services:
  telespotter:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
```

---

## ⚙️ Configuration

### 📝 Environment Variables

Copy `.env.example` to `.env` and customize:

```env
# 🔧 Flask Configuration
FLASK_ENV=development          # or 'production'
FLASK_DEBUG=1                  # 0 for production
SECRET_KEY=change-this-key     # Use a strong random key!

# 🌐 Server Configuration
PORT=5000
HOST=0.0.0.0

# 🔑 Optional: API Keys for enhanced results
# GOOGLE_API_KEY=your-google-api-key
# BING_API_KEY=your-bing-api-key
```

### 🔐 Generating a Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🛡️ Security & Privacy

### 🔒 Your Privacy Matters

- **No Data Storage** — Searches are processed in real-time and NOT stored on our servers
- **Session-Based** — Results only exist in your browser session
- **No Tracking** — We don't track your searches or collect personal data
- **Open Source** — Audit the code yourself!

### 🛡️ Security Best Practices

1. **Change the default `SECRET_KEY`** before deploying to production
2. **Use HTTPS** in production (set up SSL/TLS)
3. **Implement rate limiting** if exposing publicly
4. **Keep dependencies updated** with `pip install --upgrade -r requirements.txt`

---

## ⚠️ Disclaimer

<table>
<tr>
<td>⚠️</td>
<td>

**IMPORTANT: This tool is intended for legitimate OSINT research purposes only.**

By using TeleSpotter, you agree to:

- ✅ Use it only for **lawful purposes**
- ✅ Comply with all **applicable laws** and regulations
- ✅ Respect **privacy** and **ethical boundaries**
- ✅ Take **responsibility** for your actions

**DO NOT use TeleSpotter for:**

- ❌ Harassment or stalking
- ❌ Identity theft or fraud
- ❌ Unauthorized surveillance
- ❌ Any illegal activities

**Results Disclaimer:**
- Results are aggregated from **publicly available sources**
- Information may be **outdated or inaccurate**
- Always **verify** findings through official channels
- TeleSpotter makes **no guarantees** about data accuracy

</td>
</tr>
</table>

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Found a Bug?
Open an [issue](https://github.com/thumpersecure/TelespotXX/issues) with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior

### 💡 Have an Idea?
We'd love to hear it! Open an issue with the `enhancement` label.

### 🔧 Want to Contribute Code?

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📝 Code Style

- Follow **PEP 8** for Python code
- Use **meaningful** variable and function names
- Add **comments** for complex logic
- Write **tests** for new features

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 THUMPER33

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgments

- 🔧 Inspired by the original [Telespotter](https://github.com/thumpersecure/Telespotter) CLI tool
- 🎨 UI built with [Tailwind CSS](https://tailwindcss.com/)
- ⚡ Real-time updates powered by [Socket.IO](https://socket.io/)
- 🐍 Backend powered by [Flask](https://flask.palletsprojects.com/)

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/thumpersecure">thumpersecure</a></strong>
</p>

<p align="center">
  <a href="https://github.com/thumpersecure/TelespotXX">⭐ Star this repo</a> •
  <a href="https://github.com/thumpersecure/TelespotXX/issues">🐛 Report Bug</a> •
  <a href="https://github.com/thumpersecure/TelespotXX/issues">💡 Request Feature</a>
</p>

<p align="center">
  <sub>If TeleSpotter helped you, consider giving it a ⭐!</sub>
</p>

Made by [justinhorn.pro](https://justinhorn.pro)
