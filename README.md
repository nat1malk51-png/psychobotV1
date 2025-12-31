# Psychotherapy Booking Bot V1.0 (In work curently)

Telegram bot for psychotherapists to manage client bookings: online/onsite, individual/couple sessions, time negotiation, waitlist, and admin tools. Now with webUI for clients and admin. NPM to register your domain and request certificate. Added ability to add aditional languages from web admin UI.
# Psychotherapy Booking Bot v1.0.X

A hybrid booking management system for psychotherapists combining a Telegram Bot interface with a modern Web UI. Designed to handle scheduling, client negotiations, content management, and multi-language support efficiently.

## 🚀 New in v1.0.X
* **Web Admin Dashboard:** Full graphical interface to manage bookings, content, and settings.
* **Web Client Booking:** Clients can now book slots directly via a web interface in addition to the Telegram bot.
* **Dynamic Content:** Add languages and edit translations directly from the database without code changes.
* **Flexible Infrastructure:** Native Docker support for both Nginx Proxy Manager and Cloudflare Tunnel.

## Features

### 🤖 For Clients
* **Dual Interface:** Book via Telegram chat flow or a clean Web UI.
* **Smart Booking:** View available slots, request specific times, or join a waitlist.
* **Multi-Language:** Interface available in Russian, Armenian, and easily extensible to others via the Admin Panel.
* **Info Hub:** Access HTML landing pages (Terms, Qualifications, About) directly within the bot.

### 🛠 For Therapists (Admin)
* **Web Dashboard:**
    * **Slot Management:** Create, hold, and release appointment slots visually.
    * **Request Handling:** Approve, reject, or propose alternative times for booking requests.
    * **Content Management:** Edit "Landing" pages (HTML) and system translations on the fly.
    * **Settings:** Configure timezones, prices, and languages.
* **Telegram Admin Tools:** Quick toggles for availability, immediate request notifications, and basic management commands.
* **Negotiation History:** Full log of proposals and counter-proposals stored in PostgreSQL.

### ⚙️ Technical Highlights
* **Backend:** Python 3.10+ (Aiogram 3.x + FastAPI).
* **Database:** PostgreSQL 15 with SQLAlchemy & Alembic migrations.
* **Deployment:** Docker Compose with **Profiles** for easy proxy switching.
* **Security:** Environment-based configuration, hidden internal ports.

---

## Quick Start (Docker)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/abriesk/psychobot.git](https://github.com/abriesk/psychobotV1.git)
    cd psychobot
    ```

2.  **Configure Environment:**
    Create a `.env` file (see provided example) with your credentials:
    ```env
    BOT_TOKEN=your_token
    ADMIN_IDS=123456789
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=secret
    
    # Choose your proxy profile: 'npm' or 'cloudflare'
    COMPOSE_PROFILES=npm
    # TUNNEL_TOKEN=ey... (Required if using cloudflare)
    ```

3.  **Run with Docker:**
    The system uses Docker profiles to launch the appropriate proxy service.
    ```bash
    docker compose up --build -d
    ```

4.  **Access:**
    * **Telegram:** Start your bot via the Telegram app.
    * **Web Admin:** Access via `https://your-domain.com/admin` (configured via NPM or Cloudflare).

---

## Configuration & Customization

* **Proxy Switching:**
    Change the `COMPOSE_PROFILES` variable in `.env` to switch between Nginx Proxy Manager (`npm`) and Cloudflare Tunnel (`cloudflare`). No manual container manipulation required.
    
* **Adding Languages:**
    Go to the Web Admin Panel → **Languages** → Add New. The system automatically handles database migration for new translation keys.

* **Landing Pages:**
    Upload HTML files via the Web Admin Panel or the Telegram `/admin` menu.

---

## Credits & Contribution

This project was born from a real need and built collaboratively with the help of several LLMs under human direction.

* **Concept & Core Strategy:** Ab (Горилла in Chief 🦍)
* **Grok (xAI):** Technical requirements compilation.
* **Gemini (Google):** Generated the initial MVP architectural foundation for v0.8, core Python handlers, and performed final system-wide code reviews for version 0.8, bug fixes for v1.0, and cloudflared update.
* **Claude (Anthropic):** Gap analysis, feature implementation, and critical UX fixes for v0.8, most works on UI and backend code for update to v1.0.X.

Pull requests are welcome!
(foloowing description right now copy-pasted from v0.8)
## Features

- Multi-language interface (Russian + Armenian, easy to extend)
- Booking flow: type (individual/couple), format (online/onsite), timezone, desired time, problem description
- Flexible time negotiation (client ↔ therapist proposals/counter-proposals)
- Waitlist mode when availability is off
- Admin panel:
  - Toggle availability
  - View/manage pending requests (approve, propose alt time, reject)
  - Edit prices (displayed in buttons)
  - Upload HTML landing pages (terms, qualification, about therapy, references)
- Persistent main menu with "Home" button
- Docker-ready with PostgreSQL
- Full negotiation history stored in DB

## Quick Start (Docker)

1. Clone the repo:
   ```bash
   git clone https://github.com/abriesk/psychobot.git
   cd psychobot
2. Create or edit .env file:
   BOT_TOKEN=your_telegram_bot_token_here
   ADMIN_IDS=123456789,987654321  # your Telegram user IDs, comma-separated
   DEFAULT_LANGUAGE=ru
   CLINIC_ONSITE_LINK=https://example-clinic.com/booking
   POSTGRES_DB=psychobot
   POSTGRES_USER=postgres
3. Build and run:
   docker compose up --build -d
4. Start chatting with your bot and run /start. Admin commands appear after /admin.

   Customization

Add/edit HTML landing pages in /landings folder (volume-mounted in Docker)
Admin → "Upload Landing" to add new ones via bot
Prices edited via "Edit Prices" in admin panel
Add more languages in app/translations.py

Contributing
This project was born from a real need and built collaboratively with the help of several LLMs under human direction.

Concept & Core Strategy: Ab (Горилла in Chief 🦍)
Grok (xAI): In-depth code reviews, bug hunting & fixes (negotiation symmetry, final_time logic, flow consistency), UI/UX suggestions, and collaborative polishing throughout development.
Gemini (Google): Generated the initial MVP architectural foundation, core Python handlers, and performed final system-wide code reviews for version 0.8.
Claude (Anthropic): Gap analysis, feature implementation, and critical UX fixes for v0.8.

Pull requests welcome! Especially: new languages, cancellation flow, separate contacts collection, richer admin stats.
POSTGRES_PASSWORD=securepassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
