# 安装
## 下载代码
git clone https://github.com/FrelDX/AB.git
## 创建rbac授权
kubectl create -f deploy/yaml/rbac.yaml
## 创建ab程序
kubectl create -f deploy/yaml/deploy.yaml
   
   
   