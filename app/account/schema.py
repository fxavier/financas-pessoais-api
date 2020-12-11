import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q

from core.models import Category, Account, Transaction, User
from user.schema import UserType


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class AccountType(DjangoObjectType):
    class Meta:
        model = Account

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType, search=graphene.String())
    accounts = graphene.List(AccountType, search=graphene.String())
    transactions = graphene.List(TransactionType, search=graphene.String())

    def resolve_categories(self, info, search=None):
        if search:
            filter = (
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
            return Category.objects.filter(filter)
        return Category.objects.all()

    def resolve_accounts(self, info, search=None):
        if search:
            filter = (
                Q(category__icontains=search) |
                Q(description__icontains=search)
            )
            return Account.objects.filter(filter)
        return Account.objects.all()   

    def resolve_transactions(self, info, search=None):
        if search:
            filter = (
                Q(transaction_type__icontains=search) |
                Q(transaction_date__is=search) |
                Q(description__icontains=search)
            ) 
            return Transaction.objects.filter(filter)
        return Transaction.objects.all()

class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, name, description):
        category = Category(name=name, description=description)
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, **fields):
        category = Category.objects.get(id=fields.get('category_id'))

        category.name = fields.get('name')
        category.description = fields.get('description')

        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    category_id = graphene.Int()

    class Arguments:
        category_id = graphene.Int(required=True)

    def mutate(self, info, category_id):
        category = Category.objects.get(id=category_id)

        category.delete()
        return DeleteCategory(category_id=category.id)


     
class CreateAccount(graphene.Mutation):
    account = graphene.Field(AccountType)

    class Arguments:
        description = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    def mutate(self, info, description, category_id, user_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to add an account')
        account = Account(description=description, category_id=category_id, user_id=user_id)
        account.save()
        return CreateAccount(account=account)

class UpdateAccount(graphene.Mutation):
    account = graphene.Field(AccountType)

    class Arguments:
        account_id = graphene.Int(required=True)
        description = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
    
    def mutate(self, info, **fields):
        account = Account.objects.get(id=fields.get('account_id'))
        account.description = fields.get('description')
        account.category_id = fields.get('category_id')
        account.user_id = fields.get('user_id')

        account.save()
        return UpdateAccount(account=account)

class CreateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_type = graphene.String(required=True)
        amount = graphene.Float(required=True)
        transaction_date = graphene.Date(required=True)
        description = graphene.String(required=True)
        tags = graphene.String()
        note = graphene.String()
        account_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    def mutate(self, info, **fields):
        user = info.context.user 
        if user.is_anonymous:
            raise GraphQLError('Login to add an account')
        transaction = Transaction(
             transaction_type=fields.get('transaction_type'),
             amount=fields.get('amount'),
             transaction_date=fields.get('transaction_date'),
             description=fields.get('description'),
             tags=fields.get('tags'),
             note=fields.get('note'),
             account_id=fields.get('account_id'),
             user_id=fields.get('user_id') 
             )
        transaction.save()
        return CreateTransaction(transaction=transaction)

class UpdateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_id = graphene.Int(required=True)
        transaction_type = graphene.String()
        amount = graphene.Float()
        transaction_date = graphene.Date()
        description = graphene.String()
        tags = graphene.String()
        note = graphene.String()
        account_id = graphene.Int()
        user_id = graphene.Int()
    
    def mutate(self, info, **fields):
        transaction = Transaction.objects.get(id=fields.get('transaction_id'))

        transaction.transaction_type = fields.get('transaction_type')
        transaction.amount = fields.get('amount')
        transaction.transaction_date = fields.get('transaction_date')
        transaction.description = fields.get('description')
        transaction.tags = fields.get('tags')
        transaction.note = fields.get('note')
        transaction.account_id = fields.get('account_id')
        transaction.user_id = fields.get('user_id')

        transaction.save()
        return UpdateTransaction(transaction=transaction)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    delete_category = DeleteCategory.Field()
    update_category = UpdateCategory.Field()
    create_account = CreateAccount.Field()
    update_account = UpdateAccount.Field()
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()