from random import randint

random = lambda _: randint(0, 1000)

test = lambda t: t(*map(random, range(t.func_code.co_argcount)))

def failures(ts):
    results = {n: test(t) for n, t in ts.iteritems()}
    return {n: r for n, r in results.iteritems() if r}

from core import *

core_fails = failures({
    'currying curries': lambda a, b: (
        curry(lambda x, y: x + y)(a)(b) != a + b),
    'curried functions still callable as normal': lambda a, b: (
        curry(lambda x, y: x + y)(a, b) != a + b),
    'currying uncurries': lambda a, b, c: (
        curry(lambda x, y: lambda z: x + y + z)(a, b, c) != a + b + c),
    'can curry types': lambda a: (
        curry(str)(a) != str(a)),
    'curry passes on keywords': lambda a, b: (
        curry(lambda a, **kwargs: [str(x) for x in kwargs.iteritems()],
              foo=a)(b) != [str(('foo', a))])
})

from plumb import *

plumb_fails = failures({
    'plumb thunks': lambda a, b: (
        plumb([str(a)])(b) != str(a)),
    'plumb id': lambda a: (
        plumb([0])(a) != a),
    'plumb de Bruijn': lambda a: (
        plumb([[1 , 0]])(str, a) != str(a)),
    'plumb curries': lambda a, b: (
        plumb([[[2 , 1 , 0]]])(lambda x, y: x + y, a, b) != a + b),
    'plumb uncurries': lambda a: (
        plumb([str , 0], a) != str(a))
})
