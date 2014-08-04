import cqlengine
from cqlengine.models import ModelMetaClass


MODEL_REGISTRY = {}

class BaseModelMeta(ModelMetaClass):
    """
    A metaclass implementation that extends cqlengine.models.ModelMetaClass and keeps a registry of cqlengine model
    classes so that we can easily discover and operate on them. The current use case for this is swapping out the
    keyspace during test suite runs.
    """

    def __new__(meta, class_name, bases, new_attrs):
        cls = ModelMetaClass.__new__(meta, class_name, bases, new_attrs)
        if not new_attrs.get('__abstract__'):
            MODEL_REGISTRY[class_name] = cls

        return cls


class BaseModel(cqlengine.Model):
    """
    Provides default cqlengine configuration for models project wide.
    """

    __abstract__ = True

    __metaclass__ = BaseModelMeta