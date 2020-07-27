import os

# Settings for project, user should not be able to change them
LOGO_IMAGE = os.getenv("LOGO_IMAGE", "static/images/logo.png")
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "static/images/background.jpg")
CONTAINER_SIZE = os.getenv("CONTAINTER_SIZE", (600, 400))
