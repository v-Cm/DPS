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
                RETURN path"
            )

            nodes = [dict(record) for record in result]
            print(nodes[0]['path'])
            d = []
            for p in nodes[0]['path']:
                node = p.nodes[0]
                name = node.get('name')
                d.append({'name':name})
                print(node)
            print(d)
            nodes[0]['path'] = d
            nodes[0]['path'].append({'name':last_node})

        # with self._driver.session() as session:
        #     # result = session.run("CALL gds.graph.project('myGraphBfs', 'Location', {TRIP: {properties: ['distance', 'fare']}})")
        #     result = session.run(
        #         f" MATCH (source:Location{{name:{start_node}}}), (target:Location{{name:{last_node}}}) \
        #         CALL gds.Bfs.stream('myGraphbfs', {{ \
        #         sourceNode: source, \
        #         targetNodes: target \
        #         }}) \
        #         YIELD nodeIds \
        #         UNWIND nodeIds AS nodeId \
        #         RETURN gds.util.asNode(nodeId).name AS name"
        #     )
            
        #     nodes = [{
        #         'path':[dict(record) for record in result]
        #     }]
        
        return nodes
    
    def pagerank(self, max_iterations, weight_property):
        with self._driver.session() as session:
            result = session.run("CALL gds.graph.project('myGraphPr', 'Location', {TRIP: {properties: ['distance', 'fare']}})")
            result = session.run(
                f"CALL gds.pageRank.stream('myGraphPr', {{maxIterations: {max_iterations}, relationshipWeightProperty: '{weight_property}'}}) \
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