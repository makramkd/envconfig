import os
import unittest

import envconfig
from envconfig.lib import EnvconfigException


class TestEnvconfig(unittest.TestCase):
    def tearDown(self):
        """
        Clean up env vars after each test so environment isn't polluted.
        TODO: perhaps a better way is to pass the environment dict to
        envconfig.process, and have it default to os.environ instead?
        """
        if 'NAME' in os.environ:
            del os.environ['NAME']
        if 'AGE' in os.environ:
            del os.environ['AGE']
        if 'IS_MARRIED' in os.environ:
            del os.environ['IS_MARRIED']

    def test_process_no_overrides(self):
        os.environ['NAME'] = 'Makram'
        os.environ['AGE'] = '25'
        os.environ['IS_MARRIED'] = 'false'

        class Environment:
            name: str
            age: int
            is_married: bool

        env = Environment()
        envconfig.process(env)

        self.assertEqual('Makram', env.name)
        self.assertEqual(25, env.age)
        self.assertFalse(env.is_married)

    def test_process_some_overrides(self):
        os.environ['NAME'] = 'Makram'
        os.environ['AGE'] = '28'
        os.environ['IS_MARRIED'] = 'false'

        class Environment:
            name: str
            age: int = 25
            is_married: bool = True

        env = Environment()
        envconfig.process(env)

        self.assertEqual('Makram', env.name)
        self.assertEqual(28, env.age)
        self.assertFalse(env.is_married)

    def test_process_not_set(self):
        os.environ['NAME'] = 'Makram'
        os.environ['AGE'] = '28'

        class Environment:
            name: str
            age: int = 25
            is_married: bool # no default value and not overidden in env

        env = Environment()
        with self.assertRaises(EnvconfigException):
            envconfig.process(env)

    def test_process_not_set_no_raise_on_absence(self):
        os.environ['NAME'] = 'Makram'
        os.environ['AGE'] = '28'

        class Environment:
            name: str
            age: int = 25
            is_married: bool # no default value and not overidden in env

        env = Environment()
        envconfig.process(env, raise_on_absence=False)

        self.assertIsNone(env.is_married)
        self.assertEqual('Makram', env.name)
        self.assertEqual(28, env.age)

    def test_process_no_type_hint(self):
        os.environ['NAME'] = 'Makram'
        os.environ['AGE'] = '28'
        os.environ['IS_MARRIED'] = 'false'

        class Environment:
            name: str
            age = 25 # no type hint specified, but should still be processed as int
            is_married: bool = True

        env = Environment()
        envconfig.process(env)

        self.assertEqual('Makram', env.name)
        self.assertEqual(28, env.age)
        self.assertFalse(env.is_married)

    def test_process_prefix_set(self):
        os.environ['PERSON_NAME'] = 'Makram'
        os.environ['PERSON_AGE'] = '28'
        os.environ['PERSON_IS_MARRIED'] = 'false'

        class Environment:
            name: str
            age = 25 # no type hint specified, but should still be processed as int
            is_married: bool = True

        env = Environment()
        envconfig.process(env, prefix='person')

        self.assertEqual('Makram', env.name)
        self.assertEqual(28, env.age)
        self.assertFalse(env.is_married)
