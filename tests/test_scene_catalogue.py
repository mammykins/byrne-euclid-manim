import pytest

from byrne_euclid import definitions, postulates, propositions
from byrne_euclid.rendering import SCENE_REGISTRY
from byrne_euclid.style import ByrneScene

EXPECTED_SCENES = {
    "PaletteCard": (definitions, "src/byrne_euclid/definitions.py"),
    "DefPointLineStraightLine": (definitions, "src/byrne_euclid/definitions.py"),
    "DefAngleTypes": (definitions, "src/byrne_euclid/definitions.py"),
    "DefCircle": (definitions, "src/byrne_euclid/definitions.py"),
    "DefTrianglesBySide": (definitions, "src/byrne_euclid/definitions.py"),
    "DefTrianglesByAngle": (definitions, "src/byrne_euclid/definitions.py"),
    "DefQuadrilaterals": (definitions, "src/byrne_euclid/definitions.py"),
    "DefParallelLines": (definitions, "src/byrne_euclid/definitions.py"),
    "PostulateI": (postulates, "src/byrne_euclid/postulates.py"),
    "PostulateII": (postulates, "src/byrne_euclid/postulates.py"),
    "PostulateIII": (postulates, "src/byrne_euclid/postulates.py"),
    "PropI": (propositions, "src/byrne_euclid/propositions.py"),
    "PropII": (propositions, "src/byrne_euclid/propositions.py"),
    "PropIII": (propositions, "src/byrne_euclid/propositions.py"),
    "PropIX": (propositions, "src/byrne_euclid/propositions.py"),
    "PropX": (propositions, "src/byrne_euclid/propositions.py"),
    "PropXI": (propositions, "src/byrne_euclid/propositions.py"),
    "PropXII": (propositions, "src/byrne_euclid/propositions.py"),
    "PropXIII": (propositions, "src/byrne_euclid/propositions.py"),
    "PropXV": (propositions, "src/byrne_euclid/propositions.py"),
    "PropXXXII": (propositions, "src/byrne_euclid/propositions.py"),
}


@pytest.mark.parametrize(("scene_name", "scene_details"), EXPECTED_SCENES.items())
def test_scene_class_exists_and_inherits_byrne_scene(scene_name: str, scene_details: tuple) -> None:
    module, _ = scene_details
    scene_class = getattr(module, scene_name)
    assert issubclass(scene_class, ByrneScene)


def test_scene_registry_contains_the_full_catalogue() -> None:
    for scene_name, (_, module_path) in EXPECTED_SCENES.items():
        assert SCENE_REGISTRY[scene_name] == module_path
