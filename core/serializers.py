from rest_framework import serializers


class SignedCertSerializer(serializers.Serializer):

    domain = serializers.CharField()
    ca_password = serializers.CharField()
