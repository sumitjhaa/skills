# 📝 PyTorch — Phase 04 Practice (Production & Deployment)

## Exercise 1: Device-Agnostic Training

Take any previous training script and refactor it to be device-agnostic (works on CPU and CUDA). Print the device being used.

## Exercise 2: Mixed Precision Benchmark

Time 100 training epochs with and without AMP. Report the speedup factor. (If no GPU, explain where the speedup would come from.)

## Exercise 3: TorchScript Export & C++ Inference

Export a trained model with torch.jit.trace. Load it back and verify predictions match. Then inspect the graph with `loaded.graph`.

## Exercise 4: ONNX Export & Validate

Export an MLP to ONNX format. Validate the ONNX model with onnx.checker. Run inference with ONNX Runtime and compare outputs to PyTorch.

## Exercise 5: TorchServe Handler

Write a TorchServe handler for an image classifier that:
- Accepts raw pixel arrays as input
- Runs inference
- Returns top-1 and top-3 class predictions with probabilities

## Exercise 6: Hyperparameter Sweep

Perform a grid search over learning_rate=[0.1, 0.01, 0.001], hidden_size=[32, 64], dropout=[0, 0.2, 0.5] for a binary classifier. Use validation accuracy to select the best combination.

## Exercise 7: Gradient Clipping Threshold

Train a deep (5+ layer) MLP with gradient clipping at max_norm=[0.1, 1.0, 10.0, None]. Compare training stability and final accuracy.

## Exercise 8: Custom Initialization

Compare Kaiming, Xavier, and zero initialization for a 4-layer MLP on a classification task. Report training loss curves for the first 50 epochs.

## Exercise 9: Production Pipeline

Build a complete pipeline that:
1. Generates and splits data
2. Trains a model with gradient clipping and LR scheduling
3. Saves the best checkpoint
4. Exports to TorchScript
5. Loads and runs inference on new data
6. Measures inference latency (average of 100 runs)

## Exercise 10: Full CI/CD-Ready Training

Create a training script that:
- Accepts hyperparameters as command-line arguments (argparse)
- Logs metrics with TensorBoard
- Supports CPU/CUDA automatically
- Implements early stopping
- Saves the best model + TorchScript export
- Runs without errors when executed as `python train.py --lr 0.01 --epochs 50 --hidden 64`
