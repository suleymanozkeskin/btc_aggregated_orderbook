# orderbook/utils/ob.py
from typing import Optional, Dict
import logging
import pandas as pd
from exchange_books.bybit_orderbook import Bybit
from exchange_books.coinbase_orderbook import Coinbase
from exchange_books.okex_orderbook import OKEx
from exchange_books.binance_orderbook import Binance

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize exchange objects
bybit = Bybit('Bybit', 'https://api.bybit.com/')
coinbase = Coinbase('Coinbase', 'https://api.pro.coinbase.com/')
okex = OKEx('OKEx', 'https://www.okex.com/')
binance = Binance('Binance', 'https://api.binance.com/')

def process_orderbook(raw_ob: pd.DataFrame, exchange_name: str) -> Dict[str, pd.DataFrame]:
    """
    Process orderbook DataFrame into standardized bid/ask DataFrames
    """
    try:
        # Convert price and size to numeric
        raw_ob['Price'] = pd.to_numeric(raw_ob['Price'], errors='coerce')
        raw_ob['Size'] = pd.to_numeric(raw_ob['Size'], errors='coerce')
        
        # Split into bids and asks
        bids_df = raw_ob[raw_ob['Side'] == 'buy'].copy()
        asks_df = raw_ob[raw_ob['Side'] == 'sell'].copy()
        
        # Rename columns to standardized format
        column_mapping = {
            'Price': 'price',
            'Size': 'size'
        }
        bids_df = bids_df.rename(columns=column_mapping)
        asks_df = asks_df.rename(columns=column_mapping)
        
        # Add exchange column
        bids_df['exchange'] = exchange_name
        asks_df['exchange'] = exchange_name
        
        # Select and order columns
        columns = ['price', 'size', 'exchange']
        
        return {
            'bids': bids_df[columns],
            'asks': asks_df[columns]
        }
    except Exception as e:
        logger.error(f"Error processing {exchange_name} orderbook: {str(e)}")
        logger.warning(f"\nRaw orderbook data: {raw_ob}\n")
        return None

def fetch_orderbook_safely(exchange_instance, exchange_name: str) -> Optional[Dict]:
    """
    Safely fetch orderbook from an exchange instance, returning None if failed.
    """
    try:
        raw_ob = exchange_instance.fetch_orderbook()
        if isinstance(raw_ob, pd.DataFrame):
            processed_ob = process_orderbook(raw_ob, exchange_name)
        else:
            logger.error(f"Unexpected orderbook format from {exchange_name}: {type(raw_ob)}")
            return None
        return processed_ob
    except Exception as e:
        logger.warning(f"Failed to fetch {exchange_name} orderbook: {str(e)}")
        return None

def get_available_orderbooks() -> Dict[str, Optional[Dict[str, pd.DataFrame]]]:
    """
    Fetch all available orderbooks and return them in a dictionary.
    """
    orderbooks = {
        # 'Coinbase': fetch_orderbook_safely(coinbase, 'Coinbase'), # TODO: Fix Coinbase and uncomment
        'Binance': fetch_orderbook_safely(binance, 'Binance'),
        'Bybit': fetch_orderbook_safely(bybit, 'Bybit'),
        # 'OKEx': fetch_orderbook_safely(okex, 'OKEx'), # TODO: Fix OKEx and uncomment
    }
    
    # Count and log available/unavailable exchanges
    available = sum(1 for ob in orderbooks.values() if ob is not None)
    total = len(orderbooks)
    
    if available < total:
        logger.warning(
            f"Running with reduced market coverage: {available}/{total} exchanges available"
        )
    
    logger.info(f"Available orderbooks: {orderbooks}")
    return orderbooks

def aggregate_orderbooks(orderbooks: Dict[str, Optional[Dict[str, pd.DataFrame]]]):
    """
    Aggregate available orderbooks, skipping any that are None
    Returns concatenated bids and asks DataFrames
    """
    available_obs = {
        name: ob for name, ob in orderbooks.items() 
        if ob is not None
    }
    
    if not available_obs:
        raise RuntimeError("No orderbook data available from any exchange")
    
    # Concatenate all bids and asks
    all_bids = pd.concat([ob['bids'] for ob in available_obs.values()], ignore_index=True)
    all_asks = pd.concat([ob['asks'] for ob in available_obs.values()], ignore_index=True)
    
    # Sort bids descending (highest price first) and asks ascending (lowest price first)
    all_bids = all_bids.sort_values('price', ascending=False)
    all_asks = all_asks.sort_values('price', ascending=True)
    
    return {
        'bids': all_bids,
        'asks': all_asks
    }