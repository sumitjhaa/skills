# Lesson 07.29: ML for Science (AlphaFold, ESM)

## Learning Objectives
- Understand protein structure prediction as a ML problem
- Implement equivariant neural networks for molecular data
- Apply AlphaFold's Evoformer and structure module
- Use protein language models (ESM) for biological sequence analysis

## Theory
ML for science applies deep learning to scientific problems: protein folding, molecular dynamics, drug discovery, materials, and weather.

### Key Challenges
- **Data scarcity**: Limited experimental data (e.g., protein structures)
- **Physical constraints**: Must respect symmetries (SE(3)), conservation laws
- **Multi-scale**: From atoms to organisms
- **Uncertainty**: Critical for scientific decision-making

## AlphaFold2

### Inputs
- **MSA (Multiple Sequence Alignment)**: $N_{\text{seqs}} \times L$ — evolutionary information
- **Pair features**: $L \times L$ — distances, relative positions

### Architecture

```
MSA → Evoformer (48 blocks) → Pair representation → Structure module (8 blocks) → 3D coordinates
```

### Evoformer Block
Dual-track processing (MSA and pair representations):

```
MSA → MSA row-wise gated self-attention → MSA column-wise attention
Pair → Outer product mean (MSA → pair) → Triangular attention → Tri mul
Pair → MSA update (via pair to MSA attention)
```

**Key insight**: Information flows between MSA track and pair track bidirectionally.

### Structure Module
Iterative refinement of 3D coordinates:
1. **IPA (Invariant Point Attention)**: SE(3)-equivariant attention using 3D points
2. **Backbone frame update**: Predict rotations and translations for each residue
3. **Side chain prediction**: Torsion angles via angle prediction

### Loss
- **FAPE (Frame-Aligned Point Error)**: Supervise per-atom positions in local frames
- **Distogram**: Distance distribution prediction
- **Auxiliary losses**: Side chain angle, confidence (pLDDT)

## AlphaFold3
- **Diffusion-based**: Generate structure via denoising (no iterative refinement)
- **All-atom**: Predict all heavy atoms, not just backbone
- **Protein-ligand**: Handles small molecules, nucleic acids, post-translational modifications
- **Pairformer**: Simplified Evoformer (pair representation only)

## ESM (Evolutionary Scale Modeling)

### Protein Language Models
Treat protein sequences as language:

$$p(\text{sequence}) = \prod_{i=1}^L p(a_i \mid a_{<i})$$

- **ESM-1b**: 650M parameters, BERT-style (masked language modeling)
- **ESM-2**: 3B parameters, trained on 250M sequences
- **ESMFold**: End-to-end structure prediction from single sequence (no MSA needed)

### Why Language Models Work for Proteins
- Protein sequences are "language of life" with grammar-like rules
- Evolutionary information encoded in sequence patterns
- Masked LM learns residue interactions

## Equivariant Neural Networks

### SE(3) Equivariance
$$f(\rho(g) x) = \rho'(g) f(x) \quad \forall g \in \text{SE}(3)$$

- **Translation**: $f(x + t) = f(x) + t$ (translation equivariant)
- **Rotation**: $f(R x) = R f(x)$ (rotation equivariant)

### Architectures

| Architecture | Type | Application |
|-------------|------|-------------|
| SchNet | Distance-based | Molecular properties |
| DimeNet | Angle-based | Quantum chemistry |
| EGNN | SE(3)-equivariant | Point clouds, molecules |
| SE(3)-Transformer | Lifting to SO(3) | Protein structure |
| NequIP | E(3)-equivariant | Force field predictions |

## Code: Simple Equivariant Layer (EGNN)

```python
import torch
import torch.nn as nn

class EquivariantLayer(nn.Module):
    def __init__(self, in_dim, hidden_dim):
        super().__init__()
        self.phi_e = nn.Sequential(nn.Linear(in_dim*2+1, hidden_dim), nn.SiLU())
        self.phi_h = nn.Sequential(nn.Linear(in_dim+hidden_dim, in_dim), nn.SiLU())
        self.phi_x = nn.Sequential(nn.Linear(hidden_dim, 1), nn.SiLU())

    def forward(self, h, x, edge_index):
        # h: node features, x: 3D coordinates
        i, j = edge_index
        coord_diff = x[i] - x[j]
        dist = torch.norm(coord_diff, dim=-1, keepdim=True)
        
        # Edge features
        e = self.phi_e(torch.cat([h[i], h[j], dist], dim=-1))
        
        # Update coordinates (SE(3)-equivariant)
        coord_update = self.phi_x(e) * coord_diff / (dist + 1e-8)
        x_new = x + torch.zeros_like(x).scatter_add(0, i[:, None].expand(-1, 3), coord_update)
        
        # Update node features
        h_new = h + torch.zeros_like(h).scatter_add(0, i[:, None].expand(-1, h.shape[1]),
                   self.phi_h(torch.cat([h[i], e], dim=-1)))
        
        return h_new, x_new
```

## ML for Science Applications

| Domain | Problem | ML Approach | Key Model |
|--------|---------|-------------|-----------|
| Structural biology | Protein folding | Equivariant + attention | AlphaFold |
| Drug discovery | Molecular generation | Diffusion, GNN | GeoDiff |
| Materials science | Crystal property | GNN, equivariant | MEGNet |
| Climate science | Weather prediction | Graph NN, Transformer | GraphCast |
| Particle physics | Jet tagging | Transformer, GNN | ParticleNet |
| Astrophysics | Galaxy morphology | CNNs, transformers | Zoobot |

## Practical Considerations
- **Data**: Open-source data — PDB (structures), UniRef (sequences), ChEMBL (molecules)
- **Evaluation**: tm-score (structure), MAE (forces), Spearman (ranking)
- **Pre-training**: Public checkpoints available (esm, alphafold, openfold)
- **Hardware**: Protein structure prediction requires 4+ GPUs with large memory
- **Validation**: Always validate with domain experts — ML predictions can be subtly wrong

## Limitations
- **Extrapolation**: ML models perform poorly on out-of-distribution systems
- **Physics violations**: ML may not satisfy physical constraints (e.g., energy conservation)
- **Data quality**: Experimental data has biases and measurement errors
- **Interpretability**: "Black box" predictions are hard to trust in science
- **Reproducibility**: Scientific ML papers often miss training details

## References
- Jumper, Evans, Pritzel, et al., "Highly accurate protein structure prediction with AlphaFold", Nature 2021
- Abramson, Adler, Dunger, et al., "Accurate structure prediction of biomolecular interactions with AlphaFold 3", Nature 2024
- Lin, Akin, Rao, et al., "Evolutionary-scale prediction of atomic-level protein structure with a language model (ESM)", Science 2023
- Lam, Sanchez-Gonzalez, Willson, et al., "GraphCast: Learning skillful medium-range global weather forecasting", Science 2023
- Satorras, Hoogeboom, Welling, "E(n) Equivariant Graph Neural Networks (EGNN)", ICML 2021
