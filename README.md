===================
cqlengine-test-base
===================

An implementation of unittest.TestCase which provides management and cleanup of Cassandra keyspaces through cqlengine.

Each run of the test suite will be executed in a clean/empty keyspace so that test runs do not leak over time.

Usage
=====

```
from test_base.models import BaseModel

class MyModel(BaseModel):
   ...
   

from test_base import PersistenceTestCase

class MyModelUnitTests(PersistenceTestCase):

    def test_my_model(self):
        ...
```