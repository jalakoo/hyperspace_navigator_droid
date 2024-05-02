from neo4j import GraphDatabase, basic_auth
from secrets_util import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
from models import System
import streamlit as st

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
    
@st.cache_data
def get_system_info(system: str):
    query = """
    MATCH (n:System)
    WHERE n.name = $systemName
    RETURN n
    """
    with GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)) as driver:
        params = {
            "systemName": system
        }
        records, _, _ = driver.execute_query(query,params, database=NEO4J_DATABASE)
        print(f'Matching Systems found: {records}')
        result = []
        for r in records:
            data = r.data()
            try:
                s = System(**data['n'])
                result.append(s)
            except Exception as e:
                print(f'Error parsing system record: {r}. Error: {e}')
                continue
        print(f'{len(result)} matching systems found')
        if len(result) == 0:
            return None
        return result[0]
    
@st.cache_data
def system_exists(system: str):
    query = """
    MATCH (n:System)
    WHERE n.name = $systemName
    RETURN n
    """
    with GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)) as driver:
        params = {
            "systemName": system
        }
        records, _, _ = driver.execute_query(query,params, database=NEO4J_DATABASE)
        result = []
        for r in records:
            data = r.data()
            try:
                s = System(**data['n'])
                result.append(s)
            except Exception as e:
                print(f'Error parsing system record: {r}. Error: {e}')
                continue
        print(f'{len(result)} matching systems found')
        return len(result) > 0
    
@st.cache_data
def get_plot_path(
        from_system: str,
        to_system: str,
        max_jumps: int = 100,
        exclude_systems: list[str] = [],
):
    
    query = f"""
        MATCH (start:System {{name: $start_system}})
        MATCH (end:System {{name: $end_system}}),
        path = shortestPath((start)-[:CONNECTED_TO|NEAR*0..{max_jumps}]-(end))
        WHERE ALL(y IN nodes(path) WHERE NOT y.name IN $exclude_systems)
        RETURN path
    """
    with GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)) as driver:
        params = {
            'start_system': from_system, 
            'end_system': to_system,
            'exclude_systems': exclude_systems
        }
        records, _, _ = driver.execute_query(query,params, database=NEO4J_DATABASE)

    try:
        nodes = records[0]['path'].nodes
        result = []
        for node in nodes:
            s = System(**node)
            result.append(s)
            # print(f'Node: {node}')
            # result.append(System(name=node['name'], x=node['X'], y=node['Y'], region=node['Region'], type='Plotted System', importance=node.get('pagerank', 0.0)))
    except Exception as e:
        print(f'\nError: {e} from query response: {records}')
        result = []
    return result