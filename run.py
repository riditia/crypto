import yaml
import os
from dotenv import load_dotenv
from app.logger_config import setup_logger
from app.api_client import CoinSwitchAPIClient
from app.data_handler import get_historical_data

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
    api_secret = os.getenv('COINSWITCH_API_SECRET')

    # Setup main application logger
    main_logger = setup_logger('main_app', 'main')

    main_logger.info("Application starting...")
    main_logger.info(f"Loaded {len(config['assets'])} assets from config.")

    if api_key and api_secret:
        main_logger.info("Successfully loaded API credentials.")

        # Initialize the API client
        api_client = CoinSwitchAPIClient(api_key, api_secret)

        # --- Test Data Handler ---
        main_logger.info("Fetching historical data for BTC/INR...")
        historical_data = get_historical_data(api_client, 'BTC/INR', 30, days_history=7)

        if historical_data is not None:
            if not historical_data.empty:
                main_logger.info(f"Successfully fetched {len(historical_data)} rows of data.")
                main_logger.info("First 5 rows of data:\n" + historical_data.head().to_string())
            else:
                main_logger.info("No historical data was returned for the given period.")
        else:
            main_logger.error("Failed to fetch historical data.")
        # --- End Test ---

    else:
        main_logger.error("Could not load API credentials. Check your .env file.")

    main_logger.info("Application finished.")

if __name__ == "__main__":
    main()
