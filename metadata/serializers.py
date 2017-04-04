from marshmallow import Serializer


class KeyValueSerializer(Serializer):
    class Meta:
        fields = ('key', 'value',)
