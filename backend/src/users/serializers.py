from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("id", "email", "is_active")

    # def validate_email(self, value):
    #    user = self.context['request'].user
    #    if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #        raise serializers.ValidationError({
    #            "email": "This email is already in use."
    #        })
    #    return value

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.is_active = validated_data["is_active"]
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",
                }
            )
        return attrs

    # def validate_old_password(self, value):
    #    user = self.context['request'].user
    #    if not user.check_password(value):
    #        raise serializers.ValidationError({
    #            "old_password": "Old password is not correct"
    #        })
    #    return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
