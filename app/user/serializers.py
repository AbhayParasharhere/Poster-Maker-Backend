"""
Serializer for the user api.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user api."""
    class Meta():
        model = get_user_model()
        fields = ['email', 'name', 'password',
                  'designation', 'contact_number', 'employee_id']
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 8},
                        'contact_number': {'max_length': 10}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
