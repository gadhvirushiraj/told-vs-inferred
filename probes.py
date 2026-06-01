import torch
import torch.nn.functional as F
from torch import nn


class LinearProbeClassification(nn.Module):
    def __init__(self, input_dim, probe_class):
        super().__init__()
        self.proj = nn.Linear(input_dim, probe_class)
        self.proj.weight.data.normal_(mean=0.0, std=0.02)
        self.proj.bias.data.zero_()

    def forward(self, act, y=None):
        logits = self.proj(act)
        if y is None:
            return logits, None
        return logits, F.cross_entropy(logits, y.long())


class LinearProbeClassificationMixScaler(nn.Module):
    """Single linear probe over a learned softmax-weighted mix of all layers."""
    def __init__(self, input_dim, probe_class, num_layers):
        super().__init__()
        self.mix_weights = nn.Linear(num_layers, 1, bias=False)
        nn.init.constant_(self.mix_weights.weight, 1.0 / num_layers)
        self.proj = nn.Linear(input_dim, probe_class)
        self.proj.weight.data.normal_(mean=0.0, std=0.02)
        self.proj.bias.data.zero_()

    def forward(self, act, y=None):
        # act: [B, num_layers, hidden]
        w = F.softmax(self.mix_weights.weight, dim=1)   # [1, num_layers]
        act = (act.permute(0, 2, 1) @ w.T)[..., 0]     # [B, hidden]
        logits = self.proj(act)
        if y is None:
            return logits, None
        return logits, F.cross_entropy(logits, y.long())
