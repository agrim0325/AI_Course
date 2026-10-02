# Neural Models Laboratory Report

## Task 1: Understand the problem before coding
1. **Input/Output Space:** Input space \mathcal{X} = \{0, 1\}^2. Output space \mathcal{Y} = \{0, 1\}. 
   Examples: (0,0) \to 0, (0,1) \to 1, (1,0) \to 1, (1,1) \to 0.
2. **Sketch:** (0,1) and (1,0) are positive class (1). (0,0) and (1,1) are negative class (0).
3. **Linear Separability:** No single straight line can separate the positive class from the negative class because they are positioned diagonally across from each other.
4. **Linear Model Prediction:** Training a single affine transformation followed by a sigmoid will fail to separate the classes. It will likely converge to a state where it outputs a probability of ~0.5 for all points.

## Task 2: Design the intelligent agent
1. **Necessity of Nonlinearity:** Without a nonlinear activation function, the two layers mathematically collapse into a single affine transformation (W^{(2)}(W^{(1)}x + b^{(1)}) + b^{(2)} is still just a linear map), making it impossible to solve the non-linear XOR problem.
2. **Output pairing:** A sigmoid outputs a value strictly between 0 and 1, perfectly representing a probability. Binary cross-entropy is theoretically aligned with this and penalizes probabilistic deviations properly.
3. **Validation criteria:** 
   - The final loss must be near zero (e.g., <0.05).
   - All four predictions (after thresholding at 0.5) must perfectly match the ground truth.
   - The gradients in the early steps must be non-zero (proving the network isn't stuck/dead).

## Task 3: Use an LLM to generate a first implementation
**Prompt used:** *"Generate minimal PyTorch code for a 2-2-1 neural network to learn the XOR dataset. Use Tanh hidden activation and BCEWithLogitsLoss. Set a random seed for reproducibility. Use full-batch training for 2000 steps with SGD. After training, print the final loss, probabilities, thresholded labels, and the first-layer weight gradient at step 0."*

## Task 4: Execute, test, and diagnose
**Part B – Backpropagation check**
parameter.grad represents the partial derivative of the loss L with respect to the weights W^{(1)}. Because we compute the mean loss over the four training examples before calling .backward(), this gradient is the average of the example-wise gradients.

**Part C – Symmetry experiment**
When initializing the network weights to zero, both hidden units receive the exact same inputs and gradients. As seen in the output, their weights remain identical ([0., 0.] -> [0., 0.]) and update in lockstep. This prevents them from learning distinct, useful features, which is why the network failed to learn XOR (loss stuck at 0.6931).

**Part D – Activation experiment**

| Hidden activation | Final loss | 4/4 correct? | Early ||\nabla_{W^{(1)}}L||_2 |
|---|---|---|---|
| Sigmoid | 0.0153 | Yes | 0.0119 |
| Tanh | 0.0017 | Yes | 0.0287 |
| ReLU | 0.3467 | No | 0.0820 |

*Interpretation:* Tanh provides steeper, zero-centered gradients compared to Sigmoid, allowing the network to converge to a much lower loss in the same number of steps. ReLU had the largest initial gradient but failed to solve the problem; depending on initialization, tiny networks using ReLU can suffer from "dead" units where the gradients become permanently zero.

## Task 5: Extend the task
1. **Weight matrix shape:** The final weight matrix has shape (3, 2) (3 output logits, 2 hidden units).
2. **Logits per example:** 3 logits per example.
3. **Softmax sum:** Softmax exponentiates the logits to make them positive, then divides by the total sum of the exponentiated values, naturally enforcing that they sum exactly to 1.
4. **Logit gradient:** The gradient p - y is the mathematical result of taking the derivative of the Cross-Entropy loss with respect to the pre-softmax logits. 

*Optional Diagnostic:* Adding 100 to all logits does not change the probabilities because softmax is translation invariant. Stable implementations subtract the maximum logit to prevent e^100 from overflowing floating-point memory bounds.

## Reflection Questions
1. **Depth and Nonlinearity:** The XOR experiment proved that depth alone is not enough; adding layers only increases representation power if those layers are separated by non-linear activations.
2. **Learning Signal:** The fact that the loss steadily converged to nearly 0.00 and perfectly classified the non-linear dataset proved the gradients contained useful directional learning signals, not just random non-zero noise.
3. **Zero Initialization:** Perfect symmetry ensures that the backpropagation algorithm distributes the exact same error signal to symmetric units, trapping them in a state where they remain identical forever.
4. **Activation impact:** Changing the activation shifted the magnitude of the gradients. Scientifically, this relates to the derivative of the activation function (e.g. max derivative of sigmoid is 0.25, while tanh is 1.0). Engineering-wise, this means different activations require different learning rates or initializations to avoid dead units (like we saw with ReLU).
5. **Output layer and Loss:** The output layer determines the format (e.g., logits, probabilities), and the loss function must be mathematically paired to correctly evaluate that format (e.g., BCEWithLogitsLoss combines sigmoid and BCE for numerical stability).
6. **LLM Usage:** The LLM improved productivity by instantly writing the PyTorch boilerplate and training loop. However, human verification was essential when designing the Symmetry check; the LLM might just write a standard training loop, but a human must explicitly add the print statements for the gradients at step 0 to prove the symmetry.
7. **Scaled up models:** In a large model, I would keep tracking the training loss curve and validating prediction metrics. I would drop printing explicit weight/gradient tensors (like the symmetry check) or exhaustive finite-difference gradient checking, as millions of parameters make that computationally and visually impossible.
