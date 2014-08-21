from random import randint

random = lambda _: randint(0, 1000)

test = lambda t: t(*map(random, range(t.func_code.co_argcount)))

def failures(ts):
    results = {n: test(t) for n, t in ts.iteritems()}
    return {n: (l, r) for n, (l, r) in results.iteritems() if l != r}

def show(ts):
    if len(ts) > 0:
        print ts
        return
    print "Passed"

from core import *

core_fails = show(failures({
    'currying curries': lambda a, b: (
        curry(lambda x, y: x + y)(a)(b),
        a + b),

    'curried functions still callable as normal': lambda a, b: (
        curry(lambda x, y: x + y)(a, b),
        a + b),

    'currying uncurries': lambda a, b, c: (
        curry(lambda x, y: lambda z: x + y + z)(a, b, c),
        a + b + c),

    'can curry types': lambda a: (
        curry(str)(a),
        str(a)),

    'curry passes on keywords': lambda a, b: (
        curry(lambda x, **kwargs: map(str, kwargs.iteritems()),
              foo=a)(b),
        [str(('foo', a))]),

    'curry ignores defaults': lambda a, b, c: (
        curry(lambda x, y=a: x + y, b, c),
        b + c)
}))

from plumb import *

plumb_fails = show(failures({
    'plumb thunks': lambda a, b: (
        plumb([str(a)])(b),
        str(a)),

    'plumb id': lambda a: (
        plumb([])(a),
        a),

    'plumb id 2': lambda a: (
        plumb([0])(a),
        a),

    'plumb de Bruijn': lambda a: (
        plumb([[1 , 0]])(str, a),
        str(a)),

    'plumb curries': lambda a, b: (
        plumb([[[2 , 1 , 0]]])(lambda x, y: x + y, a, b),
        a + b),

    'plumb uncurries': lambda a: (
        plumb([str , 0], a),
        str(a))
}))
