#!/bin/bash
deactivate
source "env_tensor/bin/activate"
tensorboard --logdir runs/train/ --bind_all --bind_all