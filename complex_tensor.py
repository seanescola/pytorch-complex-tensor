import torch
import numpy as np
from torch import nn
from copy import deepcopy


"""
Complex tensor support for PyTorch.

Uses a regular tensor where the first half are the real numbers and second are the imaginary.

Supports only some basic operations without breaking the gradients for complex math.

Supported ops:
1. addition 
    - (tensor, scalar). Both complex and real.
2. subtraction 
    - (tensor, scalar). Both complex and real.
3. multiply
    - (tensor, scalar). Both complex and real.
4. mm (matrix multiply)
    - (tensor). Both complex and real.
5. abs (absolute value)
6. all indexing ops.
7. t (transpose)

>> c = ComplexTensor(10, 20)

>> #  do regular tensor ops now
>> c = c * 4
>> c = c.mm(c.t())
>> print(c.shape, c.size(0))
>> print(c)
>> print(c[0:1, 1:-1])
"""


class ComplexTensor(torch.Tensor):

    @staticmethod
    def __new__(cls, x, *args, **kwargs):
        if len(args) > 0:
            size_args = [2] + list(args)
            args = tuple(size_args)

        return super().__new__(cls, x, *args, **kwargs)

    def __deepcopy__(self, memo):
        if not self.is_leaf:
            raise RuntimeError("Only Tensors created explicitly by the user "
                               "(graph leaves) support the deepcopy protocol at the moment")
        if id(self) in memo:
            return memo[id(self)]
        with torch.no_grad():
            if self.is_sparse:
                new_tensor = self.clone()

                # hack tensor to cast as complex
                new_tensor.__class__ = ComplexTensor
            else:
                new_storage = self.storage().__deepcopy__(memo)
                new_tensor = self.new()

                # hack tensor to cast as complex
                new_tensor.__class__ = ComplexTensor
                new_tensor.set_(new_storage, self.storage_offset(), self.size(), self.stride())
            memo[id(self)] = new_tensor
            new_tensor.requires_grad = self.requires_grad
            return new_tensor

    @property
    def real(self):
        n, m = self.size()
        return self[:n//2]

    @property
    def imag(self):
        n, m = self.size()
        return self[n//2:]

    def __graph_copy__(self, real, imag):
        # return tensor copy but maintain graph connections
        # force the result to be a ComplexTensor
        result = torch.cat([real, imag], dim=0)
        result.__class__ = ComplexTensor
        return result

    def __add__(self, other):
        """
        Handles scalar (real, complex) and tensor (real, complex) addition
        :param other:
        :return:
        """
        real = self.real
        imag = self.imag

        # given a real tensor
        if type(other) is torch.Tensor:
            real = real + other

        # given a complex tensor
        elif type(other) is ComplexTensor:
            real = real + other.real
            imag = imag + other.imag

        # given a real scalar
        elif np.isreal(other):
            real = real + other

        # given a complex scalar
        else:
            real = real + other.real
            imag = imag + other.imag

        return self.__graph_copy__(real, imag)

    def __sub__(self, other):
        """
        Handles scalar (real, complex) and tensor (real, complex) addition
        :param other:
        :return:
        """
        real = self.real
        imag = self.imag

        # given a real tensor
        if type(other) is torch.Tensor:
            real = real - other

        # given a complex tensor
        elif type(other) is ComplexTensor:
            real = real - other.real
            imag = imag - other.imag

        # given a real scalar
        elif np.isreal(other):
            real = real - other

        # given a complex scalar
        else:
            real = real - other.real
            imag = imag - other.imag

        return self.__graph_copy__(real, imag)

    def __mul__(self, other):
        """
        Handles scalar (real, complex) and tensor (real, complex) multiplication
        :param other:
        :return:
        """
        real = self.real.clone()
        imag = self.imag.clone()

        # given a real tensor
        if type(other) is torch.Tensor:
            real = real * other
            imag = imag * other

        # given a complex tensor
        elif type(other) is ComplexTensor:
            ac = real * other.real
            bd = imag * other.imag
            ad = real * other.imag
            bc = imag * other.real
            real = ac - bd
            imag = ad + bc

        # given a real scalar
        elif np.isreal(other):
            real = real * other
            imag = imag * other

        # given a complex scalar
        else:
            ac = real * other.real
            bd = imag * other.imag
            ad = real * other.imag
            bc = imag * other.real
            real = ac - bd
            imag = ad + bc

        return self.__graph_copy__(real, imag)

    def mm(self, other):
        """
        Handles tensor (real, complex) matrix multiply
        :param other:
        :return:
        """
        real = self.real.clone()
        imag = self.imag.clone()

        # given a real tensor
        if type(other) is torch.Tensor:
            real = real.mm(other)
            imag = imag.mm(other)

        # given a complex tensor
        elif type(other) is ComplexTensor:
            ac = real.mm(other.real)
            bd = imag.mm(other.imag)
            ad = real.mm(other.imag)
            bc = imag.mm(other.real)
            real = ac - bd
            imag = ad + bc

        return self.__graph_copy__(real, imag)

    def t(self):
        real = self.real.t()
        imag = self.imag.t()

        return self.__graph_copy__(real, imag)

    def abs(self):
        result = torch.sqrt(self.real**2 + self.imag**2)
        return result

if __name__ == '__main__':
    c = ComplexTensor([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])
    c.requires_grad = True
    print(c.abs())
    print(c.size())

    x = torch.Tensor([[3, 3], [4, 4], [2, 2]])

    xy = c.mm(x)
    xy = xy.sum()

    xy.backward()
    print(c.grad)