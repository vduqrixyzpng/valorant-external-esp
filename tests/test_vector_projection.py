"""Sanity tests for world_to_screen projection math."""
from valorant_esp.lib.vector import Vec3, world_to_screen


IDENTITY_VIEW = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1,
]


def test_center_projects_to_screen_center():
    p = world_to_screen(Vec3(0, 0, 1), IDENTITY_VIEW, 1920, 1080)
    assert p == (960, 540)


def test_point_behind_camera_returns_none():
    p = world_to_screen(Vec3(0, 0, -5), IDENTITY_VIEW, 1920, 1080)
    assert p is None