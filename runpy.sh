#!/bin/bash
python3 login/login.py > log/login.txt -D
python3 admin/ad.py  > log/ad.txt -D
python3 user/user.py  > log/user.txt -D