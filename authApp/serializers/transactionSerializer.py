from authApp.models.account     import Account
from authApp.models.user        import User
from authApp.models.transaction import Transaction
from rest_framework             import serializers
from datetime                   import datetime

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Transaction
        fields = ['origin_account','destiny_account', 'amount', 'register_date', 'note']

    def transform_date(fecha):
        return datetime.fromisoformat(fecha).strftime('%Y-%m-%d %H:%M:$S')
    
    def to_representation(self, obj):
        account_origin  = Account.objects.get(id=obj.origin_account_id)
        account_destiny = Account.objects.get(id=obj.destiny_account_id)
        transaction     = Transaction.objects.get(id=obj.id)
        User_destiny    = User.objects.get(id=account_destiny.id)
        return {
            'id'            : transaction.id,
            'amount'        : transaction.amount,
            'register_date' : transaction.register_date,
            'note'          : transaction.note,
            'origin_account' : {
                'id'            : account_origin.id,
                'balance'       : account_origin.balance,
                'lastChangeDate': account_origin.lastChangeDate,
                'isActive'      : account_origin.isActive
            },
            'destiny_account' : {
                'id'            : account_destiny.id,
                'balance'       : account_destiny.balance,
                'lastChangeDate': account_destiny.lastChangeDate,
                'isActive'      : account_destiny.isActive,
                'email'         : User_destiny.email 
            }
        }