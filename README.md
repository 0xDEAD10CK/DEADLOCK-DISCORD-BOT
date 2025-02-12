# README.md

# Discord Bot Project

This is a simple Discord bot project that demonstrates the use of cogs to organize commands and event listeners.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd discord-bot-project
   ```

2. **Install dependencies:**
   Make sure you have Python 3.8 or higher installed. Then, run:
   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:**
   Create a file named `.env` in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

## Running the Bot

To start the bot, run the following command:
```
python src/bot.py
```

## Usage

Once the bot is running, it will respond to commands defined in the cogs. You can add more cogs by creating new files in the `src/cogs` directory and loading them in `bot.py`.

## Example Cog

The `example_cog.py` file contains a sample cog with a command and an event listener. You can modify it to add your own functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.