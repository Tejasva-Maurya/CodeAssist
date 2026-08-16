import sys
import os
import json

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor.java import JavaExtractor

def main():
    target_file = os.path.join(os.path.dirname(__file__), '..', 'tests', 'Dummy.java')
    
    with open(target_file, 'rb') as f:
        content = f.read()
        
    extractor = JavaExtractor()
    file_entity = extractor.parse_file(target_file, content)
    
    print(file_entity.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
