from django.http import JsonResponse
from django.forms.models import model_to_dict

from login.models import Gateway, Usuario, Cliente, Device
from login.api.serializers import UsuarioSerializer

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):

    def post(self, request):

        chaves = list(request.data.keys())
        requisicoes = ["username", "email", "password"]

        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausenciaaaaaaaaa de parametros"})
        
        try:
            novo_user = Usuario.objects.create(
                username = request.data["username"],
                email = request.data["email"],
                password = request.data["password"]
            )


            token, created = Token.objects.get_or_create(user=novo_user)
        except Exception as e:
            return JsonResponse({"status":"not ok", "error":str(e)})
        return JsonResponse({"status":"ok", "id_novo_user": novo_user.id, "token": token.key})

class RegisterCliente(APIView):

    def post(self, request):

        chaves = list(request.data.keys())
        requisicoes = ["email", "documento", "cep"]

        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausencia de parametros"})
        email = request.data["email"]
        usuario = Usuario.objects.filter(email = email).first()

        try:
            novo_cliente = Cliente.objects.create(
                documento = request.data['documento'],
                usuario = usuario,
                cep = request.data['cep']
            )
        except Exception as e:
            return JsonResponse({"status":"not ok", "error":str(e)})
        dicionario = model_to_dict(novo_cliente)
        data = {
            #"id": dicionario["id"]
            'cliente': dicionario
        }
        return JsonResponse(data)
    
    def get(self, request):
        if "email" not in request.data:
            return JsonResponse({"error":"ausencia de parametros!"})

#cadastra Gateway | retorna gateways de um cliente
class GatewayView(APIView):
    
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        chaves = list(request.data.keys())
        requisicoes = ["nome", "modelo", "mac_adress", "tipo", "estado"]

        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausencia de parametros"})
        usuario = Usuario.objects.filter(email=request.user).first()
        cliente = Cliente.objects.filter(usuario=usuario).first()

        try:


            novo_gateway = Gateway.objects.create(
                nome = request.data['nome'],
                modelo = request.data['modelo'],
                cliente = cliente,
                mac_adress = request.data['mac_adress'],
                estado = request.data['estado'],
                tipo = request.data['tipo']
            )
        except Exception as e:
            return JsonResponse({"status":"not ok", "error":str(e)})

        content = {
            'status': 'ok',
            'message':'Gateway Created',
            # 'gateway': model_to_dict(novo_gateway) #id do gateway
            }
        return JsonResponse(content)
    
    def get(self, request):
        usuario = Usuario.objects.filter(email=request.user).first()
        cliente = Cliente.objects.filter(usuario=usuario).first()
        gateways = Gateway.objects.filter(cliente=cliente).values()
        content = {
            'status': 'ok',
            'gateways':list(gateways)
            }
        return JsonResponse(content)

#cadastra Device | retorna devices de um gateway
class DeviceView(APIView):
    
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        chaves = list(request.data.keys())
        requisicoes = ["id_gateway","ip", "nome", "mac_adress", "estado", "tipo_device"]
        #requisicoes = ["id_gateway"]

        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausencia de parametros"})
        usuario = Usuario.objects.filter(email=request.user).first()
        cliente = Cliente.objects.filter(usuario=usuario).first()
        gateway = Gateway.objects.filter(cliente=cliente, id=request.data["id_gateway"]).first()
        if gateway == None:
            content = {
            'status': 'ok',
            'message': "not found" #id do gateway
            }
        else:
            
            try:

                Device.objects.create(
                    ip = request.data['ip'],
                    nome = request.data['nome'],
                    gateway = gateway,
                    mac_adress = request.data['mac_adress'],
                    estado = request.data['estado'],
                    tipo_device = request.data['tipo_device']
                )

                content = {
                'status': 'ok',
                'message':'Device Created'
                }
            except Exception as e:
                return JsonResponse({"status":"not ok", "error":str(e)})

        
        return JsonResponse(content)
    
    def get(self, request):
        #validação
        chaves = list(request.data.keys())
        requisicoes = ["id_gateway"]

        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausencia de parametros"})

        usuario = Usuario.objects.filter(email=request.user).first()
        cliente = Cliente.objects.filter(usuario=usuario).first()
        gateway = Gateway.objects.filter(cliente=cliente, id=request.data["id_gateway"]).first()
        
        if gateway == None:
            return JsonResponse({"error": "gateway not found"})
        

        devices = Device.objects.filter(gateway=gateway).values()
        content = {
            'status': 'ok',
            'devices':list(devices)
            }
        return JsonResponse(content)

class LoginAPI(APIView):
    def get(self, request):
        chaves = list(request.data.keys())
        requisicoes = ["email", "password"]
        if sorted(requisicoes) != sorted(chaves):
            return JsonResponse({"error": "ausencia de parametros"})
        
        usuario = Usuario.objects.filter(email=request.data['email'], password=request.data['password']).first()

        if usuario == None:
            return JsonResponse({"error":"user not found"})
        
        token, created = Token.objects.get_or_create(user=usuario)

        return JsonResponse({"status":"ok", 'token':token.key})

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ListaUsuarios(generics.ListAPIView):

    def get_queryset(self):
        queryset = Usuario.objects.all()
        return queryset
    serializer_class = UsuarioSerializer