#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utility functions decorators for Maya
"""

from __future__ import print_function, division, absolute_import

from functools import wraps
import os
import sys
import time
import inspect
import traceback

import tpPyUtils
from tpPyUtils import debug


def abstractmethod(fn):
    """
    The decorated function should be overridden by a software specific module.
    """

    def new_fn(*args, **kwargs):
        msg = 'Abstract implementation has not been overridden.'
        mode = os.getenv('RIGLIB_ABSTRACTMETHOD_MODE')
        if mode == 'raise':
            raise NotImplementedError(debug.debug_object_string(fn, msg))
        elif mode == 'warn':
            print(debug.debug_object_string(fn, msg))
        return fn(*args, **kwargs)

    new_fn.__name__ = fn.__name__
    new_fn.__doc__ = fn.__doc__
    new_fn.__dict__ = fn.__dict__
    return new_fn


def accepts(*types, **kw):
    """
    Function decorator that checks if decorated function arguments are of the expected types
    :param types: Expected types of the inputs to the decorated function. Must specify a type for each parameter
    :param kw: (optional) Specification of 'debug' level ( 0 | 1 | 2 )
    """

    if not kw:
        debug = 1
    else:
        debug = kw['debug']
    try:
        def decorator(f):
            def newf(*args):
                if debug is 0:
                    return f(*args)
                args = list(args)
                if not (len(args[1:]) == len(types)): raise AssertionError
                argtypes = tuple(map(type, args[1:]))
                if argtypes != types:
                    msg = debug.format_message(f.__name__, types, argtypes, 0)
                    if debug is 1:
                        try:
                            for i in range(1, len(args)):
                                args[i] = types[i - 1](args[i])
                        except ValueError as stdmsg:
                            raise ValueError(msg)
                        except TypeError as stdmsg:
                            raise TypeError(msg)
                    elif debug is 2:
                        raise TypeError(msg)
                return f(*args)
            newf.__name__ = f.__name__
            return newf
        return decorator
    except KeyError as key:
        raise KeyError(key + 'is not a valid keyword argument')
    except TypeError as msg:
        raise TypeError(msg)


def returns(ret_type, **kw):
    """
    Function decorator that checks if decorated function return value is of the expected type
    :param retType: Excepted type of the decorated function return value. Must specify type for each parameter
    :param kwargs: (optional) Specification of 'debug' level (0 | 1 | 2)
    """

    try:
        if not kw:
            debug = 1
        else:
            debug = kw['debug']
        def decorator(f):
            def newf(*args):
                result = f(*args)
                if debug is 0:
                    return result
                res_type = type(result)
                if res_type != ret_type:
                    msg = debug.format_message(f.__name__, (ret_type,), (res_type,), 1)
                    if debug is 1:
                        try:
                            result = ret_type(result)
                        except ValueError:
                            raise ValueError
                    elif debug is 2:
                        raise TypeError(msg)
                return result
            newf.__name__ = f.__name__
            return newf
        return decorator
    except KeyError as key:
        raise KeyError(key + 'is not a valid keyword argument')
    except TypeError as msg:
        raise TypeError(msg)


def timer(fn):
    """
    Function decorator for simple timer
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if tpPyUtils.logger.getEffectiveLevel() == 20:
            # If we are in info mode we disable timers
            res = fn(*args, **kwargs)
        else:
            t1 = time.time()
            res = fn(*args, **kwargs)
            t2 = time.time()

            trace = ''
            try:
                mod = inspect.getmodule(args[0])
                trace += '{0} >>'.format(mod.__name__.split('.')[-1])
            except:
                tpPyUtils.logger.debug('function module inspect failure')

            try:
                cls = args[0].__clas__
                trace += '{0}.'.format(args[0].__clas__.__name__)
            except:
                tpPyUtils.logger.debug('function class inspect failure')

            trace += fn.__name__
            tpPyUtils.logger.debug('Timer : %s: took %0.3f ms' % (trace, (t2 - t1) * 1000.0))
        return res
    return wrapper


def print_elapsed_time(f):
    """
    Function decorator that gets the elapsed time
    :param f: fn, function
    """

    def decorator(f):
        def newf(*args):
            t = time.time()
            f(*args)
            print(f.__name__, time.time() - t)
        newf.__name__ = f.__name__
        return newf
    return decorator(f)


def timestamp(f):
    """
    Function decorator that gets the elapsed time with a more descriptive output
    :param f: fn, function
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        print('<' + f.func_name + '> Elapsed time :', time.time() - start_time)
    return wrapper


def try_pass(fn):
    """
    Function decorator that tries a function and if it fails pass
    :param fn: function
    """

    def wrapper(*args, **kwargs):
        return_value = None
        try:
            return_value = fn(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
        return return_value
    return wrapper


def empty_decorator(f):
    """
    Empty decorator
    :param f: fn
    """

    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        return r
    return wrapper
