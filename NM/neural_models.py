import torch
import torch.nn as nn
import torch.optim as optim

def run_xor_experiment(activation_name, zero_init=False):
    torch.manual_seed(42)
    
    X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
    
    class XORModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.hidden = nn.Linear(2, 2)
            if activation_name == 'sigmoid':
                self.act = nn.Sigmoid()
            elif activation_name == 'tanh':
                self.act = nn.Tanh()
            elif activation_name == 'relu':
                self.act = nn.ReLU()
            else:
                raise ValueError("Unknown activation")
            self.output = nn.Linear(2, 1)
            
            if zero_init:
                nn.init.zeros_(self.hidden.weight)
                nn.init.zeros_(self.hidden.bias)
                nn.init.zeros_(self.output.weight)
                nn.init.zeros_(self.output.bias)

        def forward(self, x):
            return self.output(self.act(self.hidden(x)))
            
    model = XORModel()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1.0)
    
    early_grad_norm = None
    
    for step in range(2000):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        
        if step == 0:
            early_grad_norm = torch.norm(model.hidden.weight.grad).item()
            if zero_init:
                print(f"  Step 0 hidden weights:\n{model.hidden.weight.data}")
                print(f"  Step 0 hidden grad:\n{model.hidden.weight.grad}")
        if step == 10 and zero_init:
            print(f"  Step 10 hidden weights:\n{model.hidden.weight.data}")
        
        optimizer.step()
        
    logits = model(X)
    probs = torch.sigmoid(logits)
    preds = (probs >= 0.5).float()
    correct = (preds == y).all().item()
    
    return loss.item(), correct, early_grad_norm, probs, preds

def run_multiclass_experiment():
    torch.manual_seed(42)
    X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = torch.tensor([0, 1, 1, 2], dtype=torch.long)
    
    class MultiClassModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.hidden = nn.Linear(2, 2)
            self.act = nn.Tanh()
            self.output = nn.Linear(2, 3)

        def forward(self, x):
            return self.output(self.act(self.hidden(x)))
            
    model = MultiClassModel()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=1.0)
    
    for step in range(2000):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        
    logits = model(X)
    probs = torch.softmax(logits, dim=1)
    preds = torch.argmax(probs, dim=1)
    
    print("\n--- Multiclass Experiment ---")
    print(f"Final Loss: {loss.item():.4f}")
    print(f"Predictions: {preds.tolist()}")
    print("Probabilities for (0,0):", probs[0].tolist(), "Sum:", probs[0].sum().item())
    
    shifted_logits = logits + 100
    shifted_probs = torch.softmax(shifted_logits, dim=1)
    print("Probabilities with +100 to logits (0,0):", shifted_probs[0].tolist(), "Sum:", shifted_probs[0].sum().item())

if __name__ == "__main__":
    print("--- Activation Experiment ---")
    for act in ['sigmoid', 'tanh', 'relu']:
        loss, correct, grad_norm, probs, preds = run_xor_experiment(act)
        print(f"Activation: {act:7s} | Final Loss: {loss:.4f} | 4/4 Correct? {correct} | Early Grad Norm: {grad_norm:.4f}")
        
    print("\n--- Symmetry Experiment (Zero Init with Tanh) ---")
    loss, correct, grad_norm, probs, preds = run_xor_experiment('tanh', zero_init=True)
    print(f"Final Loss: {loss:.4f} | 4/4 Correct? {correct}")
    
    run_multiclass_experiment()
