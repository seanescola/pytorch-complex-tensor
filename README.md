<p align="center">
<!--   <a href="https://williamfalcon.github.io/test-tube/">
    <img alt="react-router" src="https://raw.githubusercontent.com/williamfalcon/test-tube/master/imgs/test_tube_logo.png" width="50">
  </a> -->
</p>
<h3 align="center">
  Pytorch Complex Tensor
</h3>
<p align="center">
  Unofficial complex Tensor support for Pytorch 
</p>
<p align="center">
  <a href="https://badge.fury.io/py/pytorch_complex_tensor><img src="https://badge.fury.io/py/pytorch_complex_tensor.svg"></a>
  <a href="https://travis-ci.org/williamFalcon/pytorch-complex-tensor"><img src="https://travis-ci.org/williamFalcon/pytorch-complex-tensor.svg?branch=master"></a>
<!--   <a href="https://williamfalcon.github.io/test-tube/"><img src="https://readthedocs.org/projects/test-tube/badge/?version=latest"></a> -->
  <a href="https://github.com/williamFalcon/pytorch-complex-tensor/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>   


[![CircleCI](https://circleci.com/gh/williamFalcon/pytorch-complex-tensor/tree/master.svg?style=svg)](https://circleci.com/gh/williamFalcon/pytorch-complex-tensor/tree/master)

# pytorch-complex-tensor
torch.Tensor subclass to emulate complex linear algebra.   

Treats first half of tensor as real, second as imaginary.  A few arithmetic operations are implemented to emulate complex arithmetic.   

### Installation
```bash
pip install pytorch-complex-tensor
```

### Example:   
Easy import  
```python   
from pytorch_complex_tensor import ComplexTensor
```   

Init tensor
```
# equivalent to:
# np.asarray([[1+3j, 1+3j, 1+3j], [2+4j, 2+4j, 2+4j]]).astype(np.complex64)
C = ComplexTensor([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
C.requires_grad = True
```   

Pretty printing
```
print(C)
# tensor([['(1.0+3.0j)' '(1.0+3.0j)' '(1.0+3.0j)'],
#         ['(2.0+4.0j)' '(2.0+4.0j)' '(2.0+4.0j)']])
```

handles absolute value properly for complex tensors
```
# complex absolute value implementation
print(C.abs())
# tensor([[3.1623, 3.1623, 3.1623],
#         [4.4721, 4.4721, 4.4721]], grad_fn=<SqrtBackward>)
```


number of complex numbers is half of what it says here (printing WIP)
```
print(C.size())
# torch.Size([4, 3])
```

multiplies both complex and real tensors
```
# show matrix multiply with real tensor
# also works with complex tensor
x = torch.Tensor([[3, 3], [4, 4], [2, 2]])
xy = C.mm(x)
print(xy)
# tensor([['(9.0+27.0j)' '(9.0+27.0j)'],
#         ['(18.0+36.0j)' '(18.0+36.0j)']])
```

reduce ops return ComplexScalar
```
xy = xy.sum()

# this is now a complex scalar (thin wrapper with .real, .imag)
print(type(xy))
# pytorch_complex_tensor.complex_scalar.ComplexScalar

print(xy)
# (54+126j)
```

which can be used for gradients without breaking anything... (differentiates wrt the real part)
```
# calculate dxy / dC
# for complex scalars, grad is wrt the real part
xy.backward()
print(C.grad)
# tensor([['(6.0-0.0j)' '(8.0-0.0j)' '(4.0-0.0j)'],
#         ['(6.0-0.0j)' '(8.0-0.0j)' '(4.0-0.0j)']])
```



### Supported ops:
| Operation | complex tensor | real tensor | complex scalar | real scalar |
| ----------| :-------------:|:-----------:|:--------------:|:-----------:|   
| addition | Y | Y | Y | Y |
| subtraction | Y | Y | Y | Y |
| multiply | Y | Y | Y | Y |
| mm | Y | Y | Y | Y |
| abs | Y | - | - | - |
| t | Y | - | - | - |
| grads | Y | Y | Y | Y |   


