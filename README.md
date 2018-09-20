# Hands-on Introduction to the GitHub Work Flow

## Background

Your team is tasked with extending and rewriting the arithmetics library
`holy-grail`.  You think the problem can probably be handled by your two lead
programmers sir-robin and sir-lancelot.  They go to work immediately.

For the sake of this tutorial, you will wear both heads: that of lancelot and
robin who will work on different branches.  For this, you'll first need to
create two directories which we'll call `./lancelot/` and `./robin`.  Next,
**Please fork the project into your private repository**.  Let's say your
github account is called `camelot`.  I have made this repo public, so that you
are able to fork it seamlessly.  To fork, go to [the repo
page](https://github.com/BEL-CO/github-tutorial) and hit fork in the top task
list on the right.  For the rest of the tutorial you'll work on your private
fork, where you can commit to master without disturbing the others.  If you run
into bad trouble during the tutorial, just delete your private fork and fork
the BEL-CO one again.

## Story of Sir Lancelot `> cd lancelot`

Lancelot uses the command `git clone
https://github.com/camelot/github-tutorial.git` to get a local copy of the
repository on his local computer.  In the terminal, he runs

```> pytest```

executing all the four tests in the `./tests` repository and receives the
following error message:

```
elements = ['a', 'b', 'c'], thesum = 'abc'

    @pytest.mark.parametrize("elements,thesum", [
        ([1,2,3], 6),
        (['a', 'b', 'c'], 'abc')
    ])
    def test_sum(elements, thesum):
>       assert arithmetics.sum(elements) == thesum
E       TypeError: unsupported operand type(s) for +: 'int' and 'str'

tests/test\_adding.py:17: TypeError
================ 1 failed, 3 passed in 0.26 seconds =================
```

Immediately lancelot goes to the issues page of the github repository and
creates a new issue:

> **`sum` fails when adding strings**.
> 
> *It seems that builtin `sum` does not work well with strings, however, all
> other tests seem to run through smoothly.* 

This instantiates *Issue #1*.

sir-lancelot creates a new branch which he calls *fix-sum-of-strings*.  He
issues the command

```> git checkout -b fix-sum-of-strings```

The command puts him on a new branch which is an exact copy of the current
*master* branch.  He rewrites `./holyGrail/adding.py` which then reads

```
> cat ./holyGrail/adding.py
def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

def mean(s):
    return sum(s)/len(s)
```

He adds all changes, commits, and pushes them with

```
> git add ./holyGrail/adding.py```
> git commit -m "Added sum fn for strings."
> git push --set-upstream master fix-sum-of-strings
```

Note that `git commit` adds the commit permanently to his local branch,
but only `git push` will update (and even create) the remote branch with
the same name.  The key word `master` references the remote url, and
tells git about the repository where the new branch shall be created and
updated.

Content with himself, lancelot goes to lunch.

## Story of Sir Robin `> cd robin`

Having gone to the same ivy-league school as lancelot, Sir Robin takes
similar initial steps

```
> git clone https://github.com/camelot/github-tutorial.git
> pytest
> git checkout -b fix-strings-sum
```

He then goes on to do the exact same changes as lancelot, but he also reruns
the test leading him to the following discovery:

```
elements = array([100.5 ,  99.9 , 100.6 , 101.5 ,  99.75,  99.75, 101.56, 100.75,
        99.5 , 100.56,  99.56,  99.56, 100.25, ...5, 100.  , 100.2 ,  97.94,
        99.75,  99.3 ,  99.  ,  99.75, 101.8 , 100.6 ,  99.44, 100.56],
      dtype=float16)
themean = 100.0, tol = 0.1

    @pytest.mark.parametrize("elements,themean,tol", [
        ([1, 2], 1.5, 1e-6),
        ((1e2+1.0*np.random.randn(1000)).astype(np.float16), 1e2, 0.1)
    ])
    def test_mean(elements, themean, tol):
        ans = holyGrail.mean(elements)
>       assert np.abs(ans-themean) < tol, ans
E       AssertionError: inf
E       assert inf < 0.1
E        +  where inf = <ufunc 'absolute'>((inf - 100.0))
E        +    where <ufunc 'absolute'> = np.abs

tests/test\_holyGrail.py:25: AssertionError
========================================= warnings summary ==========================================
tests/test\_holyGrail.py::test\_mean[elements1-100.0-0.1]
  /home/jus/Code/belco/github-tutorial/tests/../holyGrail/\_\_init\_\_.py:8: RuntimeWarning: overflow encountered in half_scalars
    ans += si

-- Docs: http://doc.pytest.org/en/latest/warnings.html
========================== 1 failed, 3 passed, 1 warnings in 0.05 seconds ===========================
```

Sir Robin is furious, and bravely skips lunch to churn out the following
code which now passes all tests:

```
> cat ./holyGrail/adding.py
_import numpy as np_

def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

_def mean(s):
    return sum(np.asarray(s, dtype=np.float64))/len(s)_

> git add ./holyGrail/adding.py
> git commit -m "Added string sum and fixed mean."
> git push --set-upstream master fix-strings-sums
```

He checks everything three times and merges the changes into the master
branch (on the github interface).  Exhausted, Sir Robin falls asleep.  Note
that he could have done 

```
> git checkout master
> git merge fix-strings-sums
> git push
```

## Lancelot Conflicting Robin `> cd lancelot`

Sir Lancelot is back from lunch, runs pytest and discovers the failing
`mean` function.  Immediately he goes to work, but he's quite a bit
smarter than robin.  Instead of introducing a new dependency he writes

```
> cat ./holyGrail/adding.py

builtinSum = sum

def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

def mean(s):
    return builtinSum(s)/len(s)

> git add ./holyGrail/adding.py
> git commit -m "Fixed error in mean."
> git push --set-upstream master fix-sum-of-strings
```

When lancelot enters `git status`, he notices that `master` is two
commits behind `fix-sum-of-strings`, but also one commit ahead.  He
prays to god that there's no conflict.

## Lancelot Rebasing
