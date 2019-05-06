
'''
安装运行：
    1.获取：wget -qO- https://get.docker.com/ | sh
    2.开启服务器：sudo service docker start
    3.运行测试：docker run hello-world
准备文件：
    1.定义容器：Dockerfile
    2.安装依赖：requirements.txt
    3.准备程序入口：app.py
构建镜像：
    1.构建：docker build -t image_name dir_position
    2.检查：docker images
运行一个容器：
    1.窗口模式运行：docker run -p 4000:80 image_name
    2.进程模式运行：docker run -d -p 4000:80 image_name
    3.检查：docker ps(运行中)     docker ps -a(所有的)
    4.结束：docker stop 1fa4ab2cf395
共享镜像：
    1.终端登录：docker login
    2.标记镜像：docker tag image_name user_name/repository_name:tag_name
    3.检查：docker images
    4.上传镜像：docker push username/repository_name:tag_name
    5.运行并获取镜像：docker run -p 4000:80 username/repository_name:tag_name
服务：
    1.运行新的负载均衡：docker swarm init
    2.新建一个应用：docker stack deploy -c docker-compose.yml getstartedlab
    3.列出这个应用所有的容器：docker stack ps getstartedlab
    4.删除一个应用：docker stack rm getstartedlab
    5.查看所有的应用：docker stack ls











'''













