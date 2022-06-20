# License Plate Recognition
# Hướng dẫn sử dụng: 
## Clone git : 
```
 git clone https://github.com/taidao1901/LicensePlateRecognition.git
```
## Tạo Conda env bằng 2 cách:
 ### Cách 1:

 ```
    conda env create -f enviroment.yml 
 ```
 ###Cách 2:
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

3. Vào vscode bấm tổ hợp: ctrl+shift+p --> python:select interpreter --> chọn vào tên môi trường mới tạo

4. Khởi động server bằng lệnh
```
python manage.py runserver
```
