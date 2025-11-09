"""
Visualization utilities for TruthSeeker research project.

This module provides functions to create visualizations for analyzing
misinformation spread patterns, bot detection, and comparative analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import networkx as nx
from typing import List, Dict, Optional, Tuple
from matplotlib.patches import Patch


def plot_spread_comparison(bot_data: pd.DataFrame,
                           human_data: pd.DataFrame,
                           metric: str = 'cumulative_users',
                           time_col: str = 'timestamp',
                           save_path: Optional[str] = None):
    """
    Plot temporal spread comparison between bot and human cascades.

    Args:
        bot_data: DataFrame with bot cascade data
        human_data: DataFrame with human cascade data
        metric: Metric to plot
        time_col: Name of timestamp column
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot bot cascades
    if not bot_data.empty:
        bot_data_sorted = bot_data.sort_values(time_col)
        bot_data_sorted['cumulative'] = range(1, len(bot_data_sorted) + 1)
        ax.plot(bot_data_sorted[time_col], bot_data_sorted['cumulative'],
                label='Bot-initiated', color='#e74c3c', linewidth=2, alpha=0.8)

    # Plot human cascades
    if not human_data.empty:
        human_data_sorted = human_data.sort_values(time_col)
        human_data_sorted['cumulative'] = range(1, len(human_data_sorted) + 1)
        ax.plot(human_data_sorted[time_col], human_data_sorted['cumulative'],
                label='Human-initiated', color='#3498db', linewidth=2, alpha=0.8)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Cumulative Users Reached', fontsize=12)
    ax.set_title('Misinformation Spread: Bot vs Human Cascades', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_cascade_size_distribution(bot_sizes: List[int],
                                   human_sizes: List[int],
                                   save_path: Optional[str] = None):
    """
    Plot distribution of cascade sizes for bot vs human.

    Args:
        bot_sizes: List of cascade sizes for bot-initiated cascades
        human_sizes: List of cascade sizes for human-initiated cascades
        save_path: Optional path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Violin plot
    data_for_violin = []
    labels = []
    if bot_sizes:
        data_for_violin.extend(bot_sizes)
        labels.extend(['Bot'] * len(bot_sizes))
    if human_sizes:
        data_for_violin.extend(human_sizes)
        labels.extend(['Human'] * len(human_sizes))

    df_plot = pd.DataFrame({'Cascade Size': data_for_violin, 'Type': labels})

    sns.violinplot(data=df_plot, x='Type', y='Cascade Size', ax=axes[0],
                   palette={'Bot': '#e74c3c', 'Human': '#3498db'})
    axes[0].set_title('Cascade Size Distribution', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Cascade Size (users)', fontsize=11)

    # Box plot (log scale)
    sns.boxplot(data=df_plot, x='Type', y='Cascade Size', ax=axes[1],
                palette={'Bot': '#e74c3c', 'Human': '#3498db'})
    axes[1].set_yscale('log')
    axes[1].set_title('Cascade Size Distribution (Log Scale)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Cascade Size (log scale)', fontsize=11)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_temporal_patterns(df: pd.DataFrame,
                          time_col: str = 'timestamp',
                          bot_label_col: str = 'bot_label',
                          window: str = '1H',
                          save_path: Optional[str] = None):
    """
    Plot temporal posting patterns for bots vs humans.

    Args:
        df: DataFrame with timestamps and bot labels
        time_col: Name of timestamp column
        bot_label_col: Name of bot label column
        window: Time window for aggregation (e.g., '1H', '1D')
        save_path: Optional path to save figure
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])

    fig, ax = plt.subplots(figsize=(14, 6))

    # Separate bot and human data
    bot_df = df[df[bot_label_col] == 'bot']
    human_df = df[df[bot_label_col] == 'human']

    # Resample by time window
    bot_counts = bot_df.set_index(time_col).resample(window).size()
    human_counts = human_df.set_index(time_col).resample(window).size()

    # Plot
    ax.plot(bot_counts.index, bot_counts.values, label='Bot Posts',
            color='#e74c3c', linewidth=2, alpha=0.7)
    ax.plot(human_counts.index, human_counts.values, label='Human Posts',
            color='#3498db', linewidth=2, alpha=0.7)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Number of Posts', fontsize=12)
    ax.set_title(f'Temporal Posting Patterns (Window: {window})', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_network_structure(network: nx.Graph,
                           node_labels: Optional[Dict] = None,
                           node_colors: Optional[Dict] = None,
                           layout: str = 'spring',
                           save_path: Optional[str] = None):
    """
    Visualize cascade network structure.

    Args:
        network: NetworkX graph
        node_labels: Optional dictionary of node labels
        node_colors: Optional dictionary mapping nodes to colors
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Choose layout
    if layout == 'spring':
        pos = nx.spring_layout(network, k=0.5, iterations=50)
    elif layout == 'circular':
        pos = nx.circular_layout(network)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(network)
    else:
        pos = nx.spring_layout(network)

    # Node colors
    if node_colors:
        colors = [node_colors.get(node, '#95a5a6') for node in network.nodes()]
    else:
        colors = '#3498db'

    # Draw network
    nx.draw_networkx_nodes(network, pos, node_color=colors, node_size=300,
                          alpha=0.7, ax=ax)
    nx.draw_networkx_edges(network, pos, alpha=0.3, arrows=True,
                          arrowsize=10, ax=ax)

    if node_labels:
        nx.draw_networkx_labels(network, pos, labels=node_labels,
                               font_size=8, ax=ax)

    ax.set_title('Misinformation Cascade Network', fontsize=14, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_attribution_analysis(attribution_data: Dict,
                              save_path: Optional[str] = None):
    """
    Plot bot attribution analysis results.

    Args:
        attribution_data: Dictionary with attribution metrics
        save_path: Optional path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Post-level attribution
    labels = ['Bot Posts', 'Human Posts']
    sizes = [attribution_data.get('bot_posts', 0),
             attribution_data.get('human_posts', 0)]
    colors = ['#e74c3c', '#3498db']

    axes[0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 11})
    axes[0].set_title('Post-Level Attribution', fontsize=12, fontweight='bold')

    # Cascade-level attribution
    labels = ['Bot-Initiated', 'Human-Initiated']
    sizes = [attribution_data.get('bot_initiated_cascades', 0),
             attribution_data.get('human_initiated_cascades', 0)]

    axes[1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 11})
    axes[1].set_title('Cascade-Level Attribution', fontsize=12, fontweight='bold')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_feature_importance(feature_names: List[str],
                           importance_scores: List[float],
                           top_n: int = 20,
                           save_path: Optional[str] = None):
    """
    Plot feature importance for bot detection model.

    Args:
        feature_names: List of feature names
        importance_scores: List of importance scores
        top_n: Number of top features to show
        save_path: Optional path to save figure
    """
    # Create DataFrame and sort
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance_scores
    }).sort_values('Importance', ascending=False).head(top_n)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))

    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(importance_df)))

    ax.barh(range(len(importance_df)), importance_df['Importance'], color=colors)
    ax.set_yticks(range(len(importance_df)))
    ax.set_yticklabels(importance_df['Feature'])
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_title(f'Top {top_n} Feature Importance for Bot Detection',
                fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def plot_intervention_impact(intervention_results: Dict[str, float],
                            save_path: Optional[str] = None):
    """
    Plot impact of different intervention strategies.

    Args:
        intervention_results: Dictionary mapping intervention names to impact scores
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    interventions = list(intervention_results.keys())
    impacts = list(intervention_results.values())

    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in impacts]

    bars = ax.bar(range(len(interventions)), impacts, color=colors, alpha=0.7)

    ax.set_xticks(range(len(interventions)))
    ax.set_xticklabels(interventions, rotation=45, ha='right')
    ax.set_ylabel('Impact Score', fontsize=12)
    ax.set_title('Intervention Strategy Impact Analysis', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


if __name__ == '__main__':
    print("Visualization module loaded successfully")
