def sum(s):
    if len(s) == 0: return None
    ans = s[0]
    for si in s[1:]:
        ans += si
    return ans

def mean(s):
    return sum(s)/len(s)
