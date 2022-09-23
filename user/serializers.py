from rest_framework import serializers
from .models import User as UserModel

class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"]) 
        if UserModel.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("중복된 email 존재합니다.")
        elif len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        elif len(data["username"]) < 4:
            raise serializers.ValidationError("username 4자 이상 입력해주세요")
        
        return data

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
    
    class Meta:
        model = UserModel
        fields = "__all__"