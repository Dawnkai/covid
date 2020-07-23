import os

LOGO_IMAGE = os.getenv("LOGO_IMAGE", "static/images/logo.png")
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "static/images/background.jpg")
DISPLAY_SIZE = os.getenv("DISPLAY_SIZE", (1200, 800))
CONTAINER_SIZE = os.getenv("CONTAINTER_SIZE", (800, 600))
