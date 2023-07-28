import pygame
import data.variables as var  # Import the variables


def add_to_rects_blit_ui(rect, offset=0):
    """
    Add a rect to the list of rects used to erase the ui of the screen
    (we increase the size of the rect, so we don't see the borders left on the screen)

    Args:
        rect (pygame.Rect): Rect to add
        offset (int): Offset to add to the rect
    """
    rect_to_add = pygame.Rect(rect.x, rect.y, rect.width + offset, rect.height + offset)  # Rect to add
    var.RECTS_BLIT_UI.append(rect_to_add)  # We add the rect to the list