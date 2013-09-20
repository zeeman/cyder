from rest_framework import serializers, viewsets


NestedKeyValueFields = ['id', 'key', 'value', 'is_quoted']


class NestedFieldSerializer(serializers.ModelSerializer):
    """Custom API serializer to handle nested many-to-many fields because DRF
    is kind of dumb and tries to do Domain(..., ctnr_set=things). To use this
    serializer, you should add an attribute to your serializer's Meta class
    called `nested_fields` containing a list of string names of many-to-many
    fields in the serializer's model.
    """
    def restore_object(self, attrs, instance=None, *args, **kwargs):
        """This method does all the work of creating an object representation
        of the serialized data and saving it/modifying the existing object.

        Params:
            attrs - A dict of the data sent to the API. Objects passed as links
                    are automatically turned into object representations which
                    can be passed to Django directly.
            instance - If the request is trying to update an object, this
                       contains the object to be modified.
        """
        if not self.is_valid():
            return self.errors

        if instance is not None:
            # add nested values from many-to-fields as appropriate
            if getattr(self.Meta(), 'nested_fields', None):
                for nested_field in self.Meta().nested_fields:
                    if nested_field in attrs:
                        for item in attrs.pop(nested_field):
                            getattr(self.instance, nested_field).add(item)
            for field in self.fields:
                if field in self.Meta().nested_fields:
                    continue
                setattr(instance, field, attrs.get(
                    field, getattr(instance, field)))
            instance.save()
            return instance

        if getattr(self.Meta(), 'nested_fields', None):
            nested_fields = {}
            for nested_field in self.Meta().nested_fields:
                if nested_field in attrs:
                    nested_fields[nested_field] = attrs.pop(nested_field)
        instance = self.Meta().model(**attrs)
        instance.save()

        for nested_field in nested_fields:
            getattr(instance, nested_field).add(*nested_fields[nested_field])

        return instance

    def save_object(self, *args, **kwargs):
        """Normally this is used to save the object, but obviously that
        doesn't matter when we save in restore_object(). We're overriding
        this method to keep DRF from trying to save the already saved object.
        """
        pass


class CommonAPISerializer(serializers.ModelSerializer):
    pass


class CommonAPIMeta:
    pass


class CommonAPIViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        self.queryset = self.model.objects.all()
        super(CommonAPIViewSet, self).__init__(*args, **kwargs)
