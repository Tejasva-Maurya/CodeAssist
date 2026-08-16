import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from storage.sqlite_graph import SQLiteStorage

def mock_map_reduce(graph_db: SQLiteStorage):
    print("=== MAP PHASE ===")
    print("Extracting precise relationships from Graph DB...")
    
    # 1. Get the file
    target_file = os.path.join(os.path.dirname(__file__), '..', 'tests', 'Dummy.java')
    file_id = f"file:{target_file}"
    
    # Get classes declared in this file
    edges = graph_db.get_edges(file_id, "out")
    classes = [edge["target_id"] for edge in edges if edge["relationship_type"] == "DECLARES_CLASS"]
    
    mapped_data = []
    
    for cls in classes:
        cls_node = graph_db.get_node(cls)
        print(f"Mapped Class: {cls_node['properties']['name']}")
        
        # Get methods in this class
        method_edges = graph_db.get_edges(cls, "out")
        for edge in method_edges:
            if edge["relationship_type"] == "HAS_METHOD":
                method_id = edge["target_id"]
                method_node = graph_db.get_node(method_id)
                
                # Get calls made by this method
                call_edges = graph_db.get_edges(method_id, "out")
                calls = [ce["target_id"].split(":")[-1] for ce in call_edges if ce["relationship_type"] == "CALLS"]
                
                method_info = {
                    "name": method_node["properties"]["name"],
                    "signature": method_node["properties"]["signature"],
                    "calls": calls
                }
                mapped_data.append(method_info)
                print(f"  Mapped Method: {method_info['name']} -> Calls: {calls}")
                
    print("\n=== REDUCE PHASE ===")
    print("Synthesizing Mapped Data into an Architecture Document...")
    
    # Mock LLM Synthesis
    mermaid_code = "graph TD;\n"
    for md in mapped_data:
        for call in md["calls"]:
            mermaid_code += f"    {md['name']} --> {call};\n"
            
    print("\n[Generated Architecture Document]")
    print(f"## Overview\nThe system consists of classes that interact as follows:\n\n```mermaid\n{mermaid_code}```")

if __name__ == "__main__":
    codeassist_dir = os.path.join(os.path.dirname(__file__), '..', '.codeassist')
    db_path = os.path.join(codeassist_dir, 'code_graph.db')
    graph_db = SQLiteStorage(db_path)
    mock_map_reduce(graph_db)
