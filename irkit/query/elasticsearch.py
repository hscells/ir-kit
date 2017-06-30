"""
Functions and classes for dealing with ElasticSearch queries.

Harry Scells
Jun 2017
"""
from collections import OrderedDict

from typing import Generic


class Visitor(object):
    """
    Visitor interface for performing analysis on an ElasticSearch query. Implement the visit 
    method for the node to perform some action. A visitor can either store a result to be 
    returned by the traverse function, or 
    """

    def __init__(self, node_name: str):
        self.node_name = node_name
        self.depth = 0
        self.result = None

    def visit(self, node: dict):
        """
        Implement this class to visit nodes in an ElasticSearch query. When implementing for 
        traverse, place the result in self.result. When implementing for transform, return the 
        transformed node as a dict.
        
        :param node: A node in the ElasticSearch query.
        :return: See description.
        """
        raise NotImplementedError()


def traverse(query: dict, visitor: Visitor) -> Generic:
    """
    Traverse down the query tree using the specified visitor. Visitors used by this function 
    cannot modify the query. Instead they must store their return value into the result value
    on the visitor. This is useful for getting statistics about a query. The following example
    extracts all of the keywords in match queries:
    
    >>> class ExampleVisitor(Visitor):
    ...     def __init__(self, node_name: str):
    ...         super().__init__(node_name)
    ...         self.result = []
    ...     
    ...     def visit(self, node: dict):
    ...         self.result.append(node[self.node_name])
    >>> visitor = ExampleVisitor('match')
    >>> traverse({'query': {'must': {'match': 'example'}}}, visitor) 
    ['example']
    
    :param query: An ElasticSearch query.
    :param visitor: An implemented Visitor class.
    :return: The value stored in visitor.result.
    """
    if type(query) is list:
        for node in query:
            traverse(node, visitor)
    elif type(query) is dict or type(query) is OrderedDict:
        for key in query.keys():
            if key == visitor.node_name:
                visitor.visit(query)
            else:
                traverse(query[key], visitor)
    return visitor.result


def transform(query: dict, visitor: Visitor) -> dict:
    """
    Transform the query using a visitor. Visitors used by this function modify the query
    in-place and should not return anything. The following example will transform all of the 
    must queries to must_not queries:
    
    >>> class ExampleVisitor(Visitor):
    ...     def __init__(self, node_name: str):
    ...         super().__init__(node_name)
    ...     
    ...     def visit(self, node: dict):
    ...         node['must_not'] = node[self.node_name]
    ...         del node[self.node_name]
    >>> visitor = ExampleVisitor('must')
    >>> transform({'query': {'must': {'match': 'example'}}}, visitor) 
    {'query': {'must_not': {'match': 'example'}}}
    
    :param query: An ElasticSearch query.
    :param visitor: An implemented Visitor class.
    :return: A modified query 
    """
    if type(query) is list:
        for node in query:
            transform(node, visitor)
    elif type(query) is dict or type(query) is OrderedDict:
        for key in query.keys():
            if key == visitor.node_name:
                return visitor.visit(query)
            else:
                transform(query[key], visitor)
    return query
