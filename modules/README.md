## Modules

SiteHost CLI relies on modules to provide the majority of its functionality. The code is modular and features can be provided or excluded if needed (e.g. Admin features). This also makes it easy to develop your own commands.

## Adding a new Module

Replace {New_Module_Name} with the uppercase version of the module name (e.g. "DNS") and {new_module_name} with the lower case of the module name (e.g. "dns"). You can autogenerate a customised version of the documentation for your module using sed like: 

```
sed 's/{New_Module_Name}/DNS/g;s/{new_module_name}/dns/g;' README.md
```

1. Copy the template file and update the Template name.

```
cd modules/
sed 's/template/{New_Module_Name}/gi' template.py > {new_module_name}.py
```

2. Add your commands:

You can add commands by either:

1. Adding additional commands to the `self._populate_command_array` call in the form of `additional_commands=[]`. These are fully featured commands and support suggestions and autocompletion out of the box.
2. Adding functions to the `{New_Module_Name}_Module` class with the prefix `_command_`. These commands suport suggestions but not autocompletion. The template format for these is:

```
def _command_{name}(self, args):
    """Helpful description.
    
    Usage: {name} arg1 arg2 arg3 (either_arg1|either_arg2) [optional_arg1] 
    """
    # Do operations here

    return # Any returned data will be ignored
```

3. Add module to `__init__.py`:

Add the following to the `__init__.py` file, which we will use to import the module. Importing this way avoids having to make any changes to the main executable file `main.py`.

```
from modules.{new_module_name} import {New_Module_Name}_Module
```

Then append to the __all__ dict:

```
__all__ = [..., ['{New_Module_Name}_Module']]
```