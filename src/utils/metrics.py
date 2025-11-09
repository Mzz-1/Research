"""
Metrics and evaluation utilities for analyzing misinformation spread.

This module provides functions to calculate various metrics related to
information spread, bot detection, and impact quantification.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import networkx as nx
from scipy import stats


def calculate_spread_velocity(cascade_df: pd.DataFrame,
                               time_col: str = 'timestamp',
                               window_hours: int = 24) -> float:
    """
    Calculate spread velocity (users reached per hour).

    Args:
        cascade_df: DataFrame with timestamps of spread events
        time_col: Name of timestamp column
        window_hours: Time window for velocity calculation

    Returns:
        Spread velocity (users/hour)
    """
    if cascade_df.empty or time_col not in cascade_df.columns:
        return 0.0

    cascade_df = cascade_df.sort_values(time_col)
    time_diff = (cascade_df[time_col].max() - cascade_df[time_col].min()).total_seconds() / 3600

    if time_diff == 0:
        return 0.0

    velocity = len(cascade_df) / time_diff
    return velocity


def calculate_cascade_metrics(cascade_df: pd.DataFrame,
                               network: Optional[nx.Graph] = None) -> Dict:
    """
    Calculate comprehensive cascade metrics.

    Args:
        cascade_df: DataFrame with cascade information
        network: Optional NetworkX graph

    Returns:
        Dictionary of cascade metrics
    """
    metrics = {
        'size': len(cascade_df),
        'unique_users': cascade_df['user_id'].nunique() if 'user_id' in cascade_df.columns else 0,
        'duration_hours': 0.0,
        'max_depth': 0,
        'structural_virality': 0.0
    }

    # Temporal metrics
    if 'timestamp' in cascade_df.columns:
        time_span = (cascade_df['timestamp'].max() - cascade_df['timestamp'].min())
        metrics['duration_hours'] = time_span.total_seconds() / 3600

    # Network metrics
    if network is not None:
        metrics['max_depth'] = calculate_cascade_depth(network)
        metrics['structural_virality'] = calculate_structural_virality(network)

    return metrics


def calculate_cascade_depth(network: nx.Graph, root_node: Optional[str] = None) -> int:
    """
    Calculate maximum depth of cascade tree.

    Args:
        network: NetworkX graph representing cascade
        root_node: Root node of cascade (if None, uses node with max degree)

    Returns:
        Maximum depth
    """
    if network.number_of_nodes() == 0:
        return 0

    # Find root if not specified
    if root_node is None:
        root_node = max(network.degree(), key=lambda x: x[1])[0]

    # Calculate shortest paths from root
    try:
        lengths = nx.single_source_shortest_path_length(network, root_node)
        return max(lengths.values()) if lengths else 0
    except:
        return 0


def calculate_structural_virality(network: nx.Graph) -> float:
    """
    Calculate structural virality (Goel et al., 2016).

    Structural virality measures the tree-like nature of cascades.
    Higher values indicate more viral, tree-like spreading.

    Args:
        network: NetworkX graph

    Returns:
        Structural virality score
    """
    if network.number_of_nodes() <= 1:
        return 0.0

    try:
        # Calculate average distance between all pairs of nodes
        n = network.number_of_nodes()
        total_distance = 0
        count = 0

        for node in network.nodes():
            lengths = nx.single_source_shortest_path_length(network, node)
            total_distance += sum(lengths.values())
            count += len(lengths)

        avg_distance = total_distance / count if count > 0 else 0
        return avg_distance
    except:
        return 0.0


def compare_spread_patterns(bot_cascades: List[pd.DataFrame],
                            human_cascades: List[pd.DataFrame]) -> Dict:
    """
    Compare spread patterns between bot and human cascades.

    Args:
        bot_cascades: List of DataFrames representing bot-initiated cascades
        human_cascades: List of DataFrames representing human-initiated cascades

    Returns:
        Dictionary of comparative statistics
    """
    # Calculate metrics for both groups
    bot_metrics = [calculate_cascade_metrics(c) for c in bot_cascades]
    human_metrics = [calculate_cascade_metrics(c) for c in human_cascades]

    # Extract specific metrics
    bot_sizes = [m['size'] for m in bot_metrics]
    human_sizes = [m['size'] for m in human_metrics]

    bot_velocities = [m['size'] / m['duration_hours'] if m['duration_hours'] > 0 else 0
                      for m in bot_metrics]
    human_velocities = [m['size'] / m['duration_hours'] if m['duration_hours'] > 0 else 0
                        for m in human_metrics]

    # Statistical comparison
    comparison = {
        'bot_avg_size': np.mean(bot_sizes) if bot_sizes else 0,
        'human_avg_size': np.mean(human_sizes) if human_sizes else 0,
        'bot_avg_velocity': np.mean(bot_velocities) if bot_velocities else 0,
        'human_avg_velocity': np.mean(human_velocities) if human_velocities else 0,
        'size_difference': np.mean(bot_sizes) - np.mean(human_sizes) if bot_sizes and human_sizes else 0,
        'velocity_difference': np.mean(bot_velocities) - np.mean(human_velocities) if bot_velocities and human_velocities else 0
    }

    # Statistical tests
    if len(bot_sizes) > 0 and len(human_sizes) > 0:
        # Mann-Whitney U test for size
        u_stat, p_val = stats.mannwhitneyu(bot_sizes, human_sizes, alternative='two-sided')
        comparison['size_pvalue'] = p_val

        # Mann-Whitney U test for velocity
        if len(bot_velocities) > 0 and len(human_velocities) > 0:
            u_stat, p_val = stats.mannwhitneyu(bot_velocities, human_velocities, alternative='two-sided')
            comparison['velocity_pvalue'] = p_val

    return comparison


def calculate_bot_attribution(df: pd.DataFrame, cascade_col: str = 'cascade_id') -> Dict:
    """
    Calculate proportion of misinformation attributable to bots.

    Args:
        df: DataFrame with bot labels and cascade information
        cascade_col: Column name for cascade IDs

    Returns:
        Dictionary of attribution metrics
    """
    if 'bot_label' not in df.columns:
        return {}

    # Overall statistics
    total_posts = len(df)
    bot_posts = (df['bot_label'] == 'bot').sum()
    human_posts = (df['bot_label'] == 'human').sum()

    # Cascade-level attribution
    cascade_initiators = df.groupby(cascade_col).first()
    bot_initiated = (cascade_initiators['bot_label'] == 'bot').sum()
    human_initiated = (cascade_initiators['bot_label'] == 'human').sum()

    attribution = {
        'total_posts': total_posts,
        'bot_posts': bot_posts,
        'human_posts': human_posts,
        'bot_post_percentage': (bot_posts / total_posts * 100) if total_posts > 0 else 0,
        'bot_initiated_cascades': bot_initiated,
        'human_initiated_cascades': human_initiated,
        'bot_initiation_percentage': (bot_initiated / (bot_initiated + human_initiated) * 100)
                                      if (bot_initiated + human_initiated) > 0 else 0
    }

    return attribution


def calculate_reach_metrics(df: pd.DataFrame, cascade_col: str = 'cascade_id') -> pd.DataFrame:
    """
    Calculate reach metrics for each cascade.

    Args:
        df: DataFrame with cascade information
        cascade_col: Column name for cascade IDs

    Returns:
        DataFrame with reach metrics per cascade
    """
    reach_metrics = df.groupby(cascade_col).agg({
        'user_id': 'nunique',
        'timestamp': lambda x: (x.max() - x.min()).total_seconds() / 3600 if len(x) > 1 else 0,
        'bot_label': lambda x: (x == 'bot').sum()
    }).rename(columns={
        'user_id': 'unique_users',
        'timestamp': 'duration_hours',
        'bot_label': 'bot_count'
    })

    reach_metrics['human_count'] = df.groupby(cascade_col).size() - reach_metrics['bot_count']
    reach_metrics['bot_ratio'] = reach_metrics['bot_count'] / (reach_metrics['bot_count'] + reach_metrics['human_count'])

    return reach_metrics


def calculate_network_centrality(network: nx.Graph, node_list: Optional[List] = None) -> pd.DataFrame:
    """
    Calculate centrality metrics for network nodes.

    Args:
        network: NetworkX graph
        node_list: Optional list of nodes to calculate (calculates for all if None)

    Returns:
        DataFrame with centrality metrics
    """
    nodes = node_list if node_list is not None else list(network.nodes())

    centrality_metrics = pd.DataFrame(index=nodes)

    # Degree centrality
    degree_cent = nx.degree_centrality(network)
    centrality_metrics['degree_centrality'] = [degree_cent.get(node, 0) for node in nodes]

    # Betweenness centrality
    between_cent = nx.betweenness_centrality(network)
    centrality_metrics['betweenness_centrality'] = [between_cent.get(node, 0) for node in nodes]

    # Closeness centrality (if graph is connected)
    if nx.is_connected(network):
        close_cent = nx.closeness_centrality(network)
        centrality_metrics['closeness_centrality'] = [close_cent.get(node, 0) for node in nodes]

    # PageRank
    pagerank = nx.pagerank(network)
    centrality_metrics['pagerank'] = [pagerank.get(node, 0) for node in nodes]

    return centrality_metrics


if __name__ == '__main__':
    # Example usage
    print("Metrics module loaded successfully")
