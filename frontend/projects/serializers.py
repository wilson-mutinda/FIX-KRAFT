from rest_framework import serializers

from .models import Projects


class ProjectSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(
        required=False
    )

    class Meta:
        model = Projects

        fields = '__all__'

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        request = self.context.get('request')

        if instance.image and request:

            representation['image'] = request.build_absolute_uri(
                instance.image.url
            )

        return representation