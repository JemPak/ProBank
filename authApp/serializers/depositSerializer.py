from authApp.models.account import Account
from authApp.models.deposit import Deposit
from authApp.models.user    import User
from rest_framework                import serializers

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Deposit
        fields = ['account', 'amount', 'register_date', 'note', 'depositer_name']
    
    def to_representation(self, obj):
        account  = Account.objects.get(id=obj.account_id)
        user     = User.objects.get(id=account.user_id)
        deposite = Deposit.objects.get(id=obj.id)
        return {
            'id'             : deposite.id,
            'amount'         : deposite.amount,
            'register_date'  : deposite.register_date,
            'note'           : deposite.note,
            'depositer_name' : deposite.depositer_name,
            'account' : {
                'id'       : account.id,
                'isActive' : account.isActive
            },
            'user' : {
                'id'    : user.id,
                'name'  : user.name,
                'email' : user.email
            }
        }