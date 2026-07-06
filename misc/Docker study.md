标签（空格分隔）： docker

---

# 简介
docker是基于go语言的云开源项目，其主要目标是“Build, ship and run any app, anywhere”，通过对应用组件的封装、分发、部署、运行等生命周期的管理，使得用户的APP及其运行环境能够做到“一次镜像，处处运行”。
docker与虚拟机技术的差异


# 核心概念

Docker是一个开源的应用容器引擎，可以轻松的为任何应用创建一个轻量级的、可移植的、自给自足的容器。开发者在本地编译通过的容器可以批量的在生产环境上部署。
Docker类似于集装箱，各式各样的货物，经过集装箱的标准化进行托管，而集装箱与集装箱之前没有影响。Docker是一个开放平台，使开发人员和管理员可以在称为容器的松散隔离的环境中构建镜像、交互和运行分布式应用程序，以便在开发、QA和生产环境之间进行高效的应用程序生命周期管理。
Docker的核心概念包括镜像（Image）、容器（Container）和仓库（Repository）。
**镜像**：可以理解为软件安装包，可以方便的进行传播和安装。  
**容器**：软件安装后的状态，每个软件运行环境都是独立的、隔离的，称之为容器。

### 镜像

Docker的镜像相当于一个只读的静态模板，它封装了运行应用所需的库、资源、环境等文件和配置。构建Docker Image时，会一层层进行，前一层是后一层的基础，每一层构建完就不会再发生改变。
UnionFS(联合文件系统)：是分层、轻量级高性能的文件系统，支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下。UnionFS是docker镜像的基础，讲下可以通过分层来继承，基于基础镜像(没有父镜像)，可以制作各种具体的应用镜像。
bootfs: 引导文件系统
rootfs
镜像分层的最大好处就是资源共享，方便复制迁移和复用。
镜像层都是只读的，容器层是可写的，当容器启动时，一个新的可写层被加载到镜像顶部，这一层被称为容器层，容器层以下的都是镜像层。

### 容器

Docker的容器则是一个动态的实例，通过Docker Image启动，在Image的基础上运行应用。容器有效地将由单个操作系统管理的资源划分到孤立的组中，以更好地在孤立的组之间平衡有冲突的资源使用需求。与传统虚拟化技术相比，容器提供了轻量级的隔离，并在隔离的同时提供共享机制，以实现容器与宿主机的资源共享。
镜像和容器的关系，就像是面向对象程序设计中的类和实例，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、暂停、停止、删除等。
容器的实质是进程，但与直接在宿主执行的进程不同，容器进程运行有属于自己独立的命名空间，容器也是分层存储。
容器存储层的生命周期跟容器一样，容器消亡时，容器存储层也会消亡，任何保存于容器存储层的信息都会丢失。
容器不应该向其存储层内写入任何数据，容器存储层也要保持无状态化。**所有的文件写入操作，都应该使用数据卷、或者绑定宿主目录，在这些位置的读写会跳过存储层，直接对宿主发生读写，其性能和稳定性更高。容器消亡后数据卷的数据不会丢失。**

### 仓库

Docker Registry是一个集中存储、分发镜像的服务。
一个Registry可以包含多个仓库，每个仓库只包含一种软件，但可以包含多个标签（tag，也就是版本），每个标签对应一个镜像。

### 容器数据卷

--privileged=true??? 涉及到权限
卷是目录或文件，存在于一个或多个容器中，由docker挂载到容器，但不属于联合文件系统。卷设计的目的就是完成容器数据的持久化到本地，它完全独立于容器的生命周期，docker不会在删除容器时删除其挂载的数据卷。
容器数据卷支持在容器直接共享或重用数据
卷中的更改实时生效
卷的更改不会包含在镜像的更新中




# DockerFile

Dockerfile是一个文本格式的配置文件，用户可以使用它快速创建自定义的镜像。这个文件由一行行的命令语句组成，并且支持以#开头的注释行。一般来说，Dockerfile由以下四部分组成：
1. 基础镜像信息：这是Dockerfile的第一行，用于指定基础镜像。
2. 维护者信息：这一部分是可选的，可以用来注明制作此镜像的人或者团队的信息。
3. 镜像操作指令：这包括诸如RUN、COPY、ADD等命令，这些命令会在构建镜像的过程中执行。例如，使用RUN命令来安装软件或更新包。
4. 容器启动时执行指令：这一部分的内容会在容器启动时自动执行。例如，使用CMD命令来指定运行容器时的操作命令。
Dockerfile reference: [Dockerfile reference | Docker Docs](https://docs.docker.com/reference/dockerfile/)
每个保留字指令都为大写字母，且后面至少跟随一个参数；
指令从上到下，顺序执行；
每条指令都会创建一个新的镜像层并对镜像进行提交。

**Docker执行Dockerfile的大致流程: **

docker从基础镜像运行一个容器；
执行一条指令并对容器作出修改；
执行类似docker commit操作提交一个新的镜像层；
docker再基于刚提交的镜像运行一个新容器；
执行dockerfile的下一条指令直到所有指令都执行完成。


|常用指令     |用途     |demo     |
| --- | --- | --- |
|FROM     |指定基础镜像  |     |
|ENV  |定义环境变量  |ENV MY_NAME="John" |
|ARG  |定义变量，可以在docker build时传参获取，可以放在FROM指令之前  |     |
|RUN  |运行命令的指令，有shell形式和exec形式  |     |
|CMD  |执行容器的默认指令，只有一个，有shell形式和exec形式  |     |
|LABLE  |将元数据加入到镜像中  |LABEL version="1.0"  |
|EXPOSE  |提醒docker容器是在监听指定的网络端口。可指定使用TCP/UDP协议，默认是TCP。它不是真的发布这个端口。  |EXPOSE 80/tcp  |
|ADD  |添加文件、目录或远端的文件URL(<src>)，到镜像的文件系统中的路径(<dest>)。  |ADD hom* /mydir/ |

分析器指令(parser directives) : 影响 Dockerfile 中后续行的处理方式。它不会在构建中增加层数，也不会在构建过程中展示。格式是 # directive=value 。分析器指令必须在 Dockerfile 中的第一行。有两种分析器指令可以定义：syntax 和 escape。

执行命令，RUN,CMD,ENTRYPOINT指令都有两种形式。分别是exec形式和shell形式。
INSTRUCTION ["executable","param1","param2"] (exec form)
INSTRUCTION command param1 param2 (shell form)


### docker网络模式

- 桥接模式（bridge）：这是Docker默认的网络模式，在此模式下，Docker会创建一个名为docker0的虚拟网桥，并为每个容器分配一个IP地址。这样，容器之间就可以通过IP地址进行通信。
- **主机模式**（host）：在使用这种模式时，容器将直接使用宿主机的网络，与宿主机共享网络接口。这意味着容器将能够访问宿主机上的所有网络资源。
- 容器模式（container）：这是一种较为特殊的网络模式。在此模式下，新创建的容器将共享已存在容器的网络命名空间，从而实现容器之间的网络连接。具体来说，处于这个模式下的Docker容器会共享一个网络栈，这样两个容器之间可以通过localhost进行通信。

### docker数据持久化

- **数据卷**（Volumes）：数据卷是一种特殊的目录，它绕过容器的文件系统层，将数据直接存储在宿主机的指定路径中。这个路径可以位于宿主机的任意位置，由管理员指定。与其他容器共享数据卷的方式包括使用--volumes-from参数来引用其它容器的数据卷，或者在一个容器中创建一个数据卷，然后在其它容器中使用--volumes-from参数来挂载并使用这个数据卷。这样，多个容器就可以共享一组数据了。
- 绑定挂载（Bind Mounts）：这种方式允许将宿主机上的特定目录或文件挂载到容器中。这意味着即使容器被删除，宿主机上的数据仍然存在，并且新创建的容器可以再次使用这些数据。
- tmpfs挂载：与前两种方式不同，tmpfs挂载是在内存中而不是在磁盘上存储数据。当容器停止运行时，所有由tmpfs存储的数据都将被清除。
以上三种方式都可以实现Docker的数据持久化，但在使用时需要根据具体的需求和场景进行选择。例如，对于需要长期保存且多个容器需要共享的数据，应优先考虑使用数据卷；而对于仅在单个容器中使用且不需要长期保存的数据，可以考虑使用绑定挂载或tmpfs挂载。

### docker虚悬镜像
名称、tag都是none的镜像，俗称虚悬镜像dangling image


# 基本命令

Reference: [Reference documentation | Docker Docs](https://docs.docker.com/reference/)

### image相关

```
docker search xxx, xxx表示镜像名称，仓库搜索镜像
docker pull xxx, xxx表示镜像名称，仓库下载镜像，不指定tag，默认下载latest
docker system df, 查看镜像/容器/数据卷所占据的空间
docker rmi xxx,  xxx表示镜像id或镜像名:tag，多个空格分隔，删除镜像
docker rmi -f ${docker images -af}, 删除所有镜像
docker build -t sensor:2.0 .
docker save -o sensor-2.0.tar sensor:2.0
zip sensor-2.0.zip sensor-2.0.tar
docker save lbrain-db_operation:3.0 | gzip > db_operation.tar.gz
```

```
docker image COMMAND
usage: Manage images
Commands:
  build       Build an image from a Dockerfile
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Display detailed information on one or more images
  load        Load an image from a tar archive or STDIN
  ls          List images
  prune       Remove unused images
  pull        Download an image from a registry
  push        Upload an image to a registry
  rm          Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
```

### container相关

```
docker run [options] image [command][args], 基于image创建并启动容器，command表示进入容器后执行的命令
docker ps, 列出所有容器
docker start 容器ID||name
docker stop 容器||name
docker kill 容器||name
docker rm 容器||name
docker rm -f ${docker ps -af}, 删除所有容器
docker exec [option] container command [args], 对运行的容器执行命令
docker top 容器，查看容器内运行的进程
docker inspect xxx, 查看容器or镜像的内部细节
docker cp [options] container:src dst 容器文件copy
docker cp [options] src container:dst 
docker export [options] container导出容器内容留作为一个tar归档文件
cat xxx.tar | docker import - 镜像用户/镜像名:镜像版本号  tar归档文件导入为镜像
```

```
docker container COMMAND
usage: Manage containers
Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  exec        Execute a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
  kill        Kill one or more running containers
  logs        Fetch the logs of a container
  ls          List containers
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  prune       Remove all stopped containers
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  run         Create and run a new container from an image
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes

```


