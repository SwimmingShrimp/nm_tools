import torch.nn.functional as F
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)