from models import System
import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_map(
    plot: list[System] = []
):
    
    print(f'plot: {plot}')
    
    # Config
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.grid(color='white')

    # Create
    all_x = [s.x for s in plot]
    all_y = [s.y for s in plot]
    ax.scatter(all_x, all_y)

    # Set Zoom
    margin = 100
    try:
        min_x = min(all_x) - margin
        max_x = max(all_x) + margin
        min_y = min(all_y) - margin
        max_y = max(all_y) + margin
    except Exception as e:
        print(f'Problem calculating min/max: {e} from all_x: {all_x} and all_y: {all_y}')
    plt.xlim(min_x, max_x)  # Set x-axis limits to zoom in
    plt.ylim(min_y, max_y)  # Set y-axis limits to zoom in

    # Node Label
    labels = [o.name for o in plot if o.x is not None and o.y is not None]
    for i, label in enumerate(labels):
        ax.text(all_x[i], all_y[i], label)
    
    # Course Plot
    plt.plot(all_x, all_y, 'b-', linewidth=0.5)

    return fig
