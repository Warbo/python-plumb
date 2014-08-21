from core import curry

def build():
  def call(env):
    return lambda func, arg: curry(func)(interpret(env, arg))

  def interpret(env, x):
    funcs = {int:   lambda a, b: env[x],
             list:  plumb,
             tuple: chain}
    if type(x) in funcs:
      return funcs[type(x)](env, x)
    return x

  def chain(env, calls):
    return reduce(call(env), calls, lambda x: x)

  def plumb_(env, expr, arg):
    if len(expr) is 0:
      return arg
    return chain([arg] + env, expr)

  plumb = curry(plumb_)

  return curry(lambda expr: plumb([], expr))

plumb = build()
del(build)
