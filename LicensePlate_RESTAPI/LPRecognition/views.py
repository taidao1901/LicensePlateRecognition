from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .DeepLearningModel import end2end
import io
from PIL import Image
from io import BytesIO
import numpy as np
from base64 import b64decode,b64encode


# Create your views here.

@csrf_exempt
def LPRecognition_api(api_request):
    json_object = {'success': False}
    if api_request.method == "POST":
        # Nhận thông tin của hình ảnh người dùng dưới dạng base64 rồi convert về dạng np.array
        if api_request.POST.get("image64", None) is not None:
            base64_data = api_request.POST.get("image64", None).split(',', 1)[1]
            data = b64decode(base64_data)
            data = np.array(Image.open(io.BytesIO(data)))
            result, detect_image, recog_image, time = end2end.end2end(data)

        elif api_request.FILES.get("image", None) is not None:
            image_api_request = api_request.FILES["image"]
            image_bytes = image_api_request.read()
            image = Image.open(io.BytesIO(image_bytes))
            result, detect_image, recog_image, time = end2end.end2end(image)
    if result:
        json_object['success']=True
    # Đóng gói các thông tin: dãy kí tự, thời gian xử lí, ảnh kết quả detect biển số, ảnh kết quả nhận dạng biển số
    json_object['result'] = str(result)
    json_object['time']=str(round(time,3))+" seconds"
    json_object['detect_image']= image2base64(detect_image)
    json_object['recog_image']= image2base64(recog_image)
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


