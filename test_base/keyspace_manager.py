from unittest import TestCase
from cqlengine.exceptions import CQLEngineException
from cqlengine.management import create_keyspace
from cqlengine.management import delete_keyspace
from cqlengine.management import sync_table


class TestKeyspaceManager(object):
    """
    Manages creating and cleaning a keyspace specifically for tests. This allows us to isolate the impact of running
    our tests and prevents the database from leaking resources over time as we continually run the test suite. In order
    for this to work we are dependant on all of models inheriting from test_base.models.BaseModel which does self
    registration that allows discovery of all cqlengine model classes.
    """

    # Class level flag for whether a clean keyspace has already been created.
    _KEYSPACE_CREATED = False

    # The name of the test keyspace to be cleaned and recreated. Using a hardcoded value so that the keyspace is the
    # same across test suite runs allowing us to clean on subsequent run since we don't have a great way of hooking
    # into the end of a test suite run.
    _KEYSPACE_NAME = 'cqletestsuite'

    # Keep track of tables that have already been synced in this keyspace.
    _SYNCED_TABLES = {}

    @classmethod
    def setup_keyspace(cls):
        # Import the current model registry.
        from test_base.models import MODEL_REGISTRY

        if not cls._KEYSPACE_CREATED:
            # We have not re-generated the keyspace yet.

            # First we clean out the old one if it exists.
            delete_keyspace(cls._KEYSPACE_NAME)

            # Create the fresh test keyspace.
            try:
                create_keyspace(cls._KEYSPACE_NAME)
                cls._KEYSPACE_CREATED = True
            except CQLEngineException as exc:
                print "Error creating test keyspace. {}".format(exc)

        # Sync each model in the registry into the new keyspace.
        for model_cls_name, model_cls in MODEL_REGISTRY.items():
            if model_cls_name not in cls._SYNCED_TABLES:
                model_cls.__keyspace__ = cls._KEYSPACE_NAME
                sync_table(model_cls)
                cls._SYNCED_TABLES[model_cls_name] = model_cls


class PersistenceTestCase(TestCase):
    """
    A base unittest.TestCase implementation which makes use of the TestKeyspaceManager in order to isolate the C*
    keyspace used during test suite runs.
    """

    @classmethod
    def setUpClass(cls):
        TestKeyspaceManager.setup_keyspace()
        super(PersistenceTestCase, cls).setUpClass()
