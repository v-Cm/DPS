from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        return

    def pagerank(self, max_iterations, weight_property):
        with self._driver.session() as session:
            result = session.run("CALL gds.graph.project('myGraph7', 'Location', {TRIP: {properties: ['distance', 'fare']}})")
            result = session.run(
                f"CALL gds.pageRank.stream('myGraph7', {{maxIterations: {max_iterations}, relationshipWeightProperty: '{weight_property}'}}) \
                YIELD nodeId, score \
                RETURN gds.util.asNode(nodeId).name AS name, score \
                ORDER BY score DESC"
            )

            nodes = []
            for record in result:
                node = {
                    "name": record["name"],
                    "score": record["score"]
                }
                nodes.append(node)

            # Return nodes with max and min PageRank
            max_node = max(nodes, key=lambda x: x["score"])
            min_node = min(nodes, key=lambda x: x["score"])

            return (max_node, min_node)

