from django.utils import timezone
from rest_framework import serializers

from users.models import User
from .models import Task, Member


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = '__all__'

#
# class AddMemberSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)

    # def validate(self, attrs):
    #     task_id = attrs.get('task', '')
    #     task = Task.objects.get(pk=task_id)
    #     username = attrs.get('username', '')
    #     print(self.request.user)
    #     user = User.objects.get(username=username)
    #     member = Member(user=user, task=task, role=2)
    #     member.save()
    #     return {
    #         "user": user
    #     }


# class MemberSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     task = serializers.PrimaryKeyRelatedField(many)
#     class Meta:
#         model = Member
#         fields = '__all__'
