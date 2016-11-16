from rest_framework import serializers
from .models import DataSource, Event, Variable, VarValue


class DataSourceSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    label = serializers.CharField(required=False, allow_blank=True,max_length=50)
    description = serializers.CharField(required=False, allow_blank=True,max_length=250)
    source_id = serializers.UUIDField(format='hex_verbose', required=False)

    def create(self, validated_data):
        """
        Create and return a new `DataSource` instance, given the validated data.
        """
        return DataSource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `DataSource` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.label = validated_data.get('label', instance.label)
        instance.description = validated_data.get('description', instance.description)
        instance.source_id = validated_data.get('source_id', instance.source_id)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.edition_date = validated_data.get('edition_date', instance.edition_date)
        
        instance.save()
        return instance

# class DataSourceSerializer(serializers.Serializer):
#     class Meta:
#         model = DataSource
#         fields = ('name', 'label')#, 'description', 'source_id', 'create_date','edition_date')

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('name', 'unit', 'description', 'icon', 'var_id','data_source')



class VarValueSerializer(serializers.Serializer):
    value = serializers.FloatField(required=True)
    timestamp = serializers.DateTimeField(required=False)
    var_id = serializers.UUIDField(format='hex_verbose', required=False)
    #location = serializers.CharField(max_length=100)
    #variable = models.ForeignKey(Variable, on_delete=models.CASCADE)

    def create(self, validated_data):
        """
        Create and return a new `DataSource` instance, given the validated data.
        """
        
        return VarValue.objects.create(**validated_data)