from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "national_id")

    def validate_national_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError( "national_id must be only digit")
        if len(value) != 10:
            raise serializers.ValidationError("national_id is 10 digit")
            
        return value
