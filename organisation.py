from dataclasses import dataclass
import json
import networkx as nx


@dataclass
class OrganisationUnit:
    name: str
    config: dict


class UnitManager:
    """Loads the tree structure and config objects"""

    def __init__(self, adjlist_file: str, config_file: str):
        self.G = nx.read_adjlist(adjlist_file, create_using=nx.DiGraph)
        self.root = next(nx.topological_sort(self.G))

        with open(config_file) as f:
            config = json.load(f)

        nx.set_node_attributes(self.G, config)

    def organisation_unit(self, unit_name: str) -> OrganisationUnit:
        """Returns the organisation unit with its config object or its ancestor's"""
        config = {}
        if self.G.nodes[unit_name]:
            config = self.G.nodes[unit_name]
        else:
            # breaks if source is unit_name and target is root
            ancestors = reversed(
                nx.shortest_path(self.G, source=self.root, target=unit_name)
            )
            for unit in ancestors:
                if self.G.nodes[unit]:
                    config = self.G.nodes[unit]
                    break

        return OrganisationUnit(unit_name, config)
