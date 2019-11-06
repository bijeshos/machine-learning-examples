import torch

# create a tensor and set parameter to track computation with it
x = torch.ones(2, 2, requires_grad=True)
print(x)

# perform a tensor operation
y = x + 2
print(y)
print(y.grad_fn)

# perform more operations
z = y * y * 3
out = z.mean()

print(z, out)

# check the flags
a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)

