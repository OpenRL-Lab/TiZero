<div align="center">
<img width="300px" height="auto" src="./docs/figures/TiZero.png">
</div>

<div align="center">
<img height="300px" height="auto" src="./docs/figures/screen_800.png">
</div>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

### 1.Introduction

Reinforcement learning agent for Google Research Football.

Code accompanying the paper 
"TiZero: Mastering Multi-Agent Football with Curriculum Learning and Self-Play" (AAMAS 2023). [[paper](https://arxiv.org/abs/2302.07515)] [[videos](https://www.youtube.com/watch?v=U9REh0otmVU)]. 

<div align="center">
<img height="300px" height="auto" src="./docs/figures/football_trueskill.png">
</div>

### 2.Submit TiZero to JIDI(及第评测平台)

<div align="center">
<img height="400px" height="auto" src="./docs/figures/jidi.png">
</div>


JIDI is a public evaluation platform for RL agents. You can submit your agent of GRF at: [http://www.jidiai.cn/env_detail?envid=34](http://www.jidiai.cn/env_detail?envid=34).

We provide two agents under `./submission/` directory:

- `./submission/tizero`: the final model of TiZero for JIDI submission, which ranked 1st on October 28th, 2022.
- `./submission/random_agent`: the random agent for JIDI submission.


### 3.Cite

Please cite our paper if you use our codes or our weights in your own work:

```
@article{lin2023tizero,
  title={TiZero: Mastering Multi-Agent Football with Curriculum Learning and Self-Play},
  author={Lin, Fanqi and Huang, Shiyu and Pearce, Tim and Chen, Wenze and Tu, Wei-Wei},
  journal={arXiv preprint arXiv:2302.07515},
  year={2023}
}
```
