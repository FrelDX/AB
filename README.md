#功能介绍
 
         ab是一个根据k8s的准入控制器，而开发出来的一个针对deploy资源对象的增删改查的服务，让注入/拦截变的更简单。ab是一个无状态的服务，本身不依赖任何的数据库，只使用k8s的configmap保存数据，后续会兼容kubectl使用k8s crd来保存一些策略和权限。
 
         已经实现的功能
 
                 容器注入
 
                        自定义注入的规则和注入的容器body实现自动注入
 
                 模板创建资源（支持deploy svc ingress目前还未实现）
 
                       自定义模板，通过api调用模板创建资源，模板支持模板语言，模板中可以使用变量，调用接口的时候，会自动渲染
 
          未实现在开发中的功能+
                          健康检查注入
                                   同上
 
                 configmap注入
 
                       同上
 
                 环境变量注入
 
                       同上
 
                 拦截创建/删除/更新资源
 
                      根据用户自己定义的权限策略，动态的拦截到增删改查操作，并通知，可配置回调地址
 
                 webhook回调二次鉴权
 
                       当发生没有授权的操作的时候 通知到管理员，如果管理员点击同意链接（钉钉，微信，邮件），则创建
# 安装
## 下载代码
git clone https://github.com/FrelDX/AB.git
## 创建rbac授权
kubectl create -f deploy/yaml/rbac.yaml
## 创建ab程序
kubectl create -f deploy/yaml/deploy.yaml
   
   
   
