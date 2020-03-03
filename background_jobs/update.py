import requests
from application import db
from .config import MOODLE_API_URL


# Loop through json request and check for users with timeModified in the last X hours.