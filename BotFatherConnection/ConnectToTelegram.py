import telebot


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def start_command(self, message):
        self.bot.send_message(message.chat.id, "Hello! I'm your bot. Type /help for commands.")

    def help_command(self, message):
        self.bot.send_message(message.chat.id, "This is a simple bot. You can type /start or /help.")

    def run(self):
        # Register handlers
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start_command(message)

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.help_command(message)

        # Start the bot
        self.bot.polling(none_stop=True)
