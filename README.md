# A Tale of GitHub

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

sir-lancelot creates a new branch which he calls *fix-lancelot*.  He
issues the command

```> git checkout -b fix-lancelot```

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
> git commit -m "Fixed sum."
> git push --set-upstream origin fix-lancelot
```

Note that `git commit` adds the commit permanently to his local branch,
but only `git push` will update (and even create) the remote branch with
the same name.  The remote url id `origin` references the remote url, and
tells git about the repository where the new branch shall be created and
updated.

Content with himself, lancelot goes to lunch.

## Story of Sir Robin `> cd robin`

Having gone to the same ivy-league school as lancelot, Sir Robin takes
similar initial steps

```
> git clone https://github.com/camelot/github-tutorial.git
> pytest
> git checkout -b fix-robin
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
import numpy as np

def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

def mean(s):
    return sum(np.asarray(s, dtype=np.float64))/len(s)

> git add ./holyGrail/adding.py
> git commit -m "Fixed sum and mean."
> git push --set-upstream master fix-robin
```

He checks everything three times and merges the changes into the master
branch (on the github interface).  Exhausted, Sir Robin falls asleep.  Note
that he could have done 

```
> git checkout master
> git merge fix-robin
> git push
```

## Story of Sir Lancelot continued `> cd lancelot`

### Sir Lancelot discovers the Error

Sir Lancelot is back from lunch, runs `pytest` and discovers the failing `mean`
function that he had missed before.  Immediately he goes to work, but he's
quite a bit smarter than robin.  Instead of introducing a new dependency on
`numpy` he writes

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
> git commit -m "Fixed mean."
> git push --set-upstream master fix-lancelot
```

### Lancelot is squashing it

Lancelot noticed that there are new commits in `origin/master`.  He prays to
god that there's no conflict, but we all know there is; there always is.  Sir
Lancelot checks diff of his own branch after updating his local master:

```
> git checkout master
> git pull
> git checkout fix-lancelot
> git diff master
diff --git a/holyGrail/adding.py b/holyGrail/adding.py
index 0af146f..f85057b 100644
--- a/holyGrail/adding.py
+++ b/holyGrail/adding.py
@@ -1,5 +1,5 @@
 
-import numpy as np
+builtinSum = sum
 
 def sum(s):
     if len(s) == 0: return None
@@ -9,4 +9,4 @@ def sum(s):
     return ans
 
 def mean(s):
-    return sum(np.asarray(s, dtype=np.float64))/len(s)
+    return builtinSum(s)/len(s)
```

He doesn't know what all of this means, but it seems like there's now a
conflict between his branch and the current master.  He will need to resolve
the conflict.

Sir Lancelot knows that conflict resolution is hard if you have lots of
commits that need to be replayed on top of the new master.  Therefore,
he first cleans up his own branch by squashing the last two commits into
one.  He does:


```
> git rebase -i HEAD~2
# An editor opens ..
1  pick 9666fbe Fix sum.
2  pick 7ebc6dd Fix mean.
3  
# .. lancelot changes it to ..
1  pick 9666fbe Fix sum.
2  squash 7ebc6dd Fix mean.
3  
# .. saves and quits.
# Another editor opens ..
1  # This is a combination of 2 commits.
2  # The first commit's message is:
3  
4  Fix sum.
5  
6  # This is the 2nd commit message:
7  
8  Fix mean.
9  
# .. lancelot changes it to ..
1  Fixed without numpy.
2
# .. saves and quits.
> git log
commit 46d5b55424798a7b0f7991af3ac19da775bb3972
Author: lancelot <lancelot@camelot.uk.co>
Date:   Fri Sep 21 05:12:52 2018 -0700

    Fix without numpy.

```

He notice that the two commits have been replaced by a single one.
Running `git status` he recieves
```
On branch fix-lancelot
Your branch and 'origin/fix-lancelot' have diverged,
and have 1 and 2 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)
nothing to commit, working directory clean
```

This is a dangerous state of divergence.

### Lancelot faces his Conflicts

Sir Lancelot knows there's no turning back now.  Bravely he enters

```
> git rebase master
First, rewinding head to replay your work on top of it...
Applying: Fix without numpy.
Using index info to reconstruct a base tree...
M	holyGrail/adding.py
Falling back to patching base and 3-way merge...
Auto-merging holyGrail/adding.py
CONFLICT (content): Merge conflict in holyGrail/adding.py
error: Failed to merge in the changes.
Patch failed at 0001 Fix without numpy.
The copy of the patch that failed is found in: .git/rebase-apply/patch

When you have resolved this problem, run "git rebase --continue".
If you prefer to skip this patch, run "git rebase --skip" instead.
To check out the original branch and stop rebasing, run "git rebase --abort".
> cat holyGrail/adding.py
<<<<<<< 1dbed3799ec3fc2b0eee1bc7c2355ce3c8802816
import numpy as np
=======
ssum = sum
>>>>>>> Fix without numpy.

def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

def mean(s):
<<<<<<< 1dbed3799ec3fc2b0eee1bc7c2355ce3c8802816
    return sum(np.asarray(s, dtype=np.float64))/len(s)
=======
    return ssum(s)/len(s)
>>>>>>> Fix without numpy.
```

The file `holyGrail/adding.py` has additional lines that are not python code.
`<<< ...` indicate conflicting parts in Sir Robin's remote commit that has been
played onto the file, `=====` the end of that commit's changes and the
beginning of how the file logs in lancelot's branch, and `>>>> Fix...` the end
of that.  Lancelot just deletes everything between `<<<` and `>>>`, so that
only his own code is left.  Lancelot tries to continue:

```
> git rebase --continue
Applying: Fix without numpy.
```

This could have been way more complicated without the squashing in the
beginning.

### Lancelot merges to master

First lancelot pushes his diverged branch forcefully `-f` onto his
remote branch `origin/fix-lancelot`.

```
> git push -f
```

Online, the network now shows a linear history with his branch being one
step ahead of master.  Perfect.  Finally he can merge his branch:

```
> git checkout master
> git merge fix-lancelot
> git push
```

THE END!
