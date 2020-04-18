import inspect
from typing import get_type_hints, Dict, Any, AnyStr
import os
import logging

from distutils.util import strtobool  # For casting to bool


def process(env: Any,
            raise_on_absence=True,
            prefix=''):
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

    Parameters
    ----------
    env: object
        The object to load the environment into.

    raise_on_abscence: bool
        If set to True, raise an exception if an environment variable is type annotated
        in the given object's class, but not set in the environment. If set to False,
        this attribute is simply set to None. Defaults to True.

    prefix: str
        Load environment variables with the given string prepended to the attribute names.
        For example, if an attribute `name: str` is defined, and the given prefix is `'person'`,
        then we load the environment variable `PERSON_NAME` instead of just `NAME`. Defaults to
        the empty string - i.e, no prefix.
    """
    attributes, hints, members = _get_attributes(env)

    # Iterate over attributes, look up env, and set attribute
    for attribute in attributes:
        env_var = os.getenv(_get_env_var_name(prefix, attribute))
        _process_env_var(
            attribute=attribute,
            env_var=env_var,
            hints=hints,
            members=members,
            env=env,
            raise_on_absence=raise_on_absence,
        )


def _get_env_var_name(prefix: str, attribute: str):
    # Prepend the given given prefix and an underscore if a prefix is set.
    # Otherwise, just use the attribute name.
    return prefix.upper() + '_' + attribute.upper() if prefix != '' else attribute.upper()


def _get_attributes(obj: Any):
    """
    Get the attributes of the given object that are relevant to envconfig's usage.

    In particular, we get all attributes that are defined explicitly using assignment,
    and all attributes that are only ever type-hinted, and combine these attributes
    into a single set to return.

    Parameters
    ----------
    obj: Any
        Any Python object.

    Returns
    -------
    attributes: set
        A set of attributes (represented as strings) that are deemed to be of importance
        for environment variable loading.

    hints: Dict[AnyStr, Any]
        A dictionary that maps the attribute name to the type hint, if provided.

    members: Dict[AnyStr, Any]
        A dictionary that maps the attribute name to the value, if provided.
    """
    hints: Dict[AnyStr, Any] = get_type_hints(obj)
    members = inspect.getmembers(
        obj,
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
    return attributes, hints, members


def _process_env_var(attribute, env_var, hints, members, env, raise_on_absence):
    if env_var:
        # Check if a type hint is available. If so, cast to that type.
        type_ = hints.get(attribute)
        if type_:
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
                raise EnvconfigException(f'No default value provided and no env var'
                                            f' set for {attribute} (env var: {env_var})')
            else:
                logging.getLogger().warning(f'No default value provided and no env var'
                                            f' set for {attribute} (env var: {attribute.upper()})')
                logging.getLogger().warning(f'Setting value to None')
                setattr(env, attribute, None)


class EnvconfigException(Exception):
    """
    Base class for all envconfig exceptions.
    """
    pass
