from __future__ import print_function
import torch

# construct a 5x3 matrix, uninitialized
x = torch.empty(5, 3)
print(x)

# construct a randomly initialized matrix
x = torch.rand(5, 3)
print(x)

# construct a matrix filled zeros and of dtype long
x = torch.zeros(5, 3, dtype=torch.long)
print(x)

# construct a tensor directly from data
x = torch.tensor([5.5, 3])
print(x)

# create a tensor based on an existing tensor
x = x.new_ones(5, 3, dtype=torch.double)
print(x)

x = torch.randn_like(x, dtype=torch.float)
print(x)
print(x.size())

# addition
y = torch.rand(5, 3)
print(x + y)

print(torch.add(x, y))

result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)

y.add_(x)
print(y)