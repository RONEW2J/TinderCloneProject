from rest_framework import serializers
from .models import Profile, Interest, Swipe
from django.contrib.auth import get_user_model

User = get_user_model()

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # Display username
    interests = InterestSerializer(many=True, read_only=False, queryset=Interest.objects.all())

    class Meta:
        model = Profile
        fields = ['user', 'age', 'location', 'interests'] # Add other fields as needed
        # For location, you might need a custom serializer field if using GeoDjango REST framework extensions

    def update(self, instance, validated_data):
        interests_data = validated_data.pop('interests', None)
        instance = super().update(instance, validated_data)
        if interests_data is not None:
            instance.interests.set(interests_data)
        return instance

# You'll create SwipeSerializer later when building swipe functionality