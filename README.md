# Discord Music Bot

This is a Discord bot that plays music from various sources. RuTube as an example.

## Installation

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory and add your Discord token:
    ```plaintext
    DISCORD_TOKEN=your_discord_token_here
    ```
5. Run the bot:
    ```bash
    python bot.py
    ```

## Usage

- `$play <url>`: Plays music from the given URL.
- `$pause`: Pauses the current playing music.
- `$resume`: Resumes the paused music.
- `$stop`: Stops the music and disconnects the bot from the voice channel.
- `$queue <url>`: Adds the URL to the queue.
- `$clear_queue`: Clears the music queue.
