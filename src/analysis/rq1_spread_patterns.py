"""
RQ1: Analysis of spread pattern differences between bot and human misinformation.

This module analyzes:
- Speed of spread (temporal dynamics)
- Audience reach and size
- Network structure of propagation
- Cascading patterns and virality metrics
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.metrics import (
    calculate_spread_velocity,
    calculate_cascade_metrics,
    compare_spread_patterns,
    calculate_reach_metrics
)
from utils.visualization import (
    plot_spread_comparison,
    plot_cascade_size_distribution,
    plot_temporal_patterns
)


class RQ1Analyzer:
    """Analyzer for RQ1: Spread pattern differences."""

    def __init__(self, integrated_data: pd.DataFrame):
        """
        Initialize RQ1 Analyzer.

        Args:
            integrated_data: Integrated dataset with bot/human labels
        """
        self.data = integrated_data
        self.results = {}

    def separate_cascades(self, cascade_col: str = 'cascade_id') -> Tuple[List, List]:
        """
        Separate cascades into bot-initiated and human-initiated.

        Args:
            cascade_col: Column name for cascade IDs

        Returns:
            Tuple of (bot_cascades, human_cascades)
        """
        # Get first post in each cascade to determine initiator
        cascade_initiators = self.data.groupby(cascade_col).first()

        bot_cascade_ids = cascade_initiators[
            cascade_initiators['bot_label'] == 'bot'
        ].index.tolist()

        human_cascade_ids = cascade_initiators[
            cascade_initiators['bot_label'] == 'human'
        ].index.tolist()

        # Extract cascades
        bot_cascades = [
            self.data[self.data[cascade_col] == cid]
            for cid in bot_cascade_ids
        ]

        human_cascades = [
            self.data[self.data[cascade_col] == cid]
            for cid in human_cascade_ids
        ]

        print(f"Found {len(bot_cascades)} bot-initiated cascades")
        print(f"Found {len(human_cascades)} human-initiated cascades")

        return bot_cascades, human_cascades

    def analyze_spread_speed(self, bot_cascades: List, human_cascades: List) -> Dict:
        """
        Analyze spread speed differences.

        Args:
            bot_cascades: List of bot-initiated cascade DataFrames
            human_cascades: List of human-initiated cascade DataFrames

        Returns:
            Dictionary of speed metrics
        """
        print("Analyzing spread speed...")

        bot_velocities = [
            calculate_spread_velocity(cascade)
            for cascade in bot_cascades
        ]

        human_velocities = [
            calculate_spread_velocity(cascade)
            for cascade in human_cascades
        ]

        speed_metrics = {
            'bot_avg_velocity': np.mean(bot_velocities) if bot_velocities else 0,
            'bot_median_velocity': np.median(bot_velocities) if bot_velocities else 0,
            'human_avg_velocity': np.mean(human_velocities) if human_velocities else 0,
            'human_median_velocity': np.median(human_velocities) if human_velocities else 0,
            'velocity_ratio': (np.mean(bot_velocities) / np.mean(human_velocities)
                             if human_velocities and np.mean(human_velocities) > 0 else 0)
        }

        print(f"Bot average velocity: {speed_metrics['bot_avg_velocity']:.2f} users/hour")
        print(f"Human average velocity: {speed_metrics['human_avg_velocity']:.2f} users/hour")

        return speed_metrics

    def analyze_reach(self, bot_cascades: List, human_cascades: List) -> Dict:
        """
        Analyze audience reach differences.

        Args:
            bot_cascades: List of bot-initiated cascade DataFrames
            human_cascades: List of human-initiated cascade DataFrames

        Returns:
            Dictionary of reach metrics
        """
        print("Analyzing audience reach...")

        bot_sizes = [len(cascade) for cascade in bot_cascades]
        human_sizes = [len(cascade) for cascade in human_cascades]

        reach_metrics = {
            'bot_avg_size': np.mean(bot_sizes) if bot_sizes else 0,
            'bot_median_size': np.median(bot_sizes) if bot_sizes else 0,
            'bot_max_size': max(bot_sizes) if bot_sizes else 0,
            'human_avg_size': np.mean(human_sizes) if human_sizes else 0,
            'human_median_size': np.median(human_sizes) if human_sizes else 0,
            'human_max_size': max(human_sizes) if human_sizes else 0,
            'size_ratio': (np.mean(bot_sizes) / np.mean(human_sizes)
                          if human_sizes and np.mean(human_sizes) > 0 else 0)
        }

        print(f"Bot average cascade size: {reach_metrics['bot_avg_size']:.2f}")
        print(f"Human average cascade size: {reach_metrics['human_avg_size']:.2f}")

        return reach_metrics

    def analyze_temporal_patterns(self) -> Dict:
        """
        Analyze temporal patterns of spread.

        Returns:
            Dictionary of temporal metrics
        """
        print("Analyzing temporal patterns...")

        if 'timestamp' not in self.data.columns:
            print("Warning: No timestamp column found")
            return {}

        # Separate by bot/human
        bot_data = self.data[self.data['bot_label'] == 'bot']
        human_data = self.data[self.data['bot_label'] == 'human']

        # Calculate posting patterns by hour of day
        bot_data['hour'] = pd.to_datetime(bot_data['timestamp']).dt.hour
        human_data['hour'] = pd.to_datetime(human_data['timestamp']).dt.hour

        bot_hourly = bot_data['hour'].value_counts().sort_index()
        human_hourly = human_data['hour'].value_counts().sort_index()

        temporal_metrics = {
            'bot_peak_hour': bot_hourly.idxmax() if not bot_hourly.empty else None,
            'human_peak_hour': human_hourly.idxmax() if not human_hourly.empty else None,
            'bot_hourly_std': bot_hourly.std() if not bot_hourly.empty else 0,
            'human_hourly_std': human_hourly.std() if not human_hourly.empty else 0
        }

        return temporal_metrics

    def run_full_analysis(self, save_dir: str = '../results') -> Dict:
        """
        Run complete RQ1 analysis.

        Args:
            save_dir: Directory to save results

        Returns:
            Dictionary of all analysis results
        """
        print("="*60)
        print("RQ1: Spread Pattern Analysis")
        print("="*60)

        # Separate cascades
        bot_cascades, human_cascades = self.separate_cascades()

        # Analyze speed
        speed_metrics = self.analyze_spread_speed(bot_cascades, human_cascades)
        self.results['speed'] = speed_metrics

        # Analyze reach
        reach_metrics = self.analyze_reach(bot_cascades, human_cascades)
        self.results['reach'] = reach_metrics

        # Analyze temporal patterns
        temporal_metrics = self.analyze_temporal_patterns()
        self.results['temporal'] = temporal_metrics

        # Comparative analysis
        comparison = compare_spread_patterns(bot_cascades, human_cascades)
        self.results['comparison'] = comparison

        # Generate visualizations
        save_path = Path(save_dir) / 'figures'
        save_path.mkdir(parents=True, exist_ok=True)

        bot_data = self.data[self.data['bot_label'] == 'bot']
        human_data = self.data[self.data['bot_label'] == 'human']

        # Temporal comparison
        if 'timestamp' in self.data.columns:
            plot_spread_comparison(
                bot_data, human_data,
                save_path=str(save_path / 'rq1_temporal_comparison.png')
            )

        # Size distribution
        bot_sizes = [len(cascade) for cascade in bot_cascades]
        human_sizes = [len(cascade) for cascade in human_cascades]

        plot_cascade_size_distribution(
            bot_sizes, human_sizes,
            save_path=str(save_path / 'rq1_size_distribution.png')
        )

        print("\nRQ1 Analysis Complete!")
        print("="*60)

        return self.results


if __name__ == '__main__':
    # Example usage
    print("RQ1 Analyzer module loaded")
