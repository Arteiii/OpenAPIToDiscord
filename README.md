# OpenAPI to Discord Bot

This Discord bot allows you to interact with an API using Discord commands.
It uses Discord.py for the Discord interactions and HTTPx for making API requests.
The bot provides functionality to list available API operations, call specific API routes, and check the bot's latency.

**Note:** This bot was primarily tested with the default FastAPI configuration. Additional changes in the code might be needed to work properly with different APIs.

## Features

- List available API operations with detailed information.
- Call specific API routes and display the API response.
- Check bot latency with color-coded status (green for normal, orange for high, red for big latency).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Arteiii/OpenAPIToDiscord.git
   ```

2. Navigate to the project directory:

   ```bash
    cd OpenAPIToDiscord
    ```

3. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

    If you don't have Poetry installed, follow the Poetry [installation guide](https://python-poetry.org/docs/#installation) to install it.

4. Create a .env file in the project root and add your Discord bot token and API base URL:

    ```env
    DISCORD_BOT_TOKEN=your_discord_bot_token
    API_BASE_URL=your_api_base_url
    ```

5. Run the bot:

    ```bash
    poetry run python -m openapitodiscord
    ```

## Usage

### Discord Commands

- ``/list_operations``: List available API operations.
- ``/call_api <api_route>``: Call a specific API route.
- ``/ping``: Check the bot latency.

## Configuration

You can configure the bot by modifying the .env file.
Make sure to provide the necessary environment variables for your Discord bot token and API base URL.

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
