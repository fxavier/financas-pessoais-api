import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from core.models import User, Account, Record, Category

class UserType(DjangoObjectType):
    class Meta:
        model = User

class AccountType(DjangoObjectType):
    class Meta:
        model = Account
        
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        
class RecordType(DjangoObjectType):
    class Meta:
        model = Record    
        
        
class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    accounts = graphene.List(AccountType)
    records = graphene.List(RecordType) 
    users = graphene.List(UserType)  
    
    def resolve_records(self, info):
        return Record.objects.all()
    
    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_users(self, info):
        return User.objects.all()
    
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()
        
    def mutate(self, info, name, email, password):
        user = User(name=name, email=email, password=password)
        user.save()
        return CreateUser(user=user)
    
class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)
    user = graphene.Field(UserType)
    
    class Arguments:
        description = graphene.String()
        operation = graphene.String()
        #user_id = graphene.Int(required=True)
        
    def mutate(self, info, description, operation):
        user = info.context.user
        if user.is_anonymous():
            raise GraphQLError('Login to add Category')
        category = Category(description=description, operation=operation, user=user)
        category.save()
        return CreateCategory(CreateUser=category)
            
        
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    
schema = graphene.Schema(query=Query)
        
    

       
