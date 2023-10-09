"""
Serializer for the user api.
"""

from rest_framework import serializers

from django.utils.translation import gettext as _

from django.contrib.auth import (get_user_model,
                                 authenticate)


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


class UserTextDetailSerializer(serializers.ModelSerializer):
    """Serializer for handling requests to get and update \
    user detals."""
    class Meta():
        model = get_user_model()
        fields = ['name', 'password', 'email',
                  'designation', 'contact_number', 'employee_id']
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 8},
            'contact_number': {'max_length': 10}
        }

    def update(self, instance, validated_data):
        "Update method returns the validated user instance."
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        user = super().update(instance, validated_data)

        if email is not None:
            msg = _('Email cannot be modified or updated for an account.')
            raise serializers.ValidationError(
                msg, code='email_update_not_allowed')

        if password:
            user.set_password(password)
            user.save()

        return user


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for the image upload api."""
    class Meta():
        model = get_user_model()
        fields = ['background_image']
        extra_kwargs = {'background_image': {'required': 'True'}}


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate the attributes and
        put the authenticated user in the attrs
        and return the attributes."""
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(
            request=request,
            email=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate the user \
                with the given credentials')
            raise serializers.ValidationError(msg, code="authorization")

        attrs['user'] = user
        return attrs
