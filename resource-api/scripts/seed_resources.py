import sys
import os
import random
import sqlite3
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.getenv("DB_PATH", "/data/laoma/db/app.db")


RESOURCES_DATA = {
    1: [
        ("零基础入门Python编程视频教程（全集）", "从零开始学习Python，涵盖基础语法、数据结构、面向对象、文件操作等核心内容，适合完全零基础的初学者。", "Python,编程入门,视频教程"),
        ("Vue3+TypeScript企业级实战视频课", "深入学习Vue3组合式API、Pinia状态管理、Vue Router路由，配合TypeScript进行企业级项目开发。", "Vue3,TypeScript,前端"),
        ("Java高级编程-多线程与并发实战", "全面讲解Java多线程编程、线程池、锁机制、并发工具类、CAS与原子操作，提升并发编程能力。", "Java,多线程,并发"),
        ("Spring Boot 3.x从入门到精通", "系统学习Spring Boot框架，包括自动配置原理、数据访问、安全认证、缓存、消息队列等高级特性。", "Spring Boot,后端,Java"),
        ("React18+Next.js全栈开发实战", "使用React18和Next.js构建全栈应用，涵盖SSR、SSG、API Routes、数据库集成等完整开发流程。", "React,Next.js,全栈"),
        ("Docker与Kubernetes容器编排实战", "从Docker基础到Kubernetes集群管理，学习容器化部署、服务编排、监控告警等运维技能。", "Docker,Kubernetes,运维"),
        ("MySQL数据库从入门到调优", "覆盖SQL语法、索引原理、查询优化、分库分表、主从复制等数据库核心知识。", "MySQL,数据库,调优"),
        ("Go语言Web开发实战教程", "使用Go语言开发高性能Web服务，包括Gin框架、GORM、中间件、JWT认证等实战内容。", "Go,Web开发,后端"),
        ("Flutter跨平台移动开发入门到实战", "学习Flutter框架开发iOS和Android应用，涵盖Widget体系、状态管理、网络请求、项目实战。", "Flutter,移动开发,跨平台"),
        ("Rust系统编程实战视频教程", "从Rust语法基础到系统编程实战，包括所有权机制、生命周期、并发编程、异步编程等核心概念。", "Rust,系统编程,底层"),
        ("机器学习入门与Python实践", "讲解机器学习基础算法，包括线性回归、决策树、SVM、神经网络，配合Scikit-learn实战练习。", "机器学习,Python,AI"),
        ("深度学习与PyTorch实战", "使用PyTorch框架实现CNN、RNN、Transformer等深度学习模型，完成图像分类、文本生成等项目。", "深度学习,PyTorch,神经网络"),
        ("Redis缓存实战-从入门到高可用", "全面学习Redis数据结构、持久化、哨兵模式、集群方案，以及缓存穿透、雪崩等实战问题处理。", "Redis,缓存,高可用"),
        ("Linux运维工程师入门到精通", "系统学习Linux操作系统、Shell脚本、系统管理、网络配置、Nginx、Tomcat等运维核心技能。", "Linux,运维,Shell"),
        ("微信小程序开发从零到一", "从零开始开发微信小程序，包括页面开发、云开发、支付接入、发布上线等完整流程。", "微信小程序,前端,移动开发"),
        ("数据结构与算法精讲（Java版）", "系统讲解数组、链表、栈、队列、树、图等数据结构，以及排序、查找、动态规划等常见算法。", "数据结构,算法,Java"),
        ("Elasticsearch搜索引擎实战教程", "学习Elasticsearch全文检索引擎，包括索引管理、查询DSL、聚合分析、集群部署等核心内容。", "Elasticsearch,搜索,大数据"),
        ("Node.js后端开发进阶教程", "深入学习Node.js事件循环、Stream、集群模式、性能优化，配合Express/Koa构建高性能服务。", "Node.js,后端,JavaScript"),
        ("计算机网络原理精讲", "系统讲解OSI七层模型、TCP/IP协议族、HTTP/HTTPS、DNS、CDN等网络基础知识。", "计算机网络,协议,TCP"),
        ("GraphQL API开发实战", "学习GraphQL查询语言和Schema设计，使用Apollo Server构建灵活高效的API服务。", "GraphQL,API,Apollo"),
        ("微信支付与支付宝支付集成教程", "详解微信支付和支付宝支付的接入流程，包括JSAPI支付、H5支付、退款、回调处理等实战内容。", "支付,微信,支付宝"),
        ("Python爬虫从入门到Scrapy框架", "学习Requests、BeautifulSoup、Selenium等爬虫技术，掌握Scrapy框架构建高效爬虫系统。", "爬虫,Python,Scrapy"),
        ("MongoDB数据库实战教程", "全面学习MongoDB文档数据库，包括CRUD操作、聚合管道、索引优化、副本集和分片集群。", "MongoDB,NoSQL,数据库"),
        ("TypeScript从入门到高级类型体操", "深入学习TypeScript类型系统、泛型、条件类型、映射类型，掌握高级类型编程技巧。", "TypeScript,前端,类型系统"),
        ("微服务架构设计与Spring Cloud实战", "学习微服务架构设计，使用Spring Cloud构建注册中心、网关、配置中心、熔断器等核心组件。", "微服务,Spring Cloud,架构"),
        ("Figma UI设计入门到实战", "学习Figma设计工具，包括组件设计、自动布局、原型交互、设计系统搭建等UI设计核心技能。", "Figma,UI设计,设计工具"),
        ("C++游戏开发入门教程", "使用C++和SFML/SDL库开发2D游戏，学习游戏循环、碰撞检测、物理引擎等游戏开发基础。", "C++,游戏开发,SFML"),
        ("PostgreSQL数据库从入门到实战", "系统学习PostgreSQL关系型数据库，包括高级查询、JSON支持、全文搜索、性能调优等。", "PostgreSQL,数据库,SQL"),
        ("网络安全与渗透测试入门教程", "学习网络安全基础知识，掌握Kali Linux、Nmap、Burp Suite等渗透测试工具的使用方法。", "网络安全,渗透测试,Kali"),
        ("Tailwind CSS现代前端开发实战", "使用Tailwind CSS原子化框架快速构建现代UI，学习响应式设计、自定义主题、组件封装。", "Tailwind CSS,前端,CSS"),
        ("Python数据分析与可视化实战", "使用Pandas、Matplotlib、Seaborn进行数据清洗、分析和可视化，完成真实数据分析项目。", "Python,数据分析,可视化"),
        ("iOS Swift开发入门到实战", "学习Swift语言和iOS开发，包括UIKit、SwiftUI、Core Data、网络请求等移动端开发技能。", "iOS,Swift,移动开发"),
        ("消息队列RabbitMQ实战教程", "学习RabbitMQ消息中间件，包括交换机、队列、路由模式、死信队列、消息确认等核心概念。", "RabbitMQ,消息队列,中间件"),
        ("Android Jetpack Compose开发实战", "使用Jetpack Compose声明式UI框架开发Android应用，学习状态管理、导航、动画等现代Android开发。", "Android,Compose,移动开发"),
        ("Git版本控制从入门到团队协作", "全面学习Git版本控制，包括分支管理、合并策略、冲突解决、Git Flow工作流等团队协作实践。", "Git,版本控制,协作"),
        ("Nginx高并发Web服务器配置实战", "深入学习Nginx配置，包括反向代理、负载均衡、HTTPS配置、性能优化、日志分析等运维技能。", "Nginx,Web服务器,运维"),
        ("Python自动化办公教程", "使用Python自动化处理Excel、Word、PDF、邮件等日常办公任务，提升工作效率。", "Python,自动化,办公"),
        ("DevOps持续集成与持续部署实战", "学习Jenkins、GitLab CI/CD、GitHub Actions等CI/CD工具，实现自动化构建、测试和部署。", "DevOps,CI/CD,Jenkins"),
        ("前端性能优化实战指南", "系统学习前端性能优化策略，包括资源压缩、懒加载、缓存策略、代码分割、SSR等优化手段。", "前端,性能优化,Web"),
        ("Python Django Web开发实战", "使用Django框架快速开发Web应用，包括ORM、模板、REST API、用户认证等完整开发流程。", "Django,Python,Web开发"),
    ],
    2: [
        ("Python编程：从入门到实践（第3版）", "经典Python入门书籍，通过项目驱动的方式讲解Python编程基础和实战应用，适合自学和课堂教学。", "Python,入门,编程"),
        ("深入理解Java虚拟机（第3版）", "全面解析JVM架构、内存模型、垃圾收集、类加载机制，是Java进阶必备参考书。", "Java,JVM,虚拟机"),
        ("JavaScript高级程序设计（第4版）", "前端开发经典红宝书，深入讲解JavaScript语言核心、DOM、BOM、事件、Ajax等前端知识。", "JavaScript,前端,红宝书"),
        ("算法导论（第3版）", "计算机科学经典教材，系统讲解算法设计与分析，涵盖排序、图算法、动态规划等核心内容。", "算法,数据结构,计算机科学"),
        ("设计模式：可复用面向对象软件的基础", "GoF设计模式经典著作，介绍23种经典设计模式及其在软件设计中的应用。", "设计模式,面向对象,架构"),
        ("代码整洁之道", "Martin大叔的经典之作，教你如何编写可读、可维护、高质量的代码。", "代码质量,编程实践,重构"),
        ("MySQL技术内幕：InnoDB存储引擎", "深入剖析MySQL InnoDB存储引擎的实现原理，包括B+树索引、事务、锁、崩溃恢复等。", "MySQL,InnoDB,数据库内核"),
        ("CSS权威指南（第4版）", "CSS领域的权威参考书，全面覆盖CSS选择器、布局、动画、响应式设计等现代CSS技术。", "CSS,前端,样式"),
        ("Go语言圣经", "Go语言权威指南，由Go语言核心团队成员编写，深入讲解Go语言特性和编程哲学。", "Go语言,编程,后端"),
        ("重构：改善既有代码的设计（第2版）", "经典重构指南，介绍如何通过小步重构改善代码结构，提升代码质量和可维护性。", "重构,代码质量,设计"),
        ("计算机网络：自顶向下方法（第8版）", "经典计算机网络教材，从应用层到物理层自顶向下讲解网络协议和架构。", "计算机网络,协议,教材"),
        ("深入理解计算机系统（第3版）", "CSAPP经典教材，从程序员视角理解计算机系统，包括数据表示、汇编、内存、并发等。", "计算机系统,底层,经典教材"),
        ("Rust程序设计语言", "Rust官方推荐书籍，通过实际项目引导学习Rust的所有权、借用、生命周期等核心概念。", "Rust,系统编程,安全"),
        ("高性能MySQL（第4版）", "MySQL性能优化权威指南，涵盖Schema设计、查询优化、服务器调优、高可用架构等。", "MySQL,性能优化,数据库"),
        ("React设计原理", "深入React源码，解析Fiber架构、调度机制、Hooks实现原理，理解React设计思想。", "React,源码,前端框架"),
        ("TypeScript编程", "系统学习TypeScript语言，包括类型系统、泛型、装饰器、模块化等高级特性。", "TypeScript,前端,类型系统"),
        ("Python数据科学手册", "使用NumPy、Pandas、Matplotlib、Scikit-learn进行数据科学实践的综合指南。", "Python,数据科学,数据分析"),
        ("Linux命令行与Shell脚本编程大全", "Linux命令行和Shell脚本编程的实用指南，覆盖常用命令、脚本编写、系统管理等。", "Linux,Shell,命令行"),
        ("数据库系统概念（第7版）", "数据库领域经典教材，系统讲解关系模型、SQL、事务管理、并发控制等数据库核心理论。", "数据库,理论,教材"),
        ("Flutter实战", "Flutter框架实战指南，从Dart语言到Widget体系，完成多个Flutter移动应用项目。", "Flutter,移动开发,Dart"),
        ("Spring实战（第6版）", "Spring框架实战指南，包括Spring Boot、Spring MVC、Spring Data、Spring Security等。", "Spring,Java,后端"),
        ("Docker实战", "Docker容器技术实战书籍，包括镜像构建、容器编排、网络配置、数据管理等核心内容。", "Docker,容器,运维"),
        ("Kubernetes in Action（第2版）", "Kubernetes实战指南，深入讲解Pod、Service、Deployment等核心概念和集群运维。", "Kubernetes,容器编排,运维"),
        ("机器学习实战", "通过Python实现经典机器学习算法，包括kNN、决策树、朴素贝叶斯、SVM等。", "机器学习,Python,实战"),
        ("Vue.js设计与实现", "深入Vue.js框架设计，解析响应式系统、编译器、渲染器等核心模块的实现原理。", "Vue.js,源码,前端框架"),
        ("HTTP权威指南", "HTTP协议的权威参考书，详细讲解HTTP报文、连接管理、缓存、认证、HTTPS等。", "HTTP,网络协议,Web"),
        ("Redis设计与实现", "深入Redis内部实现，解析数据结构、持久化、事件驱动、复制、集群等核心机制。", "Redis,源码,缓存"),
        ("编译原理（第2版）", "编译器设计经典教材，龙书第2版，涵盖词法分析、语法分析、语义分析、代码生成等。", "编译原理,龙书,计算机科学"),
        ("Python网络爬虫权威指南（第2版）", "使用Python构建可靠的网络爬虫，包括Scrapy、Selenium、反爬策略等实战内容。", "爬虫,Python,数据采集"),
        ("系统设计面试指南", "准备系统设计面试的实用指南，涵盖负载均衡、缓存、数据库设计、分布式系统等话题。", "系统设计,面试,架构"),
        ("C++ Primer（第5版）", "C++学习经典书籍，全面覆盖C++11标准，从基础语法到高级特性循序渐进。", "C++,入门,经典"),
        ("Node.js设计模式（第3版）", "深入Node.js设计模式和最佳实践，包括流、集群、Worker、微服务等高级主题。", "Node.js,设计模式,后端"),
        ("操作系统概念（第10版）", "操作系统经典教材（恐龙书），涵盖进程管理、内存管理、文件系统、I/O等核心概念。", "操作系统,教材,计算机科学"),
        ("图解HTTP", "以图解方式通俗讲解HTTP协议，适合前端、后端、测试等各方向开发者快速理解网络基础。", "HTTP,网络,图解"),
        ("Python深度学习（第2版）", "使用Keras和TensorFlow进行深度学习实践，包括CNN、RNN、GAN等模型实战。", "深度学习,Python,Keras"),
        ("数据密集型应用系统设计", "DDIA经典著作，讲解分布式存储、流处理、批处理等数据系统的设计原则和工程实践。", "分布式系统,数据,架构"),
        ("写给程序员的Unicode教程", "全面介绍Unicode编码标准、字符集、UTF-8/16/32编码、文本处理等实用知识。", "Unicode,编码,文本处理"),
        ("Swift编程（第6版）", "Swift语言官方指南，全面覆盖Swift语法、协议、泛型、并发等语言特性。", "Swift,iOS,编程语言"),
        ("微服务架构设计模式", "系统讲解微服务拆分策略、数据管理、Saga模式、CQRS等微服务设计模式和最佳实践。", "微服务,架构,设计模式"),
        ("PostgreSQL指南：内幕探索", "深入PostgreSQL内部实现，解析查询处理、索引结构、事务机制、MVCC等核心技术。", "PostgreSQL,数据库,内核"),
    ],
    3: [
        ("VSCode高效开发插件合集推荐", "精选30+款VSCode必装插件，覆盖代码补全、调试、Git、美化、效率工具等各个方面。", "VSCode,插件,开发工具"),
        ("IntelliJ IDEA Ultimate 2024配置指南", "详解IDEA项目配置、快捷键、插件推荐、JVM调优，打造高效Java开发环境。", "IDEA,Java,IDE"),
        ("Docker Desktop一键部署开发环境", "使用Docker Compose一键搭建包含MySQL、Redis、Nginx的完整开发环境。", "Docker,开发环境,容器"),
        ("Postman API测试工具完全指南", "使用Postman进行API接口测试，包括集合管理、环境变量、自动化测试、Mock服务等。", "Postman,API测试,接口"),
        ("Navicat Premium数据库管理工具", "强大的数据库管理工具，支持MySQL、PostgreSQL、SQLite等多种数据库的可视化管理。", "Navicat,数据库,管理工具"),
        ("GitKraken可视化Git客户端", "直观的Git图形化工具，支持分支管理、合并冲突解决、Pull Request等Git工作流。", "Git,可视化,版本控制"),
        ("Homebrew macOS包管理器使用指南", "macOS下高效的包管理工具，一条命令安装、更新、卸载各类开发工具和依赖。", "Homebrew,macOS,包管理"),
        ("Charles抓包工具使用教程", "详解Charles代理抓包工具的配置和使用，支持HTTP/HTTPS请求抓取和模拟调试。", "Charles,抓包,调试"),
        ("Chrome DevTools开发者工具高级技巧", "深入Chrome开发者工具的使用技巧，包括Performance分析、Memory排查、Network优化。", "Chrome,DevTools,调试"),
        ("Notion项目管理与知识库搭建指南", "使用Notion搭建团队项目管理看板、知识库、文档系统，提升团队协作效率。", "Notion,项目管理,协作"),
        ("Oh My Zsh终端美化与效率提升", "使用Oh My Zsh打造高效美观的终端环境，包括主题配置、插件推荐、别名设置等。", "Zsh,终端,Linux"),
        ("Wireshark网络协议分析工具教程", "使用Wireshark进行网络协议分析，抓取和分析TCP、HTTP、DNS等各类网络数据包。", "Wireshark,网络分析,抓包"),
        ("Redis Desktop Manager可视化工具", "Redis桌面可视化管理工具，支持键值浏览、数据编辑、命令执行、性能监控等功能。", "Redis,可视化管理,数据库"),
        ("JMeter性能测试工具入门指南", "使用JMeter进行Web应用性能测试，包括脚本录制、压力测试、结果分析等实战内容。", "JMeter,性能测试,压测"),
        ("Sublime Text 4高效编辑器配置", "轻量级代码编辑器Sublime Text的配置优化、插件推荐、自定义快捷键等使用技巧。", "Sublime Text,编辑器,效率"),
        (" iTerm2+tmux终端复用最佳实践", "使用iTerm2配合tmux实现终端复用、分屏、会话管理，提升命令行工作效率。", "iTerm2,tmux,终端"),
        ("Robo 3T MongoDB可视化管理工具", "MongoDB图形化管理工具，支持数据库浏览、查询构建、索引管理、聚合管道等功能。", "MongoDB,可视化管理,NoSQL"),
        ("Webpack5模块打包工具深度配置", "详解Webpack5配置，包括Loader、Plugin、代码分割、Tree Shaking、缓存优化等。", "Webpack,打包,前端构建"),
        ("Vite前端构建工具实战配置", "使用Vite快速搭建前端项目，包括插件开发、构建优化、SSR配置、库模式打包等。", "Vite,构建工具,前端"),
        ("ESLint+Prettier代码规范配置模板", "一套完整的ESLint和Prettier代码规范配置方案，支持JavaScript、TypeScript、Vue、React。", "ESLint,Prettier,代码规范"),
        ("Swagger/OpenAPI接口文档生成工具", "使用Swagger自动生成REST API文档，支持在线测试、Schema定义、代码生成等功能。", "Swagger,API文档,OpenAPI"),
        ("SourceTree免费Git图形化客户端", "Atlassian出品的Git图形化工具，支持Git Flow、合并冲突、代码审查等版本控制操作。", "SourceTree,Git,版本控制"),
        ("Electron桌面应用开发框架入门", "使用Web技术开发跨平台桌面应用，包括窗口管理、系统托盘、自动更新等桌面端功能。", "Electron,桌面开发,跨平台"),
        ("Hoppscotch轻量级API测试工具", "开源的API测试工具，支持WebSocket、SSE、GraphQL等多种协议，界面简洁高效。", "Hoppscotch,API测试,开源"),
        ("TablePlus数据库管理工具", "现代化数据库管理工具，支持多种数据库，界面美观、查询高效、支持SSH隧道连接。", "TablePlus,数据库,管理工具"),
        ("Syncthing文件同步工具配置指南", "开源的持续文件同步工具，支持多设备间实时同步，无需中央服务器，数据完全自控。", "Syncthing,文件同步,开源"),
        ("DBeaver通用数据库管理工具", "免费的通用数据库管理工具，支持MySQL、PostgreSQL、Oracle等几乎所有主流数据库。", "DBeaver,数据库,管理工具"),
        ("htop系统监控工具使用教程", "Linux系统进程监控工具，实时查看CPU、内存、进程状态，比top更直观强大。", "htop,系统监控,Linux"),
        ("Proxyman macOS抓包调试工具", "macOS原生HTTP调试代理工具，支持HTTPS解密、断点调试、Map Local等高级功能。", "Proxyman,抓包,macOS"),
        ("Cmd Markdown编辑器写作工具", "功能强大的Markdown编辑器，支持实时预览、数学公式、流程图、多平台同步。", "Markdown,编辑器,写作"),
        ("Typora Markdown写作利器", "所见即所得的Markdown编辑器，支持LaTeX公式、代码高亮、主题切换、导出多格式。", "Typora,Markdown,写作"),
        ("Apifox API一体化协作平台", "集成API设计、调试、文档、Mock于一体的API开发协作平台，支持团队协作。", "Apifox,API,协作"),
        ("Lazydocker Docker终端管理UI", "使用终端UI管理Docker容器、镜像、日志、卷，比命令行更直观高效。", "Lazydocker,Docker,终端"),
        ("Insomnia REST API调试客户端", "简洁高效的API调试工具，支持REST、GraphQL、gRPC，支持环境变量和代码生成。", "Insomnia,API,调试"),
        ("Portainer Docker可视化管理平台", "Docker容器可视化管理平台，支持容器部署、监控、日志查看、Swarm集群管理。", "Portainer,Docker,管理平台"),
    ],
    4: [
        ("Vue3组件库开发完整模板", "基于Vue3+TypeScript的企业级组件库开发模板，包含文档站、单元测试、CI/CD配置。", "Vue3,组件库,TypeScript"),
        ("Spring Boot微服务项目脚手架", "Spring Boot 3.x微服务项目模板，集成MyBatis-Plus、Redis、RabbitMQ、Swagger等常用组件。", "Spring Boot,微服务,脚手架"),
        ("React Admin后台管理系统模板", "基于React18+Ant Design Pro的后台管理系统模板，包含权限管理、用户管理、数据字典等。", "React,后台管理,Ant Design"),
        ("Flutter电商App完整源码", "Flutter开发的完整电商应用，包含商品列表、购物车、订单、支付、用户中心等模块。", "Flutter,电商,App"),
        ("Next.js博客系统完整模板", "基于Next.js 14的博客系统，支持MDX文章、标签分类、评论系统、SEO优化。", "Next.js,博客,SSR"),
        ("Django REST Framework API模板", "Django REST Framework项目模板，包含用户认证、权限管理、API文档、测试用例。", "Django,REST API,Python"),
        ("Express.js+MongoDB全栈项目模板", "Express.js后端配合MongoDB数据库的全栈项目模板，包含JWT认证、CRUD操作。", "Express,MongoDB,全栈"),
        ("Android MVVM架构模板项目", "Android MVVM架构项目模板，使用Kotlin+Jetpack组件，包含网络请求、数据持久化。", "Android,Kotlin,MVVM"),
        ("Go Gin RESTful API项目模板", "基于Gin框架的Go语言RESTful API项目模板，包含中间件、数据库操作、Swagger文档。", "Go,Gin,RESTful"),
        ("Vue3+Electron桌面应用模板", "Vue3配合Electron构建桌面应用的模板，包含自动更新、系统托盘、本地存储等功能。", "Vue3,Electron,桌面应用"),
        ("Rust Actix Web API项目模板", "使用Rust Actix Web框架构建高性能API服务，包含JWT认证、数据库连接池、错误处理。", "Rust,Actix Web,API"),
        ("微信小程序商城完整源码", "微信小程序商城完整项目，包含商品展示、购物车、微信支付、订单管理等功能。", "微信小程序,商城,电商"),
        ("Node.js+Socket.io即时通讯系统", "基于Node.js和Socket.io的即时通讯系统，支持私聊、群聊、图片发送、消息记录。", "Node.js,Socket.io,即时通讯"),
        ("Spring Cloud微服务架构模板", "Spring Cloud Alibaba微服务架构模板，集成Nacos、Gateway、Sentinel、Seata等组件。", "Spring Cloud,微服务,阿里巴巴"),
        ("React Native跨平台App模板", "React Native项目模板，包含导航、状态管理、网络请求、原生模块封装等最佳实践。", "React Native,跨平台,App"),
        ("Python FastAPI项目脚手架", "FastAPI项目模板，集成SQLAlchemy、Alembic迁移、JWT认证、Docker部署配置。", "FastAPI,Python,脚手架"),
        ("Tailwind CSS企业官网模板", "使用Tailwind CSS构建的现代化企业官网模板，支持响应式、暗色模式、SEO优化。", "Tailwind CSS,官网,响应式"),
        ("Uni-app跨平台应用开发模板", "基于uni-app的跨平台应用模板，一套代码同时发布到微信、支付宝、H5、App。", "uni-app,跨平台,小程序"),
        ("GraphQL全栈项目模板", "前后端GraphQL全栈项目模板，使用Apollo Client/Server，包含订阅、缓存策略。", "GraphQL,Apollo,全栈"),
        ("Ktor Kotlin后端API模板", "使用Ktor框架构建Kotlin后端API服务，包含JWT认证、数据库访问、CORS配置。", "Ktor,Kotlin,后端"),
        ("Svelte+SvelteKit全栈应用模板", "SvelteKit全栈项目模板，包含SSR、API Routes、表单处理、数据库集成。", "Svelte,SvelteKit,前端"),
        ("Python Scrapy爬虫项目模板", "Scrapy爬虫项目模板，包含中间件、管道、代理池、数据存储、定时任务等完整配置。", "Scrapy,爬虫,Python"),
        ("Ionic+Angular混合App开发模板", "Ionic+Angular混合移动应用模板，支持iOS/Android打包、推送通知、本地存储。", "Ionic,Angular,混合开发"),
        ("Nuxt.js全栈电商模板", "Nuxt.js 3电商项目模板，包含商品管理、购物车、结算、Stripe支付集成。", "Nuxt.js,电商,SSR"),
        ("ASP.NET Core Web API模板", "ASP.NET Core 8 Web API项目模板，包含Entity Framework、JWT认证、Swagger文档。", "ASP.NET Core,C#,Web API"),
        ("Taro跨端小程序开发模板", "使用Taro框架开发多端小程序，支持React/Vue语法，一键编译到多个小程序平台。", "Taro,小程序,跨端"),
        ("Kafka消息队列项目实战模板", "Kafka消息队列项目模板，包含生产者消费者、分区策略、消费者组、消息确认等。", "Kafka,消息队列,大数据"),
        ("Electron+React桌面Markdown编辑器", "基于Electron和React的桌面Markdown编辑器，支持实时预览、主题切换、文件管理。", "Electron,Markdown,桌面应用"),
        ("Go-Zero微服务API网关模板", "Go-Zero微服务框架项目模板，包含API网关、RPC服务、代码生成、服务注册发现。", "Go-Zero,微服务,Go"),
        ("Three.js 3D可视化项目模板", "Three.js 3D可视化项目模板，包含场景搭建、模型加载、光照材质、动画控制等。", "Three.js,3D,可视化"),
        ("Gin+Gorm+Casbin权限管理系统", "Go语言后台权限管理系统，使用Casbin实现RBAC权限控制，支持菜单和按钮级别权限。", "Go,Gin,权限管理"),
        ("Flutter+Firebase全栈App模板", "Flutter配合Firebase的完整应用模板，包含认证、实时数据库、云存储、推送通知。", "Flutter,Firebase,全栈"),
        ("SolidJS前端项目模板", "SolidJS响应式前端框架项目模板，包含路由、状态管理、SSR配置、TypeScript集成。", "SolidJS,前端,响应式"),
        ("Remix全栈Web应用模板", "Remix全栈框架项目模板，包含Loader/Action模式、表单验证、数据库集成。", "Remix,全栈,Web"),
        ("Elasticsearch+Kibana数据分析平台", "基于Elasticsearch和Kibana的数据分析平台模板，包含数据采集、索引管理、可视化面板。", "Elasticsearch,Kibana,数据分析"),
    ],
    5: [
        ("2025前端面试高频题库大全", "涵盖HTML/CSS/JavaScript/React/Vue/网络/算法等前端面试高频题目和详细解答。", "前端面试,题库,JavaScript"),
        ("Java后端面试八股文精编版", "Java后端面试核心知识点整理，包括JVM、并发、Spring、数据库、分布式等专题。", "Java面试,八股文,后端"),
        ("Python数据分析学习路线图", "从零到数据分析工程师的完整学习路线，包括工具学习、项目实战、求职指导。", "Python,数据分析,学习路线"),
        ("系统设计面试通关秘籍", "系统设计面试备考指南，包含缓存、消息队列、分布式系统、高可用等设计题解析。", "系统设计,面试,架构"),
        ("机器学习数学基础速查手册", "机器学习所需的线性代数、概率统计、微积分、优化理论等数学基础知识速查。", "机器学习,数学,基础"),
        ("CSS Flexbox与Grid布局完全指南", "CSS现代布局技术完全指南，通过大量示例掌握Flexbox和Grid的各类布局方案。", "CSS,Flexbox,Grid"),
        ("Git命令速查表（完整版）", "Git常用和进阶命令速查表，覆盖初始化、分支、合并、远程、撤销、标签等操作。", "Git,命令,速查表"),
        ("HTTP状态码完整参考手册", "HTTP状态码完整分类和含义说明，包括1xx到5xx所有常用状态码的详细解释。", "HTTP,状态码,参考手册"),
        ("SQL语法速查手册", "SQL语法快速参考，覆盖DDL、DML、聚合函数、JOIN、子查询、窗口函数等。", "SQL,速查,数据库"),
        ("正则表达式入门与实战指南", "从基础语法到高级技巧的正则表达式学习指南，配合常见场景的实战练习。", "正则表达式,入门,实战"),
        ("LeetCode刷题笔记（TOP 100）", "LeetCode热题100道详细解题笔记，包含思路分析、代码实现、复杂度分析。", "LeetCode,算法,刷题"),
        ("设计模式速查手册（Java版）", "23种GoF设计模式的快速参考手册，包含UML类图、核心代码、应用场景说明。", "设计模式,Java,速查"),
        ("React Hooks完全使用指南", "React Hooks从useState到自定义Hook的完整使用指南，配合最佳实践和常见陷阱。", "React,Hooks,前端"),
        ("TypeScript类型体操练习集", "TypeScript高级类型编程练习题集，涵盖条件类型、模板字面量类型、递归类型等。", "TypeScript,类型体操,练习"),
        ("Linux常用命令手册（运维必备）", "Linux运维常用命令手册，覆盖文件操作、进程管理、网络配置、磁盘管理等分类。", "Linux,命令,运维"),
        ("Docker命令速查手册", "Docker常用命令快速参考，包括镜像管理、容器操作、网络配置、数据卷等。", "Docker,命令,速查"),
        ("Kubernetes核心概念速查手册", "K8s核心概念和kubectl命令速查手册，涵盖Pod、Service、Deployment等资源对象。", "Kubernetes,K8s,速查"),
        ("Nginx配置模板集合", "Nginx常用配置模板集合，包括反向代理、HTTPS、负载均衡、缓存、限流等场景。", "Nginx,配置,模板"),
        ("Redis数据结构与命令参考", "Redis五种基本数据结构和常用命令参考手册，包含使用场景和性能说明。", "Redis,数据结构,命令"),
        ("MySQL索引优化实战笔记", "MySQL索引原理和优化实战笔记，包括索引类型、最左前缀、覆盖索引、执行计划。", "MySQL,索引,优化"),
        ("Vue3 Composition API完全指南", "Vue3组合式API完整使用指南，包括响应式原理、自定义Hook、性能优化技巧。", "Vue3,Composition API,前端"),
        ("Spring Boot自动配置原理笔记", "深入理解Spring Boot自动配置机制，从@EnableAutoConfiguration到条件注解。", "Spring Boot,自动配置,原理"),
        ("JVM垃圾收集器对比与选择指南", "JVM各种垃圾收集器的原理、特点、适用场景对比，帮助选择最优GC方案。", "JVM,GC,垃圾收集"),
        ("分布式系统CAP理论详解", "分布式系统CAP理论、BASE理论详解，配合常见分布式系统的设计取舍分析。", "分布式,CAP,理论"),
        ("网络安全常见攻击与防御速查", "XSS、CSRF、SQL注入、DDoS等常见Web安全攻击原理和防御方案速查。", "网络安全,防御,速查"),
        ("API设计规范与RESTful最佳实践", "RESTful API设计规范和最佳实践，包括URL设计、状态码、分页、版本管理等。", "API,RESTful,设计规范"),
        ("微前端架构设计方案笔记", "微前端架构设计方案对比，包括qiankun、Module Federation、iframe等方案分析。", "微前端,架构,前端"),
        ("消息队列选型对比分析", "Kafka、RabbitMQ、RocketMQ、Pulsar四种消息队列的对比分析和选型建议。", "消息队列,Kafka,选型"),
        ("数据库分库分表方案设计笔记", "数据库水平分片、垂直分片的设计方案，包括分片策略、唯一ID、跨片查询等。", "数据库,分库分表,架构"),
        ("OAuth2.0与JWT认证流程详解", "OAuth2.0授权流程和JWT令牌机制的详解，包含四种授权模式和最佳安全实践。", "OAuth2,JWT,认证"),
        ("Web性能优化Checklist", "Web性能优化全面检查清单，涵盖网络、渲染、JavaScript、CSS、图片等优化维度。", "性能优化,Web,Checklist"),
        ("敏捷开发Scrum实践指南", "Scrum敏捷开发框架实践指南，包括角色、仪式、工件、Sprint规划等核心概念。", "敏捷开发,Scrum,项目管理"),
        ("代码审查Code Review最佳实践", "代码审查流程规范和最佳实践，包括审查清单、常见问题、沟通技巧等。", "Code Review,代码质量,实践"),
        ("CI/CD流水线设计指南", "持续集成和持续部署流水线设计指南，包括构建、测试、部署、回滚等阶段设计。", "CI/CD,流水线,DevOps"),
        ("云原生技术栈学习路线图", "云原生技术栈完整学习路线，涵盖容器、编排、服务网格、可观测性等技术领域。", "云原生,学习路线,Kubernetes"),
        ("WebAssembly入门与实践指南", "WebAssembly技术入门指南，包括WAT语法、与JavaScript互操作、性能优化等。", "WebAssembly,WASM,前端"),
        ("GraphQL vs REST对比分析", "GraphQL和REST两种API设计风格的全面对比，帮助在项目中做出合理选择。", "GraphQL,REST,API"),
        ("函数式编程入门（JavaScript版）", "使用JavaScript学习函数式编程，包括纯函数、高阶函数、柯里化、Monad等概念。", "函数式编程,JavaScript,编程范式"),
        ("并发编程模型对比分析", "线程、协程、Actor、CSP等并发编程模型的原理对比和适用场景分析。", "并发,编程模型,对比"),
        ("BTree与LSMTree存储引擎原理", "B+Tree和LSM Tree两种存储引擎的数据结构和读写原理对比分析。", "存储引擎,BTree,LSM"),
    ],
    6: [
        ("100+免费高质量UI图标库合集", "精选100+免费商业可用的图标库，涵盖线性、面性、手绘等多种风格，支持SVG/PNG。", "图标,UI设计,免费资源"),
        ("响应式企业官网HTML模板", "现代化响应式企业官网HTML模板，包含首页、关于、产品、博客、联系等完整页面。", "企业官网,HTML,响应式"),
        ("扁平化插画素材包（50张）", "50张精美扁平化插画素材，涵盖办公、科技、教育、社交等主题，支持AI/SVG/PNG格式。", "插画,扁平化,素材"),
        ("渐变背景生成器工具", "在线渐变背景生成工具，支持线性/径向渐变、自定义色标、CSS代码一键复制。", "渐变,背景,CSS工具"),
        ("Material Design配色方案大全", "Google Material Design风格配色方案集合，包含500+精选配色，支持一键复制色值。", "配色,Material Design,设计"),
        ("60+免费英文字体打包下载", "精选60+免费商用英文字体，涵盖衬线、无衬线、手写、等宽等多种类型。", "字体,英文,免费商用"),
        ("Sketch UI组件库模板", "Sketch设计工具的UI组件库模板，包含按钮、表单、卡片、导航等常用组件。", "Sketch,组件库,UI"),
        ("Figma设计系统模板", "Figma设计系统模板，包含颜色规范、字体规范、间距系统、组件库等设计标准。", "Figma,设计系统,模板"),
        ("404错误页面创意模板合集", "20+创意404错误页面HTML模板，动画效果丰富，提升用户体验。", "404,错误页面,创意"),
        ("CSS动画效果代码集合", "50+常用CSS动画效果代码集合，包括淡入淡出、滑动、旋转、弹跳等动画。", "CSS,动画,效果"),
        ("landing page着陆页设计模板", "10个高转化率着陆页HTML模板，适合产品发布、活动推广、用户注册等场景。", "着陆页,Landing Page,模板"),
        ("SVG波浪分隔线素材", "精美的SVG波浪分隔线素材集合，用于网页区域分隔，支持自定义颜色和形状。", "SVG,波浪,分隔线"),
        ("移动端App UI Kit设计稿", "完整的移动端App UI Kit设计稿，包含登录、首页、个人中心、设置等40+页面。", "App UI,移动端,设计稿"),
        ("后台管理系统UI模板（暗色主题）", "暗色主题的后台管理系统UI模板，包含仪表盘、表格、表单、图表等完整组件。", "后台管理,暗色,UI模板"),
        ("Bootstrap5企业级网站模板", "基于Bootstrap5的企业级网站模板，包含30+页面模板，响应式设计，开箱即用。", "Bootstrap,企业,网站模板"),
        ("免费矢量图标包（1000+）", "1000+免费矢量图标，支持SVG/PNG/AI格式，涵盖常用UI、社交、电商等分类。", "矢量图标,免费,SVG"),
        ("网页Banner设计素材合集", "精选网页Banner设计PSD/AI源文件，涵盖促销、节日、新品等常见场景。", "Banner,设计素材,PSD"),
        ("Tailwind CSS UI组件模板", "基于Tailwind CSS的UI组件模板集合，包含按钮、卡片、导航、表单等常用组件。", "Tailwind CSS,组件,UI"),
        ("电商App界面设计PSD模板", "完整电商App界面设计PSD模板，包含首页、分类、商品详情、购物车等页面。", "电商,App,PSD模板"),
        ("加载动画SVG素材包", "30+精美加载动画SVG素材，包括旋转、跳动、进度条等样式，可直接嵌入网页。", "加载动画,SVG,等待"),
        ("中文免费商用字体合集", "精选20+中文免费商用字体下载，涵盖宋体、黑体、楷体、手写等多种风格。", "中文字体,免费商用,字体"),
        ("Dashboard数据看板UI模板", "数据看板Dashboard UI模板，包含折线图、饼图、柱状图等数据可视化组件。", "Dashboard,数据看板,UI"),
        ("商务PPT模板合集（50套）", "50套精美商务PPT模板，涵盖工作汇报、项目方案、产品发布等职场常用场景。", "PPT,商务,模板"),
        ("社交媒体图片尺寸规范速查", "各大社交媒体平台图片尺寸规范速查表，包括微信、微博、抖音、小红书等平台。", "社交媒体,图片尺寸,规范"),
        ("网页配色方案生成器", "在线网页配色方案生成工具，支持互补色、类似色、三角色等多种配色方案。", "配色,网页设计,工具"),
        ("iOS App UI Kit设计模板", "iOS风格App UI Kit设计模板，符合Apple Human Interface Guidelines设计规范。", "iOS,UI Kit,设计"),
        ("Material Design UI Kit", "Google Material Design风格UI Kit，包含完整的Material组件和设计规范。", "Material Design,UI Kit,Android"),
        ("电商Banner PSD源文件合集", "30+电商Banner设计PSD源文件，包含双11、618、年货节等促销场景。", "电商,Banner,PSD"),
        ("个人简历网页模板", "精美个人简历网页HTML模板，包含技能展示、项目经验、联系方式等模块。", "简历,个人,网页模板"),
        ("博客网站HTML模板", "简洁优雅的博客网站HTML模板，支持文章列表、分类、标签、搜索等功能。", "博客,网站,HTML模板"),
        ("Ant Design组件Figma源文件", "Ant Design组件库的Figma源文件，包含所有Ant Design组件的设计稿。", "Ant Design,Figma,组件"),
        ("水印纹理背景素材包", "50+精美纹理背景素材，涵盖纸张、布料、石材、金属等纹理效果。", "纹理,背景,素材"),
        ("emoji表情包素材合集", "精选emoji表情包素材，支持PNG/SVG格式，可用于聊天应用、网站评论等场景。", "emoji,表情,素材"),
        ("摄影图片免费图库合集", "10个免费高质量摄影图片网站合集，可商用，涵盖自然、人物、科技等主题。", "图库,免费,摄影"),
        ("3D图标素材包", "精美3D风格图标素材包，包含常用UI图标、社交图标等，支持PNG/Blender格式。", "3D图标,素材,立体"),
    ],
}


def seed():
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    db.row_factory = sqlite3.Row

    cur = db.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
    admin = cur.fetchone()
    if not admin:
        print("ERROR: no admin user found. Run seed_data.py first.")
        db.close()
        return
    uploader_id = admin["id"]

    cur = db.execute("SELECT id FROM categories ORDER BY sort_order")
    categories = cur.fetchall()
    if not categories:
        print("ERROR: no categories found.")
        db.close()
        return

    existing = db.execute("SELECT COUNT(*) as cnt FROM resources")
    cnt = existing.fetchone()["cnt"]
    if cnt > 0:
        print(f"Resources table already has {cnt} records. Skipping seed.")
        db.close()
        return

    total = 0
    now = datetime.now()
    for cat in categories:
        cat_id = cat["id"]
        items = RESOURCES_DATA.get(cat_id, [])
        for i, (title, summary, tags) in enumerate(items):
            days_ago = random.randint(0, 60)
            hours_ago = random.randint(0, 23)
            upload_time = now - timedelta(days=days_ago, hours=hours_ago)
            view_count = random.randint(50, 5000)
            favorite_count = random.randint(0, view_count // 10)
            is_hot = 1 if view_count > 3000 and random.random() > 0.3 else 0
            file_size = random.choice([
                random.randint(1024 * 1024, 50 * 1024 * 1024),
                random.randint(50 * 1024 * 1024, 500 * 1024 * 1024),
                random.randint(1, 100) * 1024 * 1024,
            ])
            db.execute(
                """INSERT INTO resources
                   (title, summary, category_id, tags, link, link_password, file_size,
                    upload_time, is_hot, view_count, favorite_count, uploader_id, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (title, summary, cat_id, tags, "", "", file_size,
                 upload_time.strftime("%Y-%m-%d %H:%M:%S"),
                 is_hot, view_count, favorite_count, uploader_id, "published"),
            )
            total += 1

    db.commit()
    db.close()
    print(f"Seeded {total} resources across {len(categories)} categories.")


if __name__ == "__main__":
    seed()
