from fastapi.param_functions import Body

fence_examples = Body(
    ...,
    examples={
        "Rectangular": {
            "value": {
                "name": "Rectangular Fence",
                "coordinates": [
                    {"x": 0, "y": 0},
                    {"x": 30, "y": 0},
                ],
            },
        },
        "Pentagon": {
            "value": {
                "name": "Pentagon Fence",
                "coordinates": [
                    {"x": 0, "y": 0},
                    {"x": 30, "y": 0},
                    {"x": 30, "y": 40},
                    {"x": 30, "y": 50},
                    {"x": 30, "y": 40},
                ],
            },
        },
        "Circular": {
            "value": {
                "name": "Circular Fence",
                "center": {"x": 0, "y": 0},
                "radius": 0,
            },
        },
    },
)
