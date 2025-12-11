#!/usr/bin/env python3
"""
Visualization script for Random Graphs Threshold Experiment
Generates plots showing probability curves for various graph properties
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict

# Set up matplotlib for better quality
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

def parse_results(filename):
    """Parse the CSV results file into a structured dictionary"""
    data = defaultdict(lambda: defaultdict(dict))
    current_property = None
    current_n = None
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                # Parse header: # PropertyName n=X trials=Y
                parts = line[2:].split()
                current_property = parts[0]
                for part in parts[1:]:
                    if part.startswith('n='):
                        current_n = int(part[2:])
            elif line == 'p,probability':
                continue
            else:
                try:
                    p, prob = map(float, line.split(','))
                    if current_property and current_n:
                        if 'p' not in data[current_property][current_n]:
                            data[current_property][current_n]['p'] = []
                            data[current_property][current_n]['prob'] = []
                        data[current_property][current_n]['p'].append(p)
                        data[current_property][current_n]['prob'].append(prob)
                except:
                    pass
    return data

def plot_property(data, property_name, title, threshold_func=None, threshold_label=None, filename=None):
    """Plot probability curves for a single property across different n values"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(data[property_name])))
    
    for idx, n in enumerate(sorted(data[property_name].keys())):
        p_values = data[property_name][n]['p']
        probs = data[property_name][n]['prob']
        ax.plot(p_values, probs, '-o', markersize=3, label=f'n = {n}', 
                color=colors[idx], linewidth=2)
        
        # Add vertical line at threshold if provided
        if threshold_func:
            threshold = threshold_func(n)
            if 0 < threshold < 1:
                ax.axvline(x=threshold, color=colors[idx], linestyle='--', 
                          alpha=0.5, linewidth=1)
    
    ax.set_xlabel('Edge Probability p')
    ax.set_ylabel('P(G has property)')
    ax.set_title(title)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    if threshold_label:
        ax.text(0.98, 0.02, f'Threshold: {threshold_label}', transform=ax.transAxes,
                fontsize=10, verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

def plot_all_properties(data):
    """Generate all plots"""
    
    # 1. Has Edge
    plot_property(data, 'HasEdge', 
                  'Probability of Having at Least One Edge in G(n,p)',
                  lambda n: 2/(n*(n-1)),
                  'p ≈ 2/n²',
                  'plot_has_edge.png')
    
    # 2. Has Triangle (K3)
    plot_property(data, 'HasK3',
                  'Probability of Containing a Triangle (K₃) in G(n,p)',
                  lambda n: 1/n,
                  'p = 1/n',
                  'plot_has_k3.png')
    
    # 3. Is Connected
    plot_property(data, 'IsConnected',
                  'Probability of Being Connected in G(n,p)',
                  lambda n: np.log(n)/n,
                  'p = ln(n)/n',
                  'plot_connected.png')
    
    # 4. Has K4
    plot_property(data, 'HasK4',
                  'Probability of Containing K₄ in G(n,p)',
                  lambda n: n**(-2/3),
                  'p = n^(-2/3)',
                  'plot_has_k4.png')
    
    # 5. Is Hamiltonian
    plot_property(data, 'IsHamiltonian',
                  'Probability of Having a Hamilton Cycle in G(n,p)',
                  lambda n: np.log(n)/n,
                  'p ≈ ln(n)/n',
                  'plot_hamiltonian.png')

def create_combined_plot(data):
    """Create a single figure with all 5 property plots"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    properties_info = [
        ('HasEdge', 'Has at Least One Edge', lambda n: 2/(n*(n-1)), 'p ≈ 2/n²'),
        ('HasK3', 'Contains Triangle (K₃)', lambda n: 1/n, 'p = 1/n'),
        ('IsConnected', 'Is Connected', lambda n: np.log(n)/n, 'p = ln(n)/n'),
        ('HasK4', 'Contains K₄', lambda n: n**(-2/3), 'p = n^(-2/3)'),
        ('IsHamiltonian', 'Has Hamilton Cycle', lambda n: np.log(n)/n, 'p ≈ ln(n)/n'),
    ]
    
    for idx, (prop_name, title, threshold_func, threshold_label) in enumerate(properties_info):
        ax = axes[idx]
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(data[prop_name])))
        
        for cidx, n in enumerate(sorted(data[prop_name].keys())):
            p_values = data[prop_name][n]['p']
            probs = data[prop_name][n]['prob']
            ax.plot(p_values, probs, '-o', markersize=2, label=f'n={n}',
                   color=colors[cidx], linewidth=1.5)
            
            if threshold_func:
                threshold = threshold_func(n)
                if 0 < threshold < 1:
                    ax.axvline(x=threshold, color=colors[cidx], linestyle='--',
                              alpha=0.4, linewidth=1)
        
        ax.set_xlabel('p')
        ax.set_ylabel('P(property)')
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.text(0.95, 0.05, threshold_label, transform=ax.transAxes,
               fontsize=8, va='bottom', ha='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Hide the 6th subplot
    axes[5].axis('off')
    
    plt.suptitle('Random Graph Properties: Threshold Effects in G(n,p)', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('plot_combined.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_threshold_comparison_table(data):
    """Create a table comparing experimental vs theoretical thresholds"""
    print("\n=== Threshold Comparison ===\n")
    print(f"{'Property':<20} {'n':<6} {'Theoretical p*':<18} {'Experimental p₅₀':<18} {'Ratio':<10}")
    print("-" * 80)
    
    theoretical = {
        'HasEdge': lambda n: 2/(n*(n-1)),
        'HasK3': lambda n: 1/n,
        'IsConnected': lambda n: np.log(n)/n,
        'HasK4': lambda n: n**(-2/3),
        'IsHamiltonian': lambda n: np.log(n)/n
    }
    
    for prop_name in ['HasEdge', 'HasK3', 'IsConnected', 'HasK4', 'IsHamiltonian']:
        for n in sorted(data[prop_name].keys()):
            p_values = np.array(data[prop_name][n]['p'])
            probs = np.array(data[prop_name][n]['prob'])
            
            # Find p where probability crosses 0.5
            idx = np.where(probs >= 0.5)[0]
            if len(idx) > 0:
                exp_threshold = p_values[idx[0]]
            else:
                exp_threshold = float('nan')
            
            theo_threshold = theoretical[prop_name](n)
            
            if not np.isnan(exp_threshold) and theo_threshold > 0:
                ratio = exp_threshold / theo_threshold
            else:
                ratio = float('nan')
            
            print(f"{prop_name:<20} {n:<6} {theo_threshold:<18.6f} {exp_threshold:<18.4f} {ratio:<10.3f}")

if __name__ == '__main__':
    data = parse_results('experiment_results.csv')
    
    # Generate individual plots
    plot_all_properties(data)
    
    # Generate combined plot
    create_combined_plot(data)
    
    # Print threshold comparison
    create_threshold_comparison_table(data)
    
    print("\nPlots saved: plot_has_edge.png, plot_has_k3.png, plot_connected.png,")
    print("             plot_has_k4.png, plot_hamiltonian.png, plot_combined.png")
