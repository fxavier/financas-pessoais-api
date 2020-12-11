import graphene
import user.schema
import account.schema
import graphql_jwt

class Query(user.schema.Query, account.schema.Query, graphene.ObjectType):
    pass

class Mutation(user.schema.Mutation, account.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)