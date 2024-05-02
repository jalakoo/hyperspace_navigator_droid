from models import System
from neo4j import GraphDatabase, basic_auth
from secrets_util import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@st.cache_data
def scan_of_galaxy():
    query = """
    MATCH (n:System)
    WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL
    RETURN DISTINCT n
    """
    # query = """
    # MATCH (n:System)
    # WHERE n.name IS NOT NULL AND n.X IS NOT NULL AND n.Y IS NOT NULL
    # RETURN DISTINCT n.name as name, n.X as x, n.Y as y, n.Region as region, n.type as type, n.importance as importance, n.Link as link
    # """
    with GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)) as driver:
        records, _, _ = driver.execute_query(query, database=NEO4J_DATABASE)
        result = []
        for r in records:
            data = r.data()
            try:
                s = System(**data['n'])
                result.append(s)
            except Exception as e:
                print(f'Error parsing system record: {r}. Error: {e}')
                continue
        print(f'{len(result)} Systems found')
        return result

def create_map(
    systems: list[System] = [],
    show_plot: bool = False
):
    
    if systems is None or len(systems) == 0:
        print('No system data provided')
        return None, None

    # Config
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.grid(color='white')

    # Create
    all_x = [s.X for s in systems]
    all_y = [s.Y for s in systems]
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
    
    # Course Plot
    if show_plot is True:
        # Show all system names in a plot
        labels = [o.name for o in systems if o.X is not None and o.Y is not None]
        plt.plot(all_x, all_y, 'b-', linewidth=0.5)
    else:
        # Show only milestone systems in general map
        labels = [o.name for o in systems if o.X is not None and o.Y is not None and o.importance > 0.5]

    for i, label in enumerate(labels):
        ax.text(all_x[i], all_y[i], label)

    return (fig, ax)
