@echo off

cd AppData\Roaming\Python\Python38\Scripts\5GRANSched

pip uninstall scheduler==0.0.1

cd scheduler

pip install -e .

cd C:\Users\%USERNAME%

cmd /k