"""Add Module Description"""

# TODO: # pylint: disable=fixme

# 1. Find out best practices for crud graphql √
# 2. Return presigned url for images √
# 3. Save images under userId √
# 4. Delete Image from s3 when record is deleted √
# 5. Extend UserCreatInput to include id for update input - instead of writing it out twice √
# 6. Structure Delete Response √
# 7. Refactor √
# 8. Move boto3 functionality to own folder √
# 9. Log Errors √
# 10. See if there is a way to create Custom Errors √
# 11. Check sentry recieve the custom errors √
# 12. Schema tests √
# 13. Timestamp test for abstract tests √
# 14. Using Serilizer √
# 15. Add search database functionality √
# 16. Field Validation √
# 17. Change username to username √
# 18. Add pagination √
# 19. Custom Error Tests √
# 20. main.view tests √
# 21. AWS sdk tests √
# 22. Serilizer error tests √
# 23. Main Model error tests √
# 24. Schema Empty tests ?? √
# 25. See if there is a way to use the S3 storage to delete a file - StaticS3Storage √
# 26. Fix custom errors i.e model vs class √
# 27. Mocking out the time √
# 28. Change record_id to record_id √
# 29. Add paginations tests √
# 30. Fix Flakey tests √
# 31. Simplify serializers - make object.get(pk=id) a function in base model to be get_by_id √
# 32. self.assertTrue('errors' not in content) does not appear to work as expected - fix this
# 33. Move mutation and query to main (check where it should go) ??
# 34. Add CloudFront for images

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_file_upload.scalars import Upload

from sdk.aws.s3 import S3
from users.models import UserModel
from users.serializers import (
	CreateSerializedUser,
	CreateSerializedUsers,
	UpdateSerializedUser,
	UpdateSerializedUsers
)

s3 = S3()


class UserType(DjangoObjectType):
    """Add Class Description"""

    class Meta:
        """Add Class Description"""

        model = UserModel
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'username': ['exact', 'icontains', 'istartswith'],
        }
        # use_connection = True
        interfaces = (relay.Node,)


    presigned_url = graphene.String()

    record_id = graphene.UUID()

    def resolve_record_id(self, _):
        """Add Function Description"""

        return self.id # pylint: disable=E1101

    def resolve_presigned_url(self, _):
        """Add Function Description"""

        return s3.get_presigned_url(self.profile_picture) # pylint: disable=E1101


class UserConnection(relay.Connection):
    """Add Class Description"""

    class Meta:
        """Add Class Description"""

        node = UserType

class Query(graphene.ObjectType):
    """Add Class Description"""

    users = graphene.List(UserType)
    user_by_record_id = graphene.Field(UserType, record_id=graphene.UUID(required=True))
    user_by_name = graphene.Field(UserType, name=graphene.String(required=True))
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    filtered_users = DjangoFilterConnectionField(UserType)
    user_pagination = relay.ConnectionField(UserConnection)

    def resolve_users(self, _):
        """Add Function Description"""

        return UserModel.objects.all()

    def resolve_user_by_record_id(self, _, record_id):
        """Add Function Description"""

        return UserModel.by_id(record_id, accepts_does_not_exist=True)

    def resolve_user_by_name(self, _, name):
        """Add Function Description"""

        return UserModel.by_name(name, accepts_does_not_exist=True)

    def resolve_user_by_username(self, _, username):
        """Add Function Description"""

        return UserModel.by_username(username, accepts_does_not_exist=True)

    def resolve_filter_users(self, _, **kwargs):
        """Add Function Description"""

        return UserModel.objects.filter(**kwargs)

    def resolve_user_pagination(self, _, **kwargs):
        """Add Function Description"""

        return UserModel.objects.all()


class CreateUserInput(graphene.InputObjectType):
    """Add Class Description"""

    name = graphene.String(required=True)
    username = graphene.String(required=True)
    profile_picture = Upload(required=False)


class CreateUser(graphene.Mutation):
    """Add Class Description"""

    user = graphene.Field(UserType)


    class Arguments:
        """Add Class Description"""

        user_data = CreateUserInput(required=True)

    def mutate(self, _, user_data=None):
        """Add Function Description"""

        user = CreateSerializedUser(user_data).is_valid()
        return CreateUser(user=user)


class CreateUsers(graphene.Mutation):
    """Add Class Description"""

    users = graphene.List(UserType)


    class Arguments:
        """Add Class Description"""

        user_data = graphene.List(CreateUserInput, required=True)

    def mutate(self, _, user_data=None):
        """Add Function Description"""

        users = CreateSerializedUsers(user_data).is_valid()
        return CreateUsers(users=users)


class UserUpdateInput(graphene.InputObjectType):
    """Add Class Description"""

    id = graphene.ID(required=True)
    name = graphene.String()
    username = graphene.String()
    profile_picture = Upload()


class UpdateUser(graphene.Mutation):
    """Add Class Description"""

    user = graphene.Field(UserType)


    class Arguments:
        """Add Class Description"""

        user_data = UserUpdateInput(required=True)

    def mutate(self, _, user_data=None):
        """Add Function Description"""

        user = UpdateSerializedUser(user_data).is_valid()
        return UpdateUser(user=user)


class UpdateUsers(graphene.Mutation):
    """Add Class Description"""

    users = graphene.List(UserType)


    class Arguments:
        """Add Class Description"""

        user_data = graphene.List(UserUpdateInput, required=True)

    def mutate(self, _, user_data=None):
        """Add Function Description"""

        users = UpdateSerializedUsers(user_data).is_valid()
        return UpdateUsers(users=users)


class DeleteUserResult(graphene.ObjectType):
    """Add Class Description"""

    record_id = graphene.UUID()
    success = graphene.Boolean()


class DeleteUser(graphene.Mutation):
    """Add Class Description"""

    result = graphene.Field(DeleteUserResult)


    class Arguments:
        """Add Class Description"""

        record_id = graphene.ID(required=True)

    def mutate(self, _, record_id):
        """Add Function Description"""

        UserModel.delete_record(record_id)
        result = DeleteUserResult(record_id=record_id, success=True)

        return DeleteUser(result=result)


class DeleteUsers(graphene.Mutation):
    """Add Class Description"""

    result = graphene.List(DeleteUserResult)


    class Arguments:
        """Add Class Description"""

        record_ids = graphene.List(graphene.ID, required=True)

    def mutate(self, _, record_ids):
        """Add Function Description"""

        result = UserModel.delete_records(record_ids)
        return DeleteUsers(result=result)


class Mutation(graphene.ObjectType):
    """Add Class Description"""

    create_user = CreateUser.Field()
    create_users = CreateUsers.Field()
    update_user = UpdateUser.Field()
    update_users = UpdateUsers.Field()
    delete_user = DeleteUser.Field()
    delete_users = DeleteUsers.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
