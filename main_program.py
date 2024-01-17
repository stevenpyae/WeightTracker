from BotFatherConnection import ConnectToTelegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.environ.get('BOT_TOKEN')
    bot = ConnectToTelegram.Bot(bot_token)
    bot.run()


if __name__ == "__main__":
    main()
