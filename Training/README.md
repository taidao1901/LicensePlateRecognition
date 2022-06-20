# Cách huấn luyện mô hình
## 1. Clone Darknet framework của AlexeyAB: https://github.com/AlexeyAB/darknet
## 2. Sử dụng các file cfg, data, names trong các mô hình và dữ liệu trong Data_GreenParking.zip để huấn luyện
- Đối với dữ liệu của CR-NET, cần label dữ liệu theo các class được quy định trong classes.txt
- Chia dữ liệu bằng các notebook SplitData_...
- Sử dụng notebook Data Augmentation.ipynb để tăng cường dữ liệu
- Ví dụ mẫu: https://miai.vn/2020/05/25/yolo-series-train-yolo-v4-train-tren-colab-chi-tiet-va-day-du-a-z/ 
## 3. Dự đoán
Chỉnh sửa lại code các file python ở https://github.com/htdung167/darknet-predict-python 
## 4. Đánh giá
Sử dụng https://github.com/Cartucho/mAP
