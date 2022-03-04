from typing import NewType

import numpy as np

AnnotadedImage = NewType("AnnotadedImage", np.ndarray)
FenceImage = NewType("FenceImage", np.ndarray)
