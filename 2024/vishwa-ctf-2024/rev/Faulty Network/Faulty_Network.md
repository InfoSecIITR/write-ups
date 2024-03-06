## Faulty Network : 

We were given [chal.pth](chal.pth) and some basic code to define and load the pytorch model. 

```python
import torch
import torch.nn.functional as f

def tensorize(s : str):
  return torch.tensor([(1 if (ch >> i) & 1 == 1 else -1) for ch in list(map(ord, s)) for i in range(8)])

class NeuralNetwork(torch.nn.Module):
  def __init__(self, in_dimension, mid_dimension, out_dimension=1):
    super(NeuralNetwork, self).__init__()
    self.fc = torch.nn.Linear(in_dimension, mid_dimension)
    self.fc2 = torch.nn.Linear(mid_dimension, out_dimension)

  def step_activation(self, x : torch.Tensor) -> torch.Tensor:
    x[x <= 0] = -1
    x[x >  0] = 1
    return x

  def forward(self, x : torch.Tensor) -> int:
    x = self.fc(x)
    x = self.step_activation(x)
    x = self.fc2(x)
    x = self.step_activation(x)
    return int(x)


model = NeuralNetwork(128, 1024)
model.load_state_dict(torch.load("chal.pth"))

flag = ''

inp = tensorize(flag)

if model(inp) == 1 :
    print(flag)
```

### Going throught code 

* The tensorize function converts the flag string to bits where the bits are reversed and replaces all the 0s with -1s and returns a tensor. 

* Our goal is to find such string so that the result of the model is 1. 

* So my initial thought was to perform a data extraction attack on the model from which we can get back the input by performing a backprop. But the model is using step activation whose derivative is always 0, so all the gradients with respect to the input will be zeroed out, thus making no change in them while optimization.

* To counter this problem I replaced the step activation function with a similar function such that its derivative is non-zero, one such function is `tanh`.   

---

### Chain of attack 

1. Create a zero tensor of 128 length and set `requires_grad = True`
2. Set `model.requires_grad_(False)` 
3. Make a single forward pass and backprop using `MSE` loss 
4. The backprop will add small values in the input in the direction of actual input 
5. Since the input consists of only -1 and 1 set all positive values to one and negative values to -1 
6. Thus we obtain our input and convert it back to a string to get the flag 

---

### Final Code

```python
import torch
import torch.nn.functional as f

def tensorize(s : str):
  return torch.tensor([(1 if (ch >> i) & 1 == 1 else -1) for ch in list(map(ord, s)) for i in range(8)])

class NeuralNetwork(torch.nn.Module):
  def __init__(self, in_dimension, mid_dimension, out_dimension=1):
    super(NeuralNetwork, self).__init__()
    self.fc = torch.nn.Linear(in_dimension, mid_dimension)
    self.fc2 = torch.nn.Linear(mid_dimension, out_dimension)

  def step_activation(self, x : torch.Tensor) -> torch.Tensor:
    x[x <= 0] = -1
    x[x >  0] = 1
    return x

  def forward(self, x : torch.Tensor) -> int:
    x = self.fc(x)
    x = f.tanh(x) #replaced step activation with tanh
    x = self.fc2(x)
    x = f.tanh(x) #replaced step activation with tanh
    return x


model = NeuralNetwork(128, 1024)
model.load_state_dict(torch.load("chal.pth"))

#Zero tensor input
inp = torch.zeros((128)).float().unsqueeze(0)
inp.requires_grad_(True)

#Optimizing input
optimizer = torch.optim.Adam([inp], lr = 1e-2)
res = model(inp)
loss = f.mse_loss(res, torch.tensor([[1.]]))
optimizer.zero_grad()
loss.backward()
optimizer.step()

new = inp.detach()

new[new > 0] = 1
new[new <= 0] = 0

#tensor -> string
arr = list(map(str,new.int().tolist()[0]))
x = [''.join(arr[i:i+8]) for i in range(0, 128,  8)]
x = [int(i[::-1], 2) for i in x]


print("VishwaCTF{" + ''.join(chr(i) for i in x) + "}")
```

---  


Flag : `VishwaCTF{b4cktr4ck_4h34d_}` 

I even got first blood 🩸 on this challenge but unfortunately it was removed from the CTF :( 

