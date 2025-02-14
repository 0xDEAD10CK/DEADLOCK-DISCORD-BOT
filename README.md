# README.md

# Discord Bot Project

This is a simple Discord bot project that demonstrates the use of cogs to organize commands and event listeners.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd discord-bot-project
   ```

2. **Install dependencies:**
   Make sure you have Python 3.8 or higher installed. Then, run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:**
   Create a file named `.env` in the `src` directory and add your Discord bot token and other necessary IDs:
   ```sh
   DISCORD_TOKEN=your_token_here
   OWNER_ID=your_discord_user_id
   ROLES_CHANNEL_ID=your_role_text_channel_id
   VERIFICATION_CHANNEL_ID=your_verification_channel_id
   VERIFIED_ROLE_ID=your_verified_role_id
   GUILD_ID=your_guild_id
   ```

4. **Optional Verification: Set up Discord channels and roles**
   - Create a **rules channel** where users can read the rules.
   - Create a **verification channel** where verification requests will be sent.
   - Create a **verified role** that will be assigned to users once they are verified.
   - Add the IDs of these channels and role to the `.env` file as shown above.

   - The Verified roles permissions should be able to see all the things you want. e.g. messages, history
   - The @everyone roles should be cleared of permissions.
   - The Rules channel permissions for @everyone should allow View Channel, Add Reactions and Read Message History.


## Running the Bot

To start the bot, run the following command:
```sh
python src/bot.py
```

## Usage

Once the bot is running, it will respond to commands defined in the cogs. You can add more cogs by creating new files in the `src/cogs` directory and loading them in `bot.py`.

## Example Cog

The `example_cog.py` file contains a sample cog with a command and an event listener. You can modify it to add your own functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.