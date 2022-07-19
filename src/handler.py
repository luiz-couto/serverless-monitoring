from typing import Dict, Any

def handler(data: dict, context: object) -> Dict[str, Any]:
    print("DATA:", data)
    print("CONTEXT:", context)
    
    return {
        "test": "my awesome test"
    }
