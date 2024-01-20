from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from project_manager.models import Project, Task
from accounts.utils import get_role_db_value

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=False, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile_phone",
            "role",
            "password",
            "is_active",
            "creation_date",
            "last_update",
        )
        read_only_fields = ("id", "is_active", "creation_date", "last_update",)
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_role(self, role):
        if role not in ["Developer", "Project Manager"]:
            raise serializers.ValidationError(f"User role must be 'Developer' or 'Project Manager', "
                                              f"{role} is not a valid value")
        return role

    def create(self, validated_data):
        role_display = self.initial_data.get('role', 'Developer')
        role = get_role_db_value(role_display)
        password = validated_data.get('password', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        email = validated_data.get('email', None)
        mobile_phone = validated_data.get('mobile_phone', None)
        user = User.objects.create(email=email, first_name=first_name,
                                   last_name=last_name, mobile_phone=mobile_phone,
                                   role=role, password=password)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_phone = validated_data.get('mobile_phone', instance.mobile_phone)
        role_display = self.initial_data.get('role', None)
        if role_display:
            instance.role = get_role_db_value(role_display)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_type = 'Bearer'

    def validate(self, attrs):
        data = super().validate(attrs)
        new_data_representation = {
            'user': {'id': self.user.id,
                     'first_name': self.user.first_name,
                     'last_name': self.user.last_name,
                     'email': self.user.email,
                     'mobile_phone': self.user.mobile_phone,
                     'role': self.user.get_role_display(),
                     'is_admin_user': self.user.is_superuser},
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'token_type': self.token_type
        }
        return new_data_representation


class TaskSerializer(serializers.ModelSerializer):
    developer = serializers.PrimaryKeyRelatedField(many=False,
                                                   queryset=User.objects.filter(is_active=True,
                                                                                deleted=False,
                                                                                role__exact="D", ))
    project = serializers.SlugRelatedField(slug_field="code", many=False,
                                           queryset=Project.objects.filter(is_active=True,
                                                                           is_deleted=False, ))

    class Meta:
        model = Task
        fields = ('code', 'title', 'description', 'project',
                  'developer', 'is_completed', 'final_date',
                  'is_active', 'created_at', 'updated_at',)
        read_only_fields = ('code', 'created_at',
                            'is_active', 'updated_at',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        fields = self.context.get('fields', None)
        representation.pop('project')
        if fields:
            representation['project'] = instance.project.code
        return representation

    def validate_final_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(f"The final date must be a future date, "
                                              f"{value} is before {timezone.now().date()}")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(read_only=True, many=True)
    project_manager = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.filter(is_active=True,
                                                                                                  deleted=False,
                                                                                                  role__exact="P", ))

    class Meta:
        model = Project
        fields = ('code', 'name', 'description', 'project_manager', 'is_active', 'tasks', 'created_at', 'updated_at',)
        read_only_fields = ('code', 'is_active', 'created_at', 'updated_at',)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)
