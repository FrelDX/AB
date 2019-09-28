from centos
RUN yum -y install  python3 make gcc g++ python3-devel
copy requirements.txt /app/requirements.txt
RUN rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
RUN yum -y install nginx
RUN pip3 install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
copy nginx/nginx.conf /etc/nginx/nginx.conf
copy . /app/
copy entrypoint.sh /entrypoint.sh
RUN chmod +x  /entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
