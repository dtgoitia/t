#!/usr/bin/env python3

import subprocess
from dataclasses import dataclass
from pathlib import Path

ImageName = str


@dataclass
class PodmanImage:
    repository: ImageName
    tag: str

    def __str__(self) -> str:
        return f"{self.repository}:{self.tag}"


def parse_podman_image_stdout(line: str) -> PodmanImage:
    _doublespace = "  "

    tokens = [token.strip() for token in line.split(_doublespace) if token]
    repository, tag = tokens[:2]
    return PodmanImage(repository=repository, tag=tag)


def main() -> None:
    image_name = (Path(__file__).parent.parent / "IMAGE_NAME").read_text().strip()
    repository = f"localhost/{image_name}"

    process = subprocess.run(["sudo", "podman", "images"], capture_output=True)
    lines = process.stdout.decode("utf-8").strip().split("\n")

    images = [parse_podman_image_stdout(line) for line in lines[1:]]
    t_images = [str(image) for image in images if image.repository == repository]

    if not t_images:
        return

    print("\n".join(t_images))


if __name__ == "__main__":
    main()
