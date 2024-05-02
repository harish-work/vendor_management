from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor,PurchaseOrder,CustomUser
from .serializers import VendorSerializer,PurchaseSerializer,UserSerializer
from app.services.purchasservices import getpurchas,performance_metrics
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class VendorView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        vendorserializer = VendorSerializer(data=request.data)
        if vendorserializer.is_valid():
            vendorserializer.save()
            temp = {
                "data":f"vender Created {vendorserializer.data}",
                "message":"successful"
            }
            return Response(temp,status=status.HTTP_201_CREATED)
        else:
            return Response(vendorserializer.errors)

    # permission_classes = [IsAuthenticated]
    def get(self,request):
        id = request.GET.get('id')
        if id:
            try:
                get_vendor = Vendor.objects.get(id=id)
            except:
                get_vendor = False
            if get_vendor:
                temp = {
                    "Vendor name": str(get_vendor)
                }
                return Response(temp, status=status.HTTP_200_OK)
            else:
                temp = {
                    "Message": f'No vendors with this id: {id}'
                }
                return Response(temp, status=status.HTTP_200_OK)
        else:
            vendor_list = Vendor.objects.all().values()
        # print(vendor_list)
            if vendor_list:
                vendor = []
                for value in vendor_list:
                    vendor_details= {
                        "Vendor Name":value['name'],
                        "Vendor Code" : value['vendor_code'],
                        "Contact details":value['contact_details'],
                        "Address":value['address']
                    }
                    vendor.append(vendor_details)
                temp = {
                    "data":vendor,
                    "message":'successful'
                }
                return Response(temp,status=status.HTTP_200_OK)
            else:
                temp = {
                    "data": 'No vendor to display',
                    "message": 'successful'
                }
                return Response(temp,status=status.HTTP_200_OK)


    def put(self,request):
        id = request.data['id']
        name = request.data['name']
        vendor_name = Vendor.objects.filter(id=id).update(name=name)
        temp = {
            "data":"Vendor details updated",
            "message":"successful"
        }
        return Response(temp,status=status.HTTP_200_OK)

    def delete(self,request):
        id = request.GET.get('id')
        if id:
            try:
                get_vendor = Vendor.objects.filter(id=id).delete()
                temp = {
                    "data": f'vendor with this {id} is deleted',
                    "message":"successful"
                }
                return Response(temp, status=status.HTTP_200_OK)
            except:
                temp = {
                    "data": f'No vendors with this id: {id}',
                    "message":"successful"
                }
                return Response(temp, status=status.HTTP_200_OK)


class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        purchasserializer = PurchaseSerializer(data=request.data)
        if purchasserializer.is_valid():
            purchasserializer.save()
            temp = {
                "data": f"PO Created {purchasserializer.data}",
                "message": "successful"
            }
            return Response(temp, status=status.HTTP_201_CREATED)
        else:
            return Response(purchasserializer.errors)
    def get(self,request):
        id = request.GET.get('id')
        if id:
            try:
                get_purchas_order = PurchaseOrder.objects.get(id=id)
            except:
                get_purchas_order = False
            if get_purchas_order:
                temp = {
                    "data": f"Po No : {str(get_purchas_order)}",
                    "message":"successful"
                }
                return Response(temp, status=status.HTTP_200_OK)
            else:
                temp = {
                    "data": f'No Po with this id: {id}',
                    "message":"successful"
                }
                return Response(temp, status=status.HTTP_200_OK)
        else:
            vendor = request.data['vendor']
            out = getpurchas(vendor)
            temp = {
                "data":out,
                "message":"successful"
            }
            return Response(temp,status=status.HTTP_200_OK)

    def put(self,request):
        id = request.data['id']
        po_status = request.data['status']
        rating = request.data['rating']
        purchas_status = PurchaseOrder.objects.filter(id=id).update(status=po_status,quality_rating=rating)
        temp = {
            "data": "Purchas status updated",
            "message": "successful"
        }
        return Response(temp, status=status.HTTP_200_OK)

    def delete(self,request):
        id = request.GET.get('id')
        if id:
            try:
                get_purchas_order = PurchaseOrder.objects.filter(id=id).delete()
                temp = {
                    "data": f'po with this {id} is deleted',
                    "message": "successful"
                }
                return Response(temp, status=status.HTTP_200_OK)
            except:
                temp = {
                    "data": f'No po with this id: {id}',
                    "message": "successful"
                }
                return Response(temp, status=status.HTTP_200_OK)


class UpdateAcknowledgeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id = request.data['id']
        acknowledge_date = request.data['acknowledge_date']
        purchas_status = PurchaseOrder.objects.filter(id=id).update(acknowledgment_date=acknowledge_date)
        temp = {
            "data": "Purchas order acknowledgment date updated",
            "message": "successful"
        }
        return Response(temp, status=status.HTTP_200_OK)


class GetVendorPerformance(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        id = request.GET.get('id')
        out = performance_metrics(id)
        temp = {
            "data":out,
            "message":"successful"
        }
        return Response(temp,status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self,request):
        userserializer = UserSerializer(data=request.data)
        if userserializer.is_valid():
            data = userserializer.data
            customuser = CustomUser(username=data['email'], email=data['email'],fname=data['fname'],lname=['lname'])
            customuser.set_password(data['password'])
            customuser.save()
            temp ={
                "data": f"user registred successful: {data['email']}",
                "message":"successful"
            }
            return Response(temp,status=status.HTTP_200_OK)
        else:
            return Response(userserializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email,password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)























