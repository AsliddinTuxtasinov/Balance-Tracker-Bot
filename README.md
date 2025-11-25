# Telegram Web App with Docker Compose

This project provides a complete architecture for running a Telegram Web App using Docker Compose. It includes a Django backend, a PostgreSQL database, an Aiogram bot, and Ngrok for secure HTTPS tunneling.

## Architecture

The project consists of 4 Docker services:

1.  **`web`**: A Django application serving the Web App frontend (Hello World).
2.  **`db`**: PostgreSQL database for the Django app.
3.  **`ngrok`**: Exposes the `web` service to the internet via a secure HTTPS tunnel.
4.  **`bot`**: An Aiogram Python bot that:
    *   Automatically fetches the public HTTPS URL from the `ngrok` service.
    *   Sends a "Open Web App" button to users with the correct dynamic URL.

## Prerequisites

*   Docker and Docker Compose installed.
*   A Telegram Bot Token (from [@BotFather](https://t.me/BotFather)).
*   An Ngrok Authtoken (from [ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)).

## Setup Instructions

1.  **Clone the repository** (if applicable) or navigate to the project folder.

2.  **Configure Environment Variables**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Open `.env` and fill in your credentials:
    *   `BOT_TOKEN`: Your Telegram Bot Token.
    *   `NGROK_AUTHTOKEN`: Your Ngrok Authtoken.
    *   (Optional) Change DB credentials if needed.

3.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

4.  **Usage**:
    *   Open your bot in Telegram.
    *   Send the `/start` command.
    *   The bot will reply with a button "Open Web App".
    *   Click the button to open the "Hello World" page served by Django via the secure Ngrok tunnel.

## Project Structure

```
.
├── bot/                # Telegram Bot source code
│   ├── Dockerfile
│   ├── main.py         # Bot logic (polling Ngrok API)
│   └── requirements.txt
├── web/                # Django Web App source code
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── backend/        # Django project settings
│   ├── core/           # Django app (views, urls)
│   └── templates/      # HTML templates
├── docker-compose.yml  # Service definitions
├── .env.example        # Environment variables template
└── README.md           # This file
```

## How it works

*   **Dynamic URL**: The `ngrok` container exposes an API at `http://ngrok:4040/api/tunnels`.
*   **Bot Logic**: The `bot` container periodically polls this API to find the public HTTPS URL.
*   **Seamless Experience**: When you restart the containers, Ngrok generates a new URL. The bot automatically detects this change and updates the button link, so you don't need to manually update anything.
