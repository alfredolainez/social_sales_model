# -*- coding: utf-8 -*-
import random

class Node:

    nodeNumber = 0

    def __init__(self):
        Node.nodeNumber += 1
        self.sales = []
        self.parent = None
        self.nodeNumber = Node.nodeNumber

    def sale(self, graph, toNode):
        self.sales.append(toNode)
        graph.nodes.append(toNode)
        toNode.parent = self

        # Add connection to graph
        if graph.connections.get(self, False):
            graph.connections[self][toNode] = True
        else:
            graph.connections[self] = {toNode: True}

class Graph:

    nodes = []
    connections = {}

    def __init__(self):
        self.nodes = []
        self.connections = {}

    def getRandomNode(self):
        randomSelection = random.randint(0, len(self.nodes) - 1)
        return self.nodes[randomSelection]

    def addLonelyNode(self):
        self.nodes.append(Node())

    def __str__(self):
        result = ""
        result += "Nodes: "
        for node in self.nodes:
            result += str(node.nodeNumber)+ "; "
        result += "\nConnections: =>\n"
        for connection in self.connections.keys():
            result += str(connection.nodeNumber) + " connects with: "
            for node in self.connections[connection].keys():
                result += str(node.nodeNumber) + "; "
            result += "\n"
        return result


class RewardModel:

    def __init__(self,
                 discounts,
                 total_discount_limit=1,
                 discount_limits=[], # Non-applicable by default
                 mutual_benefit=False):

        self.mutual_benefit = mutual_benefit
        self.discounts = discounts    # expects list of weights [6,3]
        self.total_discount_limit = total_discount_limit
        self.discount_limits = discount_limits # expects list of limits in %1 [0.5, 0.4]

        self.limited = len(discount_limits) > 0 or total_discount_limit < 1

    def maximum_discount(self, num_sales, sale_price):
        """
        Returns maximum theoretical discount for a model. It doesn't consider limits in discounts
        """
        if self.mutual_benefit:
            self.discounts[0] *= 2
        discount1 = self.discounts[0] * sale_price
        discount2 = self.discounts[1] * sale_price
        maximum_discount = discount1 + (num_sales - 2) * (discount1 + discount2)
        return maximum_discount

def getNodeDiscounts(node, rewards):
    """
    Returns (first_grade_discount, second_grade_discount)
    """
    first_grade_discount = 0
    second_grade_discount = 0
    # If mutual, add benefit for buying to parent
    if rewards.mutual_benefit and node.parent != None:
        first_grade_discount += rewards.discounts[0]
    for sale in node.sales:
        first_grade_discount += rewards.discounts[0]
        second_grade_discount += rewards.discounts[1] * len(sale.sales)
    return (first_grade_discount, second_grade_discount)

def generateRandomGraph(cooperation, numNodes, rewards):

    def addLimitedNode():
        node_in_position = False
        while not node_in_position:
            node = graph.getRandomNode()
            node_discounts = getNodeDiscounts(node, rewards)
            ## Assumption: first grade sales are known, but second grade sales are unknown and so we don't stop
            ## adding second grade connections
            ## TODO: Quiza convendria añadir limitación de segundo grado para ponernos en caso peor
            ## TODO: Otra cosa para hacerlo más generico es meter booleanos en el modelo de los checks que se comprueban
            if node_discounts[0] + rewards.discounts[0] <= rewards.discount_limits[0]:
                node.sale(graph, Node())
                node_in_position = True

    graph = Graph()

    for i in range(0, numNodes):
        if random.uniform(0,1) > cooperation or len(graph.nodes) == 0:
            graph.addLonelyNode()
        else:
            # Cooperation passed: add to existing node
            if rewards.limited:
                addLimitedNode()
            else:
                node = graph.getRandomNode()
                node.sale(graph, Node())

    return graph


def get_sales_per_client(graph, rewards):
    """
    Returns list of the form [(2,4), (3,5)...]. One tuple for each node, the first element the number of first-grade sales
    and the second one the number of second-grade sales
    """
    sales_per_node = []
    # De momento que funcione con grado 2 de conexiones
    for node in graph.nodes:
        sales_first_grade = len(node.sales)
        if rewards.mutual_benefit and node.parent != None:
            sales_first_grade += 1
        sales_second_grade = 0
        for sale in node.sales:
            sales_second_grade += len(sale.sales)
        sales_per_node.append((sales_first_grade, sales_second_grade))

    return sales_per_node
