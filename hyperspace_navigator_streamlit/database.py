from neo4j import GraphDatabase, basic_auth
from secrets_util import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
from models import System

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