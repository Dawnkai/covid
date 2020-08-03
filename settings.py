import os

# App settings
LOGO_IMAGE = os.getenv("LOGO_IMAGE", "static/images/logo.png")
DISPLAY_SIZE = os.getenv("DISPLAY_SIZE", [650, 790])

# Simulation settings
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "static/images/background.jpg")
CONTAINER_SIZE = os.getenv("CONTAINTER_SIZE", (600, 600))
TICK_FRAMES = os.getenv("TICK_FRAMES", 60)
