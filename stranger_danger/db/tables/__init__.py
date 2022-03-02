from stranger_danger.db.config.settings import Base
from stranger_danger.db.tables.classifier import Classifier
from stranger_danger.db.tables.email import Email
from stranger_danger.db.tables.fences import Fences
from stranger_danger.db.tables.predictions import Predictions

# Ignore unused import error
__all__ = ["Base", "Classifier", "Email", "Fences", "Predictions"]
