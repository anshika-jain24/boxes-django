from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'area',
                  'volume', 'created_by', 'created_at', 'last_updated']
        read_only_fields = ['id', 'area', 'volume',
                            'created_by', 'created_at', 'last_updated']

    area = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    def get_area(self, obj):
        return obj.length * obj.breadth

    def get_volume(self, obj):
        return obj.length * obj.breadth * obj.height


class BoxSerializerNonStaff(BoxSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'area', 'volume']
        read_only_fields = ['id', 'area', 'volume']

    area = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    def get_area(self, obj):
        return obj.length * obj.breadth

    def get_volume(self, obj):
        return obj.length * obj.breadth * obj.height


class BoxCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['length', 'breadth', 'height']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class BoxUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height']
        read_only_fields = ['id', 'created_by', 'created_at']

    def update(self, instance, validated_data):
        instance.length = validated_data.get('length', instance.length)
        instance.breadth = validated_data.get('breadth', instance.breadth)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance
