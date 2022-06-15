from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .Fastyolov2 import detect_LP_darknet
import io
from PIL import Image
from io import BytesIO
import numpy as np
from base64 import b64decode,b64encode


# Create your views here.

@csrf_exempt
def LPdetection_api(api_request):
    json_object = {'success': False}
    if api_request.method == "POST":

        if api_request.POST.get("image64", None) is not None:
            base64_data = api_request.POST.get("image64", None).split(',', 1)[1]
            data = b64decode(base64_data)

            data = np.array(Image.open(io.BytesIO(data)))
            result, result_img, time = detect_LP_darknet.detection(data)

        elif api_request.FILES.get("image", None) is not None:
            image_api_request = api_request.FILES["image"]
            image_bytes = image_api_request.read()
            image = Image.open(io.BytesIO(image_bytes))
            result, result_img, time= detect_LP_darknet.detection(image)

    if result:
        json_object['success']=True
    json_object['time']=str((time))+" seconds"
    json_object['object']= str(result)
    json_object['result_img']= image2base64(result_img)
    return JsonResponse(json_object)

def detect_request(api_request):
    return render(api_request, 'index.html')

def image2base64(image):
    image = Image.fromarray(image.astype(np.uint8))
    im_file = BytesIO()
    image.save(im_file,format='PNG')
    result_img= im_file.getvalue()
    base64 ='data:image/png;base64,'+ str(b64encode(result_img)).split("'")[1]
    return base64


