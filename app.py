import os
from langflow import main
from langflow.interface.load import load_flow_from_json

if __name__ == "__main__":
    flow_file = "flow.json"
    if os.path.exists(flow_file):
        flow = load_flow_from_json(flow_file)
        print(f"Loaded flow: {flow}")
    main()
