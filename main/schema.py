"""Add Module Description"""

import graphene

import users.schema

class Query(
    users.schema.Query,
    graphene.ObjectType
):
    """Add Class Description"""
    pass

class Mutation(
    users.schema.Mutation,
    graphene.ObjectType
):
    """Add Class Description"""
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
