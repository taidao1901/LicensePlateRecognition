import time
import cv2
import numpy as np
import numpy as np
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes,text =True):
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    label = str(classes[class_id]) + " " + str(round(confidence, 4) * 100) + "%"
    color = COLORS[class_id]
    
    if text== True:    
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    else:
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 1)

    return img
def plot_object_boxes(img, boxes, classes,text= True):
    clone = img.copy()
    for box in boxes:
        class_id, confidence, tl_x, tl_y, br_x, br_y = box
        draw_prediction(clone, class_id, round(confidence,2), round(tl_x), round(tl_y), round(br_x), round(br_y), classes,text)
    return clone

def load_networks(cfg_path, weight_path):
    net = cv2.dnn.readNet(cfg_path, weight_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    return net

def get_result_predict(img, net,dim, conf_threshold = 0.5, nms_threshold=0.4):
    # Load file weight và cfg
    height, width = img.shape[:2]
    scale = 1/255.0
    # Đưa ảnh vào blob object
    start = time.time()
    blob = cv2.dnn.blobFromImage(img, scale, dim, (0, 0, 0), True, crop=False)
    
    net.setInput(blob)
    # Get output
    
    outs = net.forward(get_output_layers(net))
 
    class_ids = []
    confidences = []
    boxes = []

    # print(outs)
    for out in outs:
        for detection in out:
            scores = detection[5:] # Xác suất các lớp
            class_id = np.argmax(scores) # Lấy vị trí có xác suất lón nhất
            confidence = scores[class_id]
            # Tính tọa độ topleft và width height
            center_x = detection[0] * width
            center_y = detection[1] * height
            w = detection[2] * width
            h = detection[3] * height
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
    
    # NMS
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    result = []
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        result.append([class_ids[i], confidences[i], x, y, x + w, y + h])

    end = time.time()
    return result, end-start

def detection(image,net,classes):
    boxes,time = get_result_predict(image, net, dim = (416,416))
    show_img=plot_object_boxes(image, boxes, classes)
    return boxes, show_img, time

def recognition(image,net,classes):
     # Swap kí tự
    ## Chữ sang số
    char2num = {'A':'4', 'B': '8', 'D':'0', 'G':'6', 'S':'5', 'Z':'7'}
    ## Số sang chữ
    num2char = {'0':'D', '2':'Z', '4':'A', '5':'S', '6':'G', '7':'Z', '8':'B'}

    pred_chars,time = get_result_predict(image, net,dim = (352,128),conf_threshold = 0.5, nms_threshold=0.3)
            # Nếu số kí tự bé hơn 8 thì cho predict lại với conf_threshold thấp hơn
    if len(pred_chars) < 8:
        pred_chars = get_result_predict(image, net, dim = (352,128),conf_threshold = 0.1, nms_threshold=0.5)
    # Nếu số kí tự hớn hơn 9 thì chọn 9 kí tự có conf lớn nhất
    if len(pred_chars) > 9:
        pred_chars = sorted(pred_chars, key=lambda x: x[1])[::-1][:9]

    first_line = []
    second_line = []
    h, w = image.shape[:2]
    for pred_char in pred_chars:
        _,_,_, tl_y,_, br_y = pred_char
        if 0 < (tl_y + br_y) / 2 < h / 2:
            first_line.append(pred_char)
        else:
            second_line.append(pred_char)
    first_line = sorted(first_line, key=lambda x:x[2])
    second_line = sorted(second_line, key=lambda x:x[2])
    result = "".join([*[classes[x[0]] for x in first_line]," ",*[classes[y[0]] for y in second_line]])
    show_img=plot_object_boxes(image, pred_chars, classes,text=False)
        # Thực hiện heuristic rule
    final_result = ""
    if 8 <= len(result) <= 9:
        for idx, c in enumerate(result):
            if idx == 2:
                if result[idx] in num2char.keys():
                    final_result += num2char[result[idx]]
                else:
                    final_result += c
            elif idx == 3:
                final_result += c
            else:
                if result[idx] in char2num.keys():
                    final_result += char2num[result[idx]]
                else:
                    final_result += c
    else:
        final_result = result
    return final_result, show_img, time


def end2end(image):
    #Load fast-yolov2 model
    cfg_pathyolov2 = os.path.join(__location__, 'Fastyolov2/fast-yolov2.cfg')
    weight_pathyolov2 = os.path.join(__location__, 'Fastyolov2/fast-yolov2_best.weights')
    with open(os.path.join(__location__, 'Fastyolov2/yolo.names'), 'r') as f:
        Detectclasses = [line.strip() for line in f.readlines()]
    DetectNet= load_networks(cfg_pathyolov2, weight_pathyolov2)

    #Load CR-Net model 
    cfg_pathCR = os.path.join(__location__,"CR_Net/crnet.cfg")
    weight_pathCR =os.path.join(__location__, "CR_Net/crnet_best.weights")
    with open(os.path.join(__location__,"CR_Net/crnet.names"), 'r') as f:
        Recogclasses = [line.strip() for line in f.readlines()]
    RecogNet = load_networks(cfg_pathCR, weight_pathCR)

    # License Plate Detection and Recognition
    boxes, detect_image, time4detect = detection(image,DetectNet,Detectclasses)
    class_id, confidence, tl_x_bs, tl_y_bs, br_x_bs, br_y_bs = boxes[0]
    lp_image = image[round(tl_y_bs):round(br_y_bs), round(tl_x_bs):round(br_x_bs)]
    result, recog_image, time4recog = recognition(lp_image,RecogNet,Recogclasses)
    return result, detect_image, recog_image, time4recog+time4detect














    
    