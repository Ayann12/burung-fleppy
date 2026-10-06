import os
import sys

# =========================
# resource convert img
# =========================
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)





# untuk di gambarnya
background_image = pygame.image.load(resource_path(
    "flappybirdbg.png"
))