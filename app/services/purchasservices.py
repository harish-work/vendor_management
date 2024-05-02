import os
from datetime import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatmug.settings")

import django
django.setup()

from app.models import PurchaseOrder,Vendor


def getpurchas(vendor="ALL"):
    purchas = PurchaseOrder.objects.all().values()
    final = []
    for data in purchas:
        final.append(data)
        if vendor != "ALL":
            try:
                if data['vendor_id'] == vendor:
                    if data not in final:
                        final.append(data)
                else:
                    final.remove(data)
                    continue
            except:
                final.remove(data)
    output = []
    for x in final:
        val = {
            "vendor id":x['vendor_id'],
            "Po number":x['po_number'],
            "Order date":x['order_date'],
            "items":x['items'],
            "quantity":x['quantity'],
            "status":x['status']
        }
        output.append(val)

    return output



def performance_metrics(id):
    entries = PurchaseOrder.objects.filter(vendor=id).values()
    # print(entries)
    '''Average quality rating'''
    total_len_rating = len([x for x in entries if x['status'] == 'completed'])
    add_rating = sum([x['quality_rating'] for x in entries if x['status'] == 'completed'])
    average_quality_rating = add_rating/total_len_rating

    '''Fullfilment Rate'''
    total_len_completed_po = len([x for x in entries if x['status'] == 'completed'])
    total_no_po = len([x for x in entries])
    fullfilment_rate = total_len_completed_po/total_no_po


    '''Average Response Time'''
    total_response = []
    for val in entries:
        try:
           response_time =  val['issue_date']-val['acknowledgment_date']
           total_response.append(response_time.days)
        except:
            total_response.append(0)
    avrage_response_time = sum(total_response)/total_no_po


    '''On Time delivery rate'''
    on_time_delivery = []
    for val in entries:
        now = datetime.now()
        deliver_date = val['delivery_date'].replace(tzinfo=None)
        try:
            time_difference = deliver_date - now
            if time_difference.days >= 0:
                on_time_delivery.append(1)

        except:
            on_time_delivery.append(0)
    on_time_delivery_rate = sum(on_time_delivery)/total_len_rating
    # print(on_time_delivery_rate,avrage_response_time,fullfilment_rate,average_quality_rating)
    update_vendor = Vendor.objects.filter(pk=id).update(on_time_delivery_rate=on_time_delivery_rate,quality_rating_avg=average_quality_rating,average_reponse_time=avrage_response_time,fullfillment_rate=fullfilment_rate)
    vendor = list(Vendor.objects.filter(pk=id).values())
    vendor = vendor[0]
    temp = {
        "Vendor name":vendor['name'],
        "Vendor code":vendor['vendor_code'],
        "On time delivery rate":vendor['on_time_delivery_rate'],
        "Average Quality rating ":vendor['quality_rating_avg'],
        "Average Response time":vendor['average_reponse_time'],
        "Fullfilment rate":vendor['fullfillment_rate']

    }
    return temp





if __name__ == '__main__':
    # print(getpurchas(vendor=3))
    print(performance_metrics(3))
