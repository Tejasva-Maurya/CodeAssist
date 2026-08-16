from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class GraphStorage(ABC):
    """
    Abstract base class for graph storage engines (SQLite, NetworkX, etc.).
    Defines the interface for storing and querying nodes and edges.
    """

    @abstractmethod
    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        """Add a node to the graph."""
        pass

    @abstractmethod
    def add_edge(self, source_id: str, target_id: str, relationship_type: str, properties: Dict[str, Any] = None):
        """Add a directional edge between two nodes."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a node's properties by its ID."""
        pass

    @abstractmethod
    def get_edges(self, node_id: str, direction: str = "both") -> List[Dict[str, Any]]:
        """
        Retrieve edges connected to a node.
        direction can be "out", "in", or "both"
        """
        pass
        
    @abstractmethod
    def commit(self):
        """Commit the current transaction to storage."""
        pass

    @abstractmethod
    def close(self):
        """Close the storage connection."""
        pass
