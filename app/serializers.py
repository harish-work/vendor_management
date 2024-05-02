from rest_framework.serializers import ModelSerializer
from .models import Vendor,HistoricalPerformance,PurchaseOrder,CustomUser



class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','fname','lname','password']
class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class PerformanceSerializer(ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'