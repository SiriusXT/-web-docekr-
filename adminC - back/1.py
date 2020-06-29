s=[b'11', b'22', b'33']
for i in s:
    print(str(i).split("'")[1])

a=[['anaconda-ks.cfg'], ['get-docker.sh'], ['images']]

print(type(a[0])==list)