import matplotlib.pyplot as plt
import os
from typing import List, Dict, Tuple
import seaborn as sns
from datetime import datetime
import numpy as np

def ensure_plots_dir():
    if not os.path.exists('plots'):
        os.makedirs('plots')

def plot_router_performance_by_type(
    router_data: Dict[str, List[float]], 
    timestamp: str
) -> None:
    ensure_plots_dir()
    
    router_names = list(router_data.keys())
    times = list(router_data.values())
    
    plt.figure(figsize=(12, 6))
    plt.boxplot(times, labels=router_names)
    plt.title('Router Types - Processing Time Distribution')
    plt.ylabel('Time (seconds)')
    plt.xlabel('Router Type')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'plots/router_types_performance_{timestamp}.png')
    plt.close()

def plot_router_types_accuracy(
    router_results: Dict[str, 'RouterResult'],
    timestamp: str
) -> None:
    ensure_plots_dir()
    
    router_types = list(router_results.keys())
    metrics = {
        'Passed': [results.passed for results in router_results.values()],
        'Failed': [results.failed for results in router_results.values()],
        'Warnings': [results.warnings for results in router_results.values()]
    }
    
    x = np.arange(len(router_types))
    width = 0.25
    multiplier = 0
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for metric, values in metrics.items():
        offset = width * multiplier
        ax.bar(x + offset, values, width, label=metric)
        multiplier += 1
    
    ax.set_xlabel('Router Type')
    ax.set_ylabel('Count')
    ax.set_title('Accuracy Metrics by Router Type')
    ax.set_xticks(x + width)
    ax.set_xticklabels(router_types, rotation=45)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'plots/router_types_accuracy_{timestamp}.png')
    plt.close()

def plot_router_types_time_series(
    router_data: Dict[str, List[float]],
    timestamp: str
) -> None:
    """Plot time series of processing times for different router types"""
    ensure_plots_dir()
    
    plt.figure(figsize=(12, 6))
    for router_type, times in router_data.items():
        plt.plot(times, label=router_type, marker='o')
    
    plt.title('Processing Time per Test Case by Router Type')
    plt.xlabel('Test Case')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'plots/router_types_time_series_{timestamp}.png')
    plt.close()

def plot_router_types_summary(
    router_results: Dict[str, 'RouterResult'],
    timestamp: str
) -> None:
    ensure_plots_dir()
    
    router_types = list(router_results.keys())
    avg_times = [results.get_avg_time() for results in router_results.values()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(router_types, avg_times)
    plt.title('Average Processing Time by Router Type')
    plt.xlabel('Router Type')
    plt.ylabel('Average Time (seconds)')
    plt.grid(True, alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}s',
                ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'plots/router_types_summary_{timestamp}.png')
    plt.close()