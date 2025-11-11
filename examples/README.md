# Strand SDK Examples

This directory contains example scripts demonstrating the Strand SDK for biological sequence optimization.

## Examples

### `basic_optimization.py`

A comprehensive example showing the full optimization pipeline:

1. **Define Candidate Sequences**: Load biological sequences (proteins, DNA, RNA) to optimize
2. **Create Reward Blocks**: Combine multiple scoring functions:
   - Stability scoring
   - Solubility prediction
   - Novelty measurement
   - Custom scoring functions
3. **Run Optimization**: Compare different optimization methods:
   - Random search (baseline)
   - Cross-Entropy Method (CEM)
   - Genetic Algorithm (GA)
4. **Export Results**: Save results in JSON, CSV, and manifest formats

## Running the Examples

```bash
# Install the SDK in development mode
pip install -e .

# Run the basic optimization example
python examples/basic_optimization.py
```

## Expected Output

The script will:
- Print optimization progress for each method
- Display top 3 sequences ranked by score
- Export results to `results_*.json`, `results_*.csv`, and `manifest_*.json`
- Compare performance across methods

## Next Steps

- Explore different reward block configurations
- Implement custom scoring functions
- Test on real biological sequences
- Integrate with protein structure prediction models

