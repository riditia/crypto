import yaml
import os
from dotenv import load_dotenv
from app.logger_config import setup_logger

def main():
    """
    Main function to run the trading bot.
    """
    # Load configuration from config.yml
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv('COINSWITCH_API_KEY')

    # Setup main application logger
    main_logger = setup_logger('main_app', 'main')

    main_logger.info("Application starting...")
    main_logger.info(f"Loaded {len(config['assets'])} assets from config.")

    if api_key:
        main_logger.info("Successfully loaded API key.")
    else:
        main_logger.error("Could not load API key. Check your .env file.")

    main_logger.info("Application finished.")

if __name__ == "__main__":
    main()
