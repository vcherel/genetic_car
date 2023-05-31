import pygame  # To use pygame


def scale_image(img, factor):
    """
    Change the scale of an image

    Args:
        img (pygame.Surface): the image to scale
        factor (float): the scale factor

    Returns:
        scaled_image (pygame.image): the scaled image
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)