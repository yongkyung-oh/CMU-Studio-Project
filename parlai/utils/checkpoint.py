"""Load tensor state dictionaries without executing checkpoint pickle globals."""

import torch


def load_state_checkpoint(path):
    """Read a CPU checkpoint; never retry with unrestricted pickle loading.

    Opt/APEX/custom-class checkpoints must first be exported as plain
    tensor/dict state in an isolated environment by their trusted producer.
    Restricted loading does not prevent denial of service: use trusted files.
    """
    states = torch.load(path, map_location='cpu', weights_only=True)
    if not isinstance(states, dict):
        raise ValueError('Expected a dictionary checkpoint.')
    return states
