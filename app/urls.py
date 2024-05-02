from django.urls import path
from .views import VendorView,PurchaseView,UpdateAcknowledgeView,GetVendorPerformance,RegisterView,LoginView,LogoutView

urlpatterns = [
    path('Vendors/', VendorView.as_view()),
    path('purchase_orders/',PurchaseView.as_view()),
    path('purchase_orders/acknowledge/',UpdateAcknowledgeView.as_view()),
    path('vendors/performance/',GetVendorPerformance.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view())

]