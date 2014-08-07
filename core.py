call = lambda f, *args, **kwargs: f(*args, **kwargs)

def dict_join(x, y):
    z = dict(x)
    z.update(y)
    return z

def _curry(args, kwargs, n, f):
  if len(args) >= n:
    return reduce(call, args[n:], f(*args[:n], **kwargs))
  else:
    return lambda *more_args, **more_kwargs: (
        _curry(args + more_args, dict_join(kwargs, more_kwargs), n, f))

curry = lambda f, *args, **kwargs: _curry(
    args,
    kwargs,
    # TODO: If f isn't a function, we assume its argcount is 1
    f.func_code.co_argcount if 'func_code' in dir(f) else 1,
    f)
