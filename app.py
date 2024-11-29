import os
from langflow import main
from langflow import load_flow_from_json

if __name__ == "__main__":
    flow_file = "LangRAG.json"
    if os.path.exists(flow_file):
        flow = load_flow_from_json(flow_file)
        print(f"Loaded flow: {flow}")
    main()
