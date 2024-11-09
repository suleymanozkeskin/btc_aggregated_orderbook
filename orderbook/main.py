import pandas as pd
from utils.ob import get_available_orderbooks, aggregate_orderbooks
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def main():
    try:
        # Fetch all available orderbooks
        orderbooks = get_available_orderbooks()
        
        # Aggregate the available orderbooks
        aggregated_data = aggregate_orderbooks(orderbooks)
        
        # aggregated_data['bids'] and aggregated_data['asks']
        # as sorted pandas DataFrames with price, size, and exchange columns
        print(f"Aggregated {len(aggregated_data['bids'])} bids and {len(aggregated_data['asks'])} asks")
        
        # Save the aggregated orderbook to a csv file
        aggregated_data['bids'].to_csv('aggregated_bids.csv', index=False)
        aggregated_data['asks'].to_csv('aggregated_asks.csv', index=False)
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()