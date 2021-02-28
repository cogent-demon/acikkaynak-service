import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.common.schemas.languages import LanguageNode
from app.achievements.models import Achievement


# queries


class AchievementNode(DjangoObjectType):
    # id = graphene.ID(source="pk", required=True)
    languages = graphene.List(LanguageNode)

    class Meta:
        model = Achievement
        exclude = ("uuid",)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "type": ["exact"],
        }


class Query(graphene.ObjectType):
    achievement = graphene.relay.Node.Field(AchievementNode)
    achievement_by_uuid = graphene.Field(AchievementNode, uuid=graphene.UUID(required=True))
    achievements_all = DjangoFilterConnectionField(AchievementNode)

    @staticmethod
    # pylint:disable=unused-argument
    def resolve_profile_by_uuid(parent, info, uuid):
        try:
            return Achievement.objects.get(uuid=uuid)
        except Achievement.DoesNotExist:
            return None


# mutations


class Mutation(graphene.ObjectType):
    pass
