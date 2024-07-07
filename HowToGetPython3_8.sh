apt update -y

apt install curl -y

wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz  

tar -xf Python-3.8.0.tar.xz  

cd Python-3.8.0

./configure --enable-optimizations --enable-loadable-sqlite-extensions && make altinstall 

sudo ln -sfn /usr/local/bin/python3.8 /usr/bin/python3

python3 <(curl -sSL https://bootstrap.pypa.io/get-pip.py)
