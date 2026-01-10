
# fake_quantization_kernels.py
import torch

def load_quantization_kernel(*args, **kwargs):
    return None

class QuantizationKernel:
    def __init__(self):
        pass
    
    def forward(self, *args):
        return None
