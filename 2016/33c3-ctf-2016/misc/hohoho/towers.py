def smove(a, b): # single move from a to b
    return str(a) + str(b)

def exch(n, a, b, c): # exchange nth disk b/w a and b
    if n == 0:
        return ''
    else:
        ret = ''
        ret += merge(n, a, b, c)
        ret += unmerge(n, b, a, c)
        return ret

def merge(n, a, b, c): # interlace n from a and b with a on bottom into c
    if n == 0:
        return ''
    else:
        ret = ''
        ret += merge(n-1, a, b, c)
        ret += move(2*(n-1), c, b, a)
        ret += smove(a, c)
        ret += move(2*(n-1), b, a, c)
        ret += smove(b, c)
        ret += move(2*(n-1), a, c, b)
        return ret

def unmerge(n, a, b, c): # exact opposite of merge(n, a, b, c)
    if n == 0:
        return ''
    else:
        ret = ''
        ret += move(2*(n-1), c, a, b)
        ret += smove(c, b)
        ret += move(2*(n-1), a, b, c)
        ret += smove(c, a)
        ret += move(2*(n-1), b, c, a)
        ret += unmerge(n-1, a, b, c)
        return ret

def move(n, a, b, c): # move exactly n disks from a to b using c (fragile)
    if n == 0:
        return ''
    else:
        ret = ''
        ret += move(n-1, a, c, b)
        ret += smove(a, b)
        ret += move(n-1, c, b, a)
        return ret

def wunmerge(n, a, b, c): # weird unmerge
    if n == 0:
        return ''
    else:
        ret = ''
        ret += move(2*(n-1), c, a, b)
        ret += smove(c, b)
        ret += move(2*(n-1), a, b, c)
        ret += smove(c, a)
        ret += move(2*(n-1), b, c, a)
        ret += wunmerge(n-1, b, a, c)
        return ret

def fixer(n, a, b, c): # fix it all :)
    return merge(n, b, a, c) + wunmerge(n, a, b, c)
