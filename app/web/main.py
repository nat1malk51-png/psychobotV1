# app/web/main.py - FastAPI application entry point
"""
FastAPI web interface for PsychoBot.
Serves both client booking interface and admin management UI.
Authentication handled by Nginx Proxy Manager for /admin routes.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.web.routers import client, admin
from app.translations import get_text, get_cached_languages

# Initialize FastAPI app
app = FastAPI(
    title="PsychoBot Web Interface",
    description="Web interface for psychotherapy booking bot",
    version="1.0"
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Mount routers
app.include_router(client.router)
app.include_router(admin.router, prefix="/admin")

templates = Jinja2Templates(directory="app/web/templates")

# Root redirect / Home Page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, lang: str = "ru"):
    """
    Landing page with language support and content loading.
    Reads HTML files from /app/landings/ just like the Telegram bot.
    """
    
    # 1. Define topics and their translation keys (same as in Telegram bot)
    # The order here determines the tab order in the UI
    topics_map = [
        ("work_terms", "menu_terms"),         # Условия работы
        ("qualification", "menu_qual"),       # Квалификация
        ("about_psychotherapy", "menu_about") # О психотерапии
    ]
    
    landings = {}
    has_content = False
    
    # 2. Try to load content for each topic from files
    for file_prefix, title_key in topics_map:
        # File path matches what is used in app/handlers/common.py
        # Try absolute path first (Docker), then relative (Local dev)
        file_path = f"/app/landings/{file_prefix}_{lang}.html"
        
        content = ""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        
        # Only add to list if we found content
        if content:
            landings[file_prefix] = {
                "title": get_text(lang, title_key), # Get translated title (e.g. "Условия работы")
                "content": content
            }
            has_content = True

    # 3. Get languages for the switcher
    # Using the helper from translations.py (or hardcoded fallback)
    # This matches the structure expected by index.html: items() -> key, value
    available_langs = {
        "ru": "Русский",
        "am": "Հայերեն" # Fixed typo
    }

    return templates.TemplateResponse("client/index.html", {
        "request": request,
        "lang": lang,
        "languages": available_langs,
        "landings": landings,
        "has_content": has_content
    })