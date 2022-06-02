import networkx as nx
import json


class UnitManager:
    """Loads the tree structure and config objects"""

    def __init__(self, adjlist_file: str, config_file: str):
        self.G = nx.read_adjlist(adjlist_file, create_using=nx.DiGraph)

        with open(config_file) as f:
            config = json.load(f)

        nx.set_node_attributes(self.G, config)

    def config(self, unit_name: str) -> dict:
        """Returns config object or the parent's"""
        if self.G.nodes[unit_name]:
            return self.G.nodes[unit_name]

        for unit in nx.ancestors(self.G, unit_name):
            if self.G.nodes[unit]:
                return self.G.nodes[unit]

        return {}

    def has_fixed_membership_fee(self, unit_name: str) -> bool:
        """Returns if unit or parent has fixed membership fee config"""
        config = self.config(unit_name)
        return config["has_fixed_membership_fee"]

    def fixed_membership_fee_amount(self, unit_name: str) -> int:
        config = self.config(unit_name)
        return config["fixed_membership_fee_amount"]
