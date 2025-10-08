# Multi-UAV Formation Control with Static and Dynamic Obstacle Avoidance via Reinforcement Learning
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Yuqing Xie*, Chao Yu*, Hongzhi Zang*, Wenhao Tang, Jingyi Huang, Jiayu Chen, Botian Xu, Yi Wu, Yu Wang

Website: https://sites.google.com/view/uav-formation-with-avoidance/

This is the official repository of the paper "Multi-UAV Formation Control with Static and Dynamic Obstacle Avoidance via Reinforcement Learning". This repository is heavily based on https://github.com/btx0424/OmniDrones.git.

<div align=center>
<img src="https://github.com/thu-uav/multi-UAV-formation/blob/main/overview.png" width="700"/>
</div>

We propose a two-stage RL training pipeline. In the first stage, we randomly search within the reward function space to find the best one that balances all four objectives. The second stage applies the selected reward function to a more complex scenario and solves the transformed single-objective task with curriculum learning.


## Install

#### 1. Download Isaac Sim (local version)

Download the [Omniverse Isaac Sim (local version)](https://developer.nvidia.com/isaac-sim) and install the desired Isaac Sim release **(version 2022.2.0)** following the [official document](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html). *Note that Omniverse Isaac Sim supports multi-user access, eliminating the need for repeated downloads and installations across different user accounts.*

Set the following environment variables to your ``~/.bashrc`` or ``~/.zshrc`` files :

```
# Isaac Sim root directory
export ISAACSIM_PATH="${HOME}/.local/share/ov/pkg/isaac_sim-2022.2.0"
```

*(Currently we use isaac_sim-2022.2.0. Whether other versions can work or not is not guaranteed. We provide a .zip flie for [isaac_sim-2022.2.0](https://drive.google.com/file/d/1ZrfhIkQVdRynthJ2FqGBC5jA93J6yEiZ/view?usp=sharing). For easy usage, we also provide a [guide](https://github.com/thu-uav/Multi-UAV-pursuit-evasion/issues/1#issuecomment-2573176995) on the correct usage of Isaac Sim 2022.)*

After adding the environment variable, apply the changes by running:
```
source ~/.bashrc
```

#### 2. Conda

Although Isaac Sim comes with a built-in Python environment, we recommend using a seperate conda environment which is more flexible. We provide scripts to automate environment setup when activating/deactivating a conda environment at ``Multi-UAV-pursuit-evasion/conda_setup``.

```
conda create -n sim python=3.7
conda activate sim

# at Multi-UAV-pursuit-evasion/
cp -r conda_setup/etc $CONDA_PREFIX
# re-activate the environment
conda activate sim
# install Multi-UAV-pursuit-evasion
pip install -e .

# verification
python -c "from omni.isaac.kit import SimulationApp"
# which torch is being used
python -c "import torch; print(torch.__path__)"
```

#### 3. Third Party Packages
Multi-UAV-pursuit-evasion requires specific versions of the `tensordict` and `torchrl` packages. For the ``deploy`` branch, it supports `tensordict` version 0.1.2+5e6205c and `torchrl` version 0.1.1+e39e701. 

We manage these two packages using Git submodules to ensure that the correct versions are used. To initialize and update the submodules, follow these steps:

Get the submodules:
```
# at Multi-UAV-pursuit-evasion/
git submodule update --init --recursive
```
Pip install these two packages respectively:
```
# at Multi-UAV-pursuit-evasion/
cd third_party/tensordict
pip install -e . --no-build-isolation
```
```
# at Multi-UAV-pursuit-evasion/
cd third_party/torchrl
pip install -e . --no-build-isolation
```
Install dgl:
```
pip install dgl -f https://data.dgl.ai/wheels/torch-1.13/cu122/repo.html
```
#### 4. Verification
```
# at Multi-UAV-pursuit-evasion/
cd scripts
python train.py headless=true wandb.mode=disabled total_frames=50000 task=Hover
```

#### 5. Working with VSCode

To enable features like linting and auto-completion with VSCode Python Extension, we need to let the extension recognize the extra paths we added during the setup process.

Create a file ``.vscode/settings.json`` at your workspace if it is not already there.

After activating the conda environment, run

```
printenv > .vscode/.python.env
``````

and edit ``.vscode/settings.json`` as:

```
{
    // ...
    "python.envFile": "${workspaceFolder}/.vscode/.python.env",
}
```

## Usage

For general usage and more details, please refer to the [documentation](https://omnidrones.readthedocs.io/en/latest/).

The code is organized as follow:
```
cfg
|-- train.yaml
|-- algo
    |-- mappo.yaml
|-- task
    |-- FormationUnified.yaml
omni_drones
|-- envs
    |-- formation_unified.py
scripts
|-- train_weight.py
|-- parse_weight.py
|-- train.py
```

For policy training and evaluation, run the following commands:
```
cd scripts
# for stage-1 training, try multiple reward weights
python train_weight.py 
# obtain a csv file that contains all reward weights and their corresponding performance
python parse_weight.py 
```

After determining the best reward function, fill in the weight in `cfg/task/FormationUnified.yaml` and then run:
```
# first period in CL, obstacle-free
python train.py total_frames=15_000_000 task.static_obs_num=0 task.ball_num=1 task.throw_threshold=1000 task.throw_time_range=800

# second period in CL, static obstacle only
python train.py total_frames=150_000_000 task.static_obs_num=10 task.ball_num=1 task.throw_threshold=1000 task.throw_time_range=800 \
+init_ckpt_path=/previous/run/ckpt

# third period in CL, mixed obstacles
python train.py total_frames=150_000_000 task.static_obs_num=10 task.ball_num=2 \
+init_ckpt_path=/previous/run/ckpt
```

## Citation
please cite [our paper](http://arxiv.org/abs/2410.18495
) if you find it useful:

```
@misc{xie2024multiuavbehaviorbasedformationstatic,
      title={Multi-UAV Behavior-based Formation with Static and Dynamic Obstacles Avoidance via Reinforcement Learning}, 
      author={Yuqing Xie and Chao Yu and Hongzhi Zang and Feng Gao and Wenhao Tang and Jingyi Huang and Jiayu Chen and Botian Xu and Yi Wu and Yu Wang},
      year={2024},
      eprint={2410.18495},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2410.18495}, 
}
```
