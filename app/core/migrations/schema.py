import graphene
from graphene_django import DjangoObjectType

from django.db.models import Q

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
    

       
