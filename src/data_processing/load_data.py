"""
Data loading utilities for TruthSeeker dataset components.

This module provides functions to load data from FakeNewsNet, CoAID,
and TwiBot-22 datasets.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and parse TruthSeeker dataset components."""

    def __init__(self, data_dir: str = '../data'):
        """
        Initialize DataLoader.

        Args:
            data_dir: Path to data directory
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / 'raw'
        self.external_dir = self.data_dir / 'external'

    def load_fakenewsnet(self, source: str = 'politifact') -> pd.DataFrame:
        """
        Load FakeNewsNet data.

        Args:
            source: Either 'politifact' or 'gossipcop'

        Returns:
            DataFrame with news articles and labels
        """
        fakenewsnet_path = self.external_dir / 'FakeNewsNet' / source

        if not fakenewsnet_path.exists():
            logger.warning(f"FakeNewsNet {source} directory not found at {fakenewsnet_path}")
            return pd.DataFrame()

        logger.info(f"Loading FakeNewsNet data from {source}")

        # TODO: Implement actual loading logic based on FakeNewsNet structure
        # This is a placeholder that should be updated once the actual data structure is known

        try:
            # Example structure - update based on actual data
            fake_dir = fakenewsnet_path / 'fake'
            real_dir = fakenewsnet_path / 'real'

            data_records = []

            # Load fake news
            if fake_dir.exists():
                for news_file in fake_dir.glob('*.json'):
                    with open(news_file, 'r') as f:
                        news_data = json.load(f)
                        news_data['label'] = 'fake'
                        news_data['source'] = source
                        data_records.append(news_data)

            # Load real news
            if real_dir.exists():
                for news_file in real_dir.glob('*.json'):
                    with open(news_file, 'r') as f:
                        news_data = json.load(f)
                        news_data['label'] = 'real'
                        news_data['source'] = source
                        data_records.append(news_data)

            df = pd.DataFrame(data_records)
            logger.info(f"Loaded {len(df)} news articles from {source}")
            return df

        except Exception as e:
            logger.error(f"Error loading FakeNewsNet data: {e}")
            return pd.DataFrame()

    def load_coaid(self) -> Dict[str, pd.DataFrame]:
        """
        Load CoAID dataset.

        Returns:
            Dictionary of DataFrames for different CoAID components
        """
        coaid_path = self.external_dir / 'CoAID'

        if not coaid_path.exists():
            logger.warning(f"CoAID directory not found at {coaid_path}")
            return {}

        logger.info("Loading CoAID data")

        data = {}

        try:
            # TODO: Update based on actual CoAID structure
            # Example components
            components = ['news', 'claims', 'tweets']

            for component in components:
                component_file = coaid_path / f'{component}.csv'
                if component_file.exists():
                    data[component] = pd.read_csv(component_file)
                    logger.info(f"Loaded {len(data[component])} {component} records")

            return data

        except Exception as e:
            logger.error(f"Error loading CoAID data: {e}")
            return {}

    def load_twibot22(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load TwiBot-22 dataset.

        Returns:
            Tuple of (user_data, labels)
        """
        twibot_path = self.external_dir / 'TwiBot-22'

        if not twibot_path.exists():
            logger.warning(f"TwiBot-22 directory not found at {twibot_path}")
            return pd.DataFrame(), pd.DataFrame()

        logger.info("Loading TwiBot-22 data")

        try:
            # Load user data
            user_file = twibot_path / 'user.json'
            if user_file.exists():
                users = pd.read_json(user_file, lines=True)
            else:
                logger.warning("User data file not found")
                users = pd.DataFrame()

            # Load labels
            label_file = twibot_path / 'label.csv'
            if label_file.exists():
                labels = pd.read_csv(label_file)
            else:
                logger.warning("Label file not found")
                labels = pd.DataFrame()

            logger.info(f"Loaded {len(users)} users and {len(labels)} labels")
            return users, labels

        except Exception as e:
            logger.error(f"Error loading TwiBot-22 data: {e}")
            return pd.DataFrame(), pd.DataFrame()

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """
        Load all dataset components.

        Returns:
            Dictionary containing all loaded datasets
        """
        logger.info("Loading all datasets")

        datasets = {}

        # Load FakeNewsNet
        datasets['fakenewsnet_politifact'] = self.load_fakenewsnet('politifact')
        datasets['fakenewsnet_gossipcop'] = self.load_fakenewsnet('gossipcop')

        # Load CoAID
        coaid_data = self.load_coaid()
        for key, df in coaid_data.items():
            datasets[f'coaid_{key}'] = df

        # Load TwiBot-22
        users, labels = self.load_twibot22()
        datasets['twibot22_users'] = users
        datasets['twibot22_labels'] = labels

        # Summary
        logger.info("\nDataset loading summary:")
        for name, df in datasets.items():
            logger.info(f"  {name}: {len(df)} records")

        return datasets


def load_tweets_from_fakenewsnet(news_id: str, source: str = 'politifact',
                                  data_dir: str = '../data/external') -> pd.DataFrame:
    """
    Load tweets associated with a specific news article from FakeNewsNet.

    Args:
        news_id: News article ID
        source: Either 'politifact' or 'gossipcop'
        data_dir: Path to data directory

    Returns:
        DataFrame of tweets
    """
    tweet_dir = Path(data_dir) / 'FakeNewsNet' / source / 'tweets' / news_id

    if not tweet_dir.exists():
        logger.warning(f"Tweet directory not found: {tweet_dir}")
        return pd.DataFrame()

    tweets = []
    for tweet_file in tweet_dir.glob('*.json'):
        try:
            with open(tweet_file, 'r') as f:
                tweet_data = json.load(f)
                tweets.append(tweet_data)
        except Exception as e:
            logger.error(f"Error loading tweet {tweet_file}: {e}")

    return pd.DataFrame(tweets)


if __name__ == '__main__':
    # Test data loading
    loader = DataLoader('../data')
    datasets = loader.load_all()

    print("\nLoaded datasets:")
    for name, df in datasets.items():
        print(f"{name}: {len(df)} records")
