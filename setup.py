from setuptools import find_packages, setup

setup(
    name="omni_drones",
    version="1.0",
    keywords=["robotics", "rl"],
    packages=find_packages("."),
    install_requires=[
        "hydra-core",
        "omegaconf",
        "wandb",
        "imageio",
        "plotly",
        "einops",
        "pandas",
        "moviepy",
        "av",
        # "torchrl==0.3.1", # for torch==2.2.2
    ],
)
