# Telegram Button Bot

This bot allows you to manage buttons in categories, with each button linking to a specific URL. You can add, edit, and delete buttons directly through the bot.

## Features
- Categories for buttons.
- Add, edit, and delete buttons via commands.
- Bot stats for the admin.
- User interaction tracking.

## Requirements
- Python 3.x
- MongoDB (local or MongoDB Atlas)

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/telegram-button-bot.git
    cd telegram-button-bot
    ```

2. Create a virtual environment and activate it:
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file with the following content:
    ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    MONGO_URI=your_mongo_connection_string
    SUDO_USER_ID=your_telegram_user_id
    ```

5. Run the bot:
    ```
    python bot.py
    ```

## Deployment on Koyeb

1. Create a Koyeb account and set up a new app.
2. Link your GitHub repository to the app.
3. Koyeb will automatically detect the `Procfile` and deploy the bot.

## Usage

Once the bot is running, you can interact with it by typing `/start` in the chat.

### Admin Commands (Sudo Users Only)
- `/add_button <category> <name> <link>` - Add a new button.
- `/edit_button <button_id> <name> <link>` - Edit an existing button.
- `/delete_button <button_id>` - Delete a button.
- `/bot_stats` - View bot statistics (e.g., total users and buttons).

