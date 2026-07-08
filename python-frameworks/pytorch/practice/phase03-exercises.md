# 📝 PyTorch — Phase 03 Practice (Advanced Architectures)

## Exercise 1: BatchNorm vs No BatchNorm

Train two identical 4-layer MLPs on a 200-sample dataset — one with BatchNorm after each Linear, one without. Compare training loss curves after 100 epochs.

## Exercise 2: CNN Feature Visualizer

Build a CNN with 3 conv layers on 16×16 input. Print the output shape after each conv+pool operation. Compute total parameter count.

## Exercise 3: CNN with Different Kernel Sizes

Compare CNNs with all 3×3 vs all 5×5 conv kernels (same depth). Which has more params? Which converges faster? Test on synthetic 2D data.

## Exercise 4: RNN for Sequence Classification

Generate a synthetic sequence dataset where each sequence of length 15 has a binary label (sum of elements > 0). Train an RNN classifier. Report test accuracy.

## Exercise 5: LSTM vs GRU Comparison

Train LSTM and GRU with the same hidden size on a sequence classification task. Compare parameters, training time, and accuracy.

## Exercise 6: Transfer Learning Experiment

Create a "pretrained" model (trained on one synthetic distribution), freeze its base, and train a new classifier on a similar but different distribution. Compare with training from scratch on the target.

## Exercise 7: Fine-Tuning with Discriminative LRs

Implement fine-tuning with 3× lower LR for base layers vs classifier layers. Train on a small target dataset. Show benefit vs training all layers at same LR.

## Exercise 8: Custom Focal Loss

Implement Focal Loss for binary classification with gamma=[0, 1, 2, 5]. Test on imbalanced synthetic data (95/5 split). Report precision and recall for the minority class.

## Exercise 9: TensorBoard Logger

Create a reusable training logger class that logs: loss, accuracy, LR, weight histograms, and gradients. Test it on a 30-epoch training run.

## Exercise 10: CNN Pipeline with Augmentation

Build a full image classification pipeline:
- CNN with 2 conv layers + 2 linear layers
- Data augmentation: add random noise to training data
- Train/val/test split with DataLoaders
- ReduceLROnPlateau scheduler
- Print test accuracy and confusion matrix
