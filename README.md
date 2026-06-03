# Told vs. Inferred: User Attribute Conflicts in LLMs

Investigating whether LLMs follow explicit user statements about themselves or secretly rely on their own inferences about user attributes (expertise, age, background).

## Core Question

When a model's inferred profile of a user conflicts with what the user explicitly states, which wins? 

**Example:** User asks "How do I install Python?" (model infers: inexperienced), then says "I've been a senior engineer for 12 years." Does the model:
1. Update to accept the explicit claim?
2. Blend both signals?
3. Ignore the user and stick with its inference?

## Why This Matters

If models secretly trust their own inferences over explicit user statements, then stated intent becomes decorative. Users can't actually control the model by telling it about themselves. The model is following a hidden profile instead. This breaks instruction-following and creates invisible failure modes.

## Project Structure

```
told-vs-inferred/
├── baseline.ipynb          # Reproduce Chen et al. baseline
├── probes.py              # Probe architectures
├── data/                  # Conversation datasets
└── plots/                 # Analysis visualizations
```

## Baseline Results

**Dataset:** 1,000 multi-turn conversations (balanced gender labels)
**Model:** Google Gemma-4-E2B-it (1.5B parameters, 35 layers)
**Best Result:** LinearProbeClassification achieved 77.5% test accuracy on layer 26 for gender attribute classification

| Method | Max Accuracy | Avg Accuracy | Best Layer |
|--------|-------------|-------------|-----------|
| Difference in Means | 51.0% | 45.6% | 24 |
| Logistic Regression | 73.5% | 66.5% | 15 |
| LinearProbe (torch) | 77.5% | 66.5% | 26 |
| MixScaler (all layers) | 69.0% | - | all |

This confirms user attributes are linearly decodable from the residual stream, validating the foundation for conflict detection experiments.

## Next Phase

Generate datasets where stated and inferred attributes contradict, then measure how the probe representation changes at the exact moment of contradiction. See [Dataset Generation Pipeline Plan](data/DATASET_GENERATION.md) for details on synthetic conversation generation with auditor validation.

## References

Chen et al. (2024). "Discovering and Interpreting Emergent Behaviors in LLMs"
https://arxiv.org/abs/2406.07882
