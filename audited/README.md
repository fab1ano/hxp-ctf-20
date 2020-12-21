audited
=======

Challenge description: 
```
Ceci n’est pas un sandbox.
```

* Category: pwn
* Difficulty: medium
* Points: TODO
* Author: `hlt`

Given files: `audited.py`, `ynetd`, `Dockerfile`

I solved this challenge with phi for team FAUST.

## Solution

The challenge provides us with a python audit hook sandbox.
We are able to provide python code, which is compiled and executed in an empty namespace (this means we have (almost) no local and global variables, see below).
However, our code is sandboxed with an audit hook:
```python
def audit(name, args):
    if not audit.did_exec and name == 'exec':
        audit.did_exec = True
    else:
        __exit(1)
audit.did_exec = False

[...]

sys.addaudithook(audit)
```

The `audit` function is now triggered at certain events (see full list [here](https://docs.python.org/3/library/audit_events.html)).
It only lets us execute `exec` once and exits if any function from the list of audit events is called after that (including `exec`).
Thus, we cannot execute any interesting functions like `os.exec` or `os.system`.
Also, `object.__getattr__` and `object.__setattr__` are on that list which makes code execution challenging.

But how do we execute code at all, if our namespace is empty?
Looking at the python documentation for `exec(object[, globals[, locals]])` reveals the following:
> If the globals dictionary does not contain a value for the key __builtins__, a reference to the dictionary of the built-in module builtins is inserted under that key.
Thus, we have the `__builtins__` module available.

Now, it might make sense to first import some important modules.
The loader provides us with that functionality:
```python
sys = __builtins__["__loader__"].load_module('sys')
gc = __builtins__["__loader__"].load_module('gc')
```

Given the module for garbage collection, we can also access all available objects with `gc.get_objects()` and search for other non-builtin modules like `os` and the `__main__` module which contains the code for `audit`.

At this point, I tried to replace the byte code of the function `audit` which didn't quite work out since `object.__getattr__` is also blocked by the sandbox.
The trick is to replace the `__exit` function in the module `__main__` with a different function, such that whenever the `audit` function tries to `__exit`, a different function is executed instead.
So we just replace `__exit` in the `__main__` module (`mod_main`):
```python
mod_main.__exit = lambda x : None
```

Now, the sandbox is effectively turnend off and we can easily call `os.system` to get the flag.

Flag: `hxp{m4yb3_b4by_sh0uld_h4v3_stuck_t0_pl4y1ng_1n_th3_s4ndb0x}`
