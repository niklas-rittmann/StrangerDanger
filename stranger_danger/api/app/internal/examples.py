from fastapi.param_functions import Body

rec_example = Body(
    ...,
    example={
        "name": "Rectangular Fence",
        "coordinates": [
            {"x": 30, "y": 40},
            {"x": 70, "y": 80},
        ],
    },
)

pent_example = Body(
    ...,
    example={
        "name": "Rectangular Fence",
        "coordinates": [
            {"x": 0, "y": 0},
            {"x": 30, "y": 0},
            {"x": 30, "y": 40},
            {"x": 30, "y": 50},
            {"x": 30, "y": 40},
        ],
    },
)
