# 📝 PyTorch — Phase 02 Practice (Neural Networks & Training)

## Exercise 1: Sequential vs Custom

Build a 4-layer MLP (20→64→32→1) using nn.Sequential and also as a custom nn.Module subclass. Verify both produce the same forward output for random input.

## Exercise 2: Activation Comparison

Train identical 2-layer MLPs with ReLU, Tanh, and LeakyReLU on a binary classification task. Compare convergence speed and final accuracy after 50 epochs.

## Exercise 3: Dataset from CSV

Create a Dataset class that reads from a dictionary of numpy arrays (simulate a CSV). Implement __len__ and __getitem__ with proper tensor conversion.

## Exercise 4: Batch Size Effect

Train the same model with batch sizes [8, 32, 128, full-batch]. Compare training time per epoch and final accuracy on a 1000-sample dataset.

## Exercise 5: MLP Depth Study

Compare 1, 2, 3, and 4 hidden layer MLPs (same total param budget ≈ 2000). Which depth performs best on a synthetic 10-feature classification?

## Exercise 6: Checkpoint Resume

Train a model for 20 epochs, save a checkpoint with model state, optimizer state, and epoch number. Then load and resume training for 10 more epochs. Verify loss continues from where it left off.

## Exercise 7: Early Stopping with Restore

Implement early stopping that saves the best model weights and restores them after training stops. Verify the restored model matches the best validation performance.

## Exercise 8: Scheduler Showdown

Compare StepLR, CosineAnnealingLR, and ReduceLROnPlateau on the same training run. Print the LR at each epoch and the final validation accuracy.

## Exercise 9: Regularization Grid

Train models with all combinations of dropout=[0, 0.2, 0.5] and weight_decay=[0, 1e-5, 1e-4] on a small dataset (n=200, make it easy to overfit). Report train vs test accuracy for each.

## Exercise 10: Multi-Class Pipeline

Build a full pipeline for 5-class classification with 8 features (n=1500):
- 70/15/15 split
- MLP with 2 hidden layers
- CrossEntropyLoss + Adam
- ReduceLROnPlateau scheduler
- Early stopping (patience=10)
- Test set evaluation with confusion matrix (print as text table)
