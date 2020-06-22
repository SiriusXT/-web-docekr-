echo start
python3 login/login.py > log-login.txt &
python3 admin/ad.py  > log-ad.txt &
python3 user/user.py  > log-user.txt &