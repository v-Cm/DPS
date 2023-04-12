from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        with self._driver.session() as session:
            result = session.run("CALL gds.graph.project('myGraphBfs', 'Location', {TRIP: {properties: ['distance', 'fare']}})")
            result = session.run(
            f" MATCH (source:Location{{name:{start_node}}}), (target:Location{{name:{last_node}}}) \
            CALL gds.bfs.stream('myGraphBfs', {{ \
            sourceNode: source, \
            targetNodes: target \
            }}) \
            YIELD path \
            RETURN REDUCE(acc = [], n in nodes(path) | acc + {{name: n.name}}) AS path"
            )
            
            nodes_list = [dict(record) for record in result]

            return nodes_list
    
    def pagerank(self, max_iterations, weight_property):
        with self._driver.session() as session:
            result = session.run("CALL gds.graph.project('myGraphPr', 'Location', {TRIP: {properties: ['distance', 'fare']}})")
            result = session.run(
                f"CALL gds.pageRank.stream('myGraphPr', {{maxIterations: {max_iterations}, relationshipWeightProperty: '{weight_property}'}}) \
                YIELD nodeId, score \
                RETURN gds.util.asNode(nodeId).name AS name, score \
                ORDER BY score DESC"
            )

            nodes_list = [{"name": record["name"], "score": record["score"]} for record in result]
            top_node = max(nodes_list, key=lambda node: node["score"])
            bottom_node = min(nodes_list, key=lambda node: node["score"])

            return (top_node, bottom_node)