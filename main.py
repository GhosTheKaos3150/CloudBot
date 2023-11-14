from dotenv import load_dotenv

import logging

from telegram_bot.bot import main

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == "__main__":
    load_dotenv()
    
    main()