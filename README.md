# License Plate Recognition
# Hướng dẫn sử dụng: 
1. Clone git này về nhá : 
```
 git clone https://github.com/taidao1901/LicensePlateRecognition.git
```
2. Tạo Conda env bằng 2 cách:
 - 1.1. Cách 1: Clone y chang cái env gốc

 ```
    conda env create -f enviroment.yml 
 ```
 - 1.2. Cách 2: Cài các gói giống t
  + B1: Khởi tạo môi trường
 ```
    conda create --name <tên env> python=3.9.12
 ```
 + B2: Khởi chạy môi trường
 ```
    conda activate <tên env>
 ```
 + B3: Cài các gói giống với môi trường gốc:
 ```
    pip install -r requirements.txt
 ```

3. vào vs code bấm tổ hợp: ctrl+shift+p --> python:select interpreter --> chọn vào tên môi trường mới tạo

4. Khởi động server bằng lệnh
```
python manage.py runserver
```
