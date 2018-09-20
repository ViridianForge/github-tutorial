

from sys import path
from os.path import join, exists, dirname
path.insert(0, join(dirname(__file__),'..'))
import holyGrail
import pytest
import numpy as np

np.random.seed(42)

@pytest.mark.parametrize("elements,thesum", [
    ([1,2,3], 6),
    (['a', 'b', 'c'], 'abc')
])
def test_sum(elements, thesum):
    assert holyGrail.sum(elements) == thesum

@pytest.mark.parametrize("elements,themean,tol", [
    ([1, 2], 1.5, 1e-6),
    ((1e2+1.0*np.random.randn(1000)).astype(np.float16), 1e2, 0.1)
])
def test_mean(elements, themean, tol):
    ans = holyGrail.mean(elements)
    assert np.abs(ans-themean) < tol, ans
