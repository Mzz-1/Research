"""
Data integration pipeline for combining FakeNewsNet, CoAID, and TwiBot-22.

This module provides functions to integrate datasets and create unified
analysis-ready data with bot/human labels.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIntegrator:
    """Integrate multiple datasets into unified format."""

    def __init__(self, datasets: Dict[str, pd.DataFrame]):
        """
        Initialize DataIntegrator.

        Args:
            datasets: Dictionary of loaded datasets
        """
        self.datasets = datasets
        self.integrated_data = None

    def extract_user_ids(self, df: pd.DataFrame, user_id_col: str = 'user_id') -> set:
        """
        Extract unique user IDs from a dataset.

        Args:
            df: DataFrame containing user IDs
            user_id_col: Name of user ID column

        Returns:
            Set of unique user IDs
        """
        if user_id_col not in df.columns:
            logger.warning(f"Column {user_id_col} not found in dataset")
            return set()

        return set(df[user_id_col].dropna().unique())

    def match_users_to_labels(self, user_ids: List[str],
                               bot_labels: pd.DataFrame) -> pd.DataFrame:
        """
        Match user IDs to bot/human labels.

        Args:
            user_ids: List of user IDs to label
            bot_labels: DataFrame with columns ['user_id', 'label']

        Returns:
            DataFrame with user IDs and matched labels
        """
        user_df = pd.DataFrame({'user_id': user_ids})

        # Merge with bot labels
        labeled_users = user_df.merge(
            bot_labels[['user_id', 'label']],
            on='user_id',
            how='left'
        )

        # Report matching statistics
        total_users = len(labeled_users)
        labeled_users_count = labeled_users['label'].notna().sum()
        match_rate = (labeled_users_count / total_users * 100) if total_users > 0 else 0

        logger.info(f"Matched {labeled_users_count}/{total_users} users ({match_rate:.2f}%)")

        return labeled_users

    def integrate_fakenewsnet_with_labels(self, fakenewsnet_df: pd.DataFrame,
                                          bot_labels: pd.DataFrame) -> pd.DataFrame:
        """
        Integrate FakeNewsNet data with bot labels.

        Args:
            fakenewsnet_df: FakeNewsNet DataFrame
            bot_labels: TwiBot-22 labels

        Returns:
            Integrated DataFrame
        """
        logger.info("Integrating FakeNewsNet with bot labels")

        # Assuming FakeNewsNet has user_id column
        if 'user_id' not in fakenewsnet_df.columns:
            logger.warning("user_id column not found in FakeNewsNet data")
            return fakenewsnet_df

        # Merge with bot labels
        integrated = fakenewsnet_df.merge(
            bot_labels[['user_id', 'label']].rename(columns={'label': 'bot_label'}),
            on='user_id',
            how='left'
        )

        # Add source identifier
        integrated['dataset_source'] = 'fakenewsnet'

        logger.info(f"Integrated dataset size: {len(integrated)}")
        return integrated

    def integrate_coaid_with_labels(self, coaid_df: pd.DataFrame,
                                    bot_labels: pd.DataFrame) -> pd.DataFrame:
        """
        Integrate CoAID data with bot labels.

        Args:
            coaid_df: CoAID DataFrame
            bot_labels: TwiBot-22 labels

        Returns:
            Integrated DataFrame
        """
        logger.info("Integrating CoAID with bot labels")

        # Similar to FakeNewsNet integration
        if 'user_id' not in coaid_df.columns:
            logger.warning("user_id column not found in CoAID data")
            return coaid_df

        integrated = coaid_df.merge(
            bot_labels[['user_id', 'label']].rename(columns={'label': 'bot_label'}),
            on='user_id',
            how='left'
        )

        integrated['dataset_source'] = 'coaid'

        logger.info(f"Integrated dataset size: {len(integrated)}")
        return integrated

    def create_unified_dataset(self) -> pd.DataFrame:
        """
        Create unified dataset from all sources.

        Returns:
            Unified DataFrame with standardized schema
        """
        logger.info("Creating unified dataset")

        unified_records = []

        # Extract bot labels
        bot_labels = self.datasets.get('twibot22_labels', pd.DataFrame())

        if bot_labels.empty:
            logger.warning("Bot labels not available")
            return pd.DataFrame()

        # Integrate FakeNewsNet datasets
        for source in ['politifact', 'gossipcop']:
            key = f'fakenewsnet_{source}'
            if key in self.datasets and not self.datasets[key].empty:
                integrated = self.integrate_fakenewsnet_with_labels(
                    self.datasets[key], bot_labels
                )
                unified_records.append(integrated)

        # Integrate CoAID datasets
        for component in ['news', 'claims', 'tweets']:
            key = f'coaid_{component}'
            if key in self.datasets and not self.datasets[key].empty:
                integrated = self.integrate_coaid_with_labels(
                    self.datasets[key], bot_labels
                )
                unified_records.append(integrated)

        # Combine all datasets
        if unified_records:
            unified_df = pd.concat(unified_records, ignore_index=True)
            logger.info(f"Created unified dataset with {len(unified_df)} records")

            # Standardize schema
            unified_df = self._standardize_schema(unified_df)

            self.integrated_data = unified_df
            return unified_df
        else:
            logger.warning("No datasets to integrate")
            return pd.DataFrame()

    def _standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names and types.

        Args:
            df: Input DataFrame

        Returns:
            Standardized DataFrame
        """
        # Define standard columns
        standard_columns = {
            'post_id': 'str',
            'user_id': 'str',
            'text': 'str',
            'timestamp': 'datetime64[ns]',
            'label': 'str',  # fake/real label
            'bot_label': 'str',  # bot/human label
            'dataset_source': 'str'
        }

        # Ensure required columns exist
        for col, dtype in standard_columns.items():
            if col not in df.columns:
                df[col] = np.nan

        # Convert data types
        for col, dtype in standard_columns.items():
            if col in df.columns:
                try:
                    if dtype == 'datetime64[ns]' and col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif dtype == 'str':
                        df[col] = df[col].astype(str).replace('nan', np.nan)
                except Exception as e:
                    logger.warning(f"Error converting {col} to {dtype}: {e}")

        return df

    def get_statistics(self) -> Dict:
        """
        Get statistics about the integrated dataset.

        Returns:
            Dictionary of statistics
        """
        if self.integrated_data is None or self.integrated_data.empty:
            return {}

        df = self.integrated_data

        stats = {
            'total_records': len(df),
            'unique_users': df['user_id'].nunique(),
            'bot_labeled_records': df['bot_label'].notna().sum(),
            'bot_count': (df['bot_label'] == 'bot').sum(),
            'human_count': (df['bot_label'] == 'human').sum(),
            'fake_news_count': (df['label'] == 'fake').sum(),
            'real_news_count': (df['label'] == 'real').sum(),
            'datasets_included': df['dataset_source'].unique().tolist(),
            'temporal_coverage': {
                'start': df['timestamp'].min(),
                'end': df['timestamp'].max()
            } if 'timestamp' in df.columns else None
        }

        return stats

    def save_integrated_data(self, output_path: str):
        """
        Save integrated dataset to file.

        Args:
            output_path: Path to save the integrated data
        """
        if self.integrated_data is None or self.integrated_data.empty:
            logger.warning("No integrated data to save")
            return

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as parquet for efficiency
        if output_path.suffix == '.parquet':
            self.integrated_data.to_parquet(output_path, index=False)
        else:
            self.integrated_data.to_csv(output_path, index=False)

        logger.info(f"Saved integrated data to {output_path}")


if __name__ == '__main__':
    # Example usage
    from load_data import DataLoader

    # Load data
    loader = DataLoader('../data')
    datasets = loader.load_all()

    # Integrate
    integrator = DataIntegrator(datasets)
    unified_df = integrator.create_unified_dataset()

    # Get statistics
    stats = integrator.get_statistics()
    print("\nIntegration Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Save
    integrator.save_integrated_data('../data/processed/integrated_dataset.parquet')
