# YouTube Clone

A modern YouTube clone built with Django, featuring video upload, playback, user authentication, and more.

## 🚀 Features

- User authentication and profile management
- Video upload and streaming
- Video playback with comments
- Like and dislike functionality
- Docker containerization
- YouTube API integration for video import

## 🛠️ Tech Stack

- **Backend**: Django 5.2
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Containerization**: Docker & Docker Compose
- **Authentication**: Django's built-in authentication system
- **YouTube Integration**: Google API Client for random video imports

## 📋 Prerequisites

- Python 3.12.6+
- Docker and Docker Compose
- Git
- YouTube Data API Key (for video import feature)

## 🚀 Getting Started


2. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```

3. **Using Docker (Recommended)**
   ```bash
   docker compose up        # Run in foreground
   docker compose up -d     # Run in background
   ```

4. **Local Development**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

## 📁 Project Structure

```
youtube-clone/
├── content/          # Video content management
├── templates/        # HTML templates
├── users/           # User management
├── youtube_clone/   # Main project configuration
├── docker-compose.yml
├── Dockerfile
├── gunicorn.py
├── nginx.conf
└── requirements.txt
```

## 🔧 Configuration

- **Django Settings**: Located in `youtube_clone/settings.py`
- **Nginx Configuration**: `nginx.conf`
- **Gunicorn Configuration**: `gunicorn.py`
- **Docker Configuration**: `Dockerfile` and `docker-compose.yml`

## 📹 Importing YouTube Videos

The project includes a management command to import random YouTube videos. To use it:

1. **Get a YouTube API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create credentials (API key)

2. **Import Videos**
   ```bash
   python manage.py import_random_youtube_videos --count 100 --user your_username --api-key YOUR_API_KEY
   ```

   Parameters:
   - `--count`: Number of videos to import (default: 100)
   - `--user`: Username of the user who will upload the videos
   - `--api-key`: Your YouTube API key (can also be set as YOUTUBE_API_KEY environment variable)

   The command will:
   - Import videos with titles and embed URLs
   - Assign the specified user as the uploader


## 👥 Authors

Hugo Montañez



