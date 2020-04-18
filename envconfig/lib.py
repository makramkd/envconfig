import inspect
from typing import get_type_hints, Dict, Any, AnyStr
import os
import logging

from distutils.util import strtobool # For casting to bool


def process(env, raise_on_absence=True):
    """
    Given an object that has members defined with type hints,
    load environment variables with the name of these members.

    For example, given this class:
    ```python
    class Environment:
        name: str     # No default, read from env
        age: int = -1 # A default is provided
    ```
    We can then load the environment variables like so:
    ```python
    env = Environment()
    envconfig.process(env)
    ```

    We will look for the environment variables 'NAME' and 'AGE',
    and cast those to the appropriate type and set them as the values
    for the attributes of the class, if available. Otherwise, that
    attribute is set to the default if it's provided.

    Members of the class that are defined with a leading underscore, such
    as `_name`, are ignored.
    """
    # We have to cover the following cases:
    # 1. Type hint is provided.
    # 2. Type hint is not provided.
    # In the second case, we interpret the env var as a string and set the
    # attribute to a string.
    # Overriding behavior:
    # If an attribute is set to a value and we find an environment variable
    # corresponding to it, then we override the value with the value from the environment.
    hints: Dict[AnyStr, Any] = get_type_hints(env)
    members = inspect.getmembers(
        env,
        lambda m: not inspect.isroutine(m),
    )
    # Ignore members that start with underscores
    members = {
        key: value
        for (key, value) in members
        if not key.startswith('_')
    }
    # Construct the union of attributes that we got from both hints
    # and members
    attributes = set(members.keys()) | set(hints.keys())

    # Iterate over attributes, look up env, and set attribute
    for attribute in attributes:
        env_var = os.getenv(attribute.upper())
        if env_var:
            # Check if a type hint is available. If so, cast to that type.
            type_ = hints.get(attribute)
            if type_:
                # TODO: perhaps some more customization here (post-processing?)
                # after the env var is read other than this default behavior

                # bool is a special case
                if type_ is bool:
                    setattr(env, attribute, type_(strtobool(env_var)))
                else:
                    setattr(env, attribute, type_(env_var))
            else:
                # Otherwise, cast to the type that the attribute was initialized to
                type_ = type(members[attribute])
                setattr(env, attribute, type_(env_var))
        else:
            # Env var is not present - check if a default is specified
            default_val = members.get(attribute)
            if not default_val:
                # No default value available - raise if that kwarg is set
                if raise_on_absence:
                    raise EnvconfigException(f'No default value provided and no env var set for {attribute} (env var: {env_var})')
                else:
                    logging.getLogger().warning(f'No default value provided and no env var set for {attribute} (env var: {attribute.upper()})')
                    logging.getLogger().warning(f'Setting value to None')
                    setattr(env, attribute, None)



class EnvconfigException(Exception):
    pass
