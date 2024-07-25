tryRandomNTool = {
    "type": "function",
    "function": {
        "name": "get_random_numbers",
        "description": "Generates a list of random numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "min": {
                    "type": "integer",
                    "description": "The generated numbers will be greater than this",
                },
                "max": {
                    "type": "integer",
                    "description": "The generated numbers will be smaller than this",
                },
                "count": {
                    "type": "integer",
                    "description": "How many numbers should be calculated",
                }
            },
            "required": ["location"],
        }
    }
}

temperatureTool = {
    "type": "function",
    "function": {
        "name": "get_temperature",
        "description": "Gives the temperature for a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "The latitude of the location",
                },
                "longitude": {
                    "type": "number",
                    "description": "The longitude of the location",
                },
            },
            "required": ["latitude, longitude"],
        }
    }
}