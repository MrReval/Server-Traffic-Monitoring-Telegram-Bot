# Server Traffic Monitoring Telegram Bot

![Logo](./readme.svg)

This is a small Telegram bot designed to provide server traffic usage reports.

## Features

Using this bot, you can:
- Monitor incoming, outgoing, and total traffic usage.
- Receive hourly traffic usage reports automatically.

## Installation and Usage

Running this bot is simple and requires minimal setup. Follow the steps below:

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**
   Make sure you have Python installed. Then, install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**
   Update the configuration file with your Telegram bot token and server details:
   - Open `bot.py` .
   - Add your bot token and ChatID.

4. **Run the Bot**
   Start the bot with:
   ```bash
   python bot.py
   ```
   OR
    ```bash
   nohup python bot.py &
   ```

5. **Monitor Reports**
   Once the bot is running, it will send hourly reports about your server’s traffic usage directly to your Telegram chat.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

