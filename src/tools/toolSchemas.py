randomNumbersTool = {
    "type": "function",
    "function": {
        "name": "get_random_numbers",
        "description": "Generates a list of random numbers",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "min": {
                    "type": "integer",
                    "description": "Lower bound on the generated number",
                },
                "max": {
                    "type": "integer",
                    "description": "Upper bound on the generated number",
                },
                "count": {
                    "type": "integer",
                    "description": "How many numbers should be calculated",
                }
            },
            "required": ["min", "max", "count"],
            "additionalProperties": False
        }
    }
}

temperatureTool = {
    "type": "function",
    "function": {
        "name": "get_temperature",
        "description": "Gives the temperature for a given location",
        "strict": True,
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
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        }
    }
}
