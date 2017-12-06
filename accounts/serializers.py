# -*- coding: UTF-8 -*-
from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.serializers import api_settings as jwt_settings
from django.utils.translation import ugettext as _

User = get_user_model()
jwt_payload_handler = jwt_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = jwt_settings.JWT_DECODE_HANDLER


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    token = serializers.SerializerMethodField(read_only=True)
    captcha_val = serializers.CharField(max_length=128, required=True, write_only=True)
    captcha_key = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'token',
            'captcha_val',
            'captcha_key',
        )

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.password = make_password(validated_data['password'])  # hash password
        user.save()
        return user

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        return jwt_encode_handler(payload)


class UserLoginSerializer(JSONWebTokenSerializer, serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    id = serializers.CharField(allow_blank=True, read_only=True)
    # captcha_val = serializers.CharField(max_length=128, required=True, write_only=True)
    # captcha_key = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'token',
            # 'captcha_val',
            # 'captcha_key',
        )
        extra_kwargs = {"password": {"write_only": True}}

    # check user auth
    def validate(self, data):

        # check user auth
        credentials = {
            self.username_field: data.get(self.username_field),
            'password': data.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                # payload = jwt_payload_handler(user)
                user.last_login = timezone.now()
                user.save()
                # return {
                #     'token': jwt_encode_handler(payload),
                #     'user': user
                # }
                return user
            else:
                if User.objects.filter(username=data.get(self.username_field)).first() is None:
                    msg = _('This user account does not exist.')
                    raise serializers.ValidationError(msg)
                else:
                    msg = _('Incorrect password.')
                    raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        return jwt_encode_handler(payload)


class CapthaValueSerializer(serializers.Serializer):
    val = serializers.CharField(max_length=128, required=True)
    hashKey = serializers.CharField(max_length=128, required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass