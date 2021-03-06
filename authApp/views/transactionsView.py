from django.conf                                      import settings
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend

from authApp.models.account                           import Account
from authApp.models.user                           import User
from authApp.models.transaction                       import Transaction
from authApp.serializers.transactionSerializer        import TransactionSerializer

class TransactionsDetailView(generics.RetrieveAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().get(request, *args, **kwargs)


class TransactionsAccountView(generics.ListAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
    
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Transaction.objects.filter(origin_account_id=self.kwargs['account'])
        return queryset


class TransactionCreateView(generics.CreateAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != request.data['transaction_data']['origin_account']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        origin_account = Account.objects.get(id=request.data['transaction_data']['origin_account'])
        if origin_account.balance < request.data['transaction_data']['amount']:
            stringResponse = {'detail':'Saldo Insuficiente'}
            return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)

            #Try except por si la consulta arroja error al no encontrar nada
        try:
            User_email_destiny = request.data['transaction_data'].pop('email_destiny_account')
            print(User_email_destiny)
            User_destiny = User.objects.get(email=User_email_destiny)
        except User_email_destiny.DoesNotExist:
            User_destiny = None
        
        if User_destiny == None:
            stringResponse = {'detail':'Cuenta de envio inexistente'}
            return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)

        id_destiny_account = Account.objects.get(id=User_destiny.id)
        request.data['transaction_data']['destiny_account'] = id_destiny_account.id
        serializer = TransactionSerializer(data=request.data['transaction_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        origin_account.balance -= request.data['transaction_data']['amount']
        origin_account.save()
        
        destiny_account = Account.objects.get(id=request.data['transaction_data']['destiny_account'])
        destiny_account.balance += request.data['transaction_data']['amount']
        destiny_account.save()
        
        return Response("Transacci??n exitosa", status=status.HTTP_201_CREATED)


class TransactionsUpdateView(generics.UpdateAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def update(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().update(request, *args, **kwargs)


class TransactionsDeleteView(generics.DestroyAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def delete(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().destroy(request, *args, **kwargs)
