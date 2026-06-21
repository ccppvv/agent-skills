# 架构图类型详解

## 1. 业务架构图 (Business Architecture)

### 定义
描述业务能力、业务流程、组织架构及其之间的关系。

### 关键要素
- 业务领域/模块
- 业务能力
- 业务流程
- 用户角色
- 业务规则

### 最佳实践
- 从用户视角出发
- 避免技术细节
- 突出业务价值流
- 标注关键决策点

### 模板
```mermaid
graph TB
    subgraph "客户管理域"
        CRM[客户信息管理]
        Lead[线索管理]
    end
    
    subgraph "订单管理域"
        Order[订单处理]
        Payment[支付管理]
    end
    
    subgraph "库存管理域"
        Stock[库存管理]
        Warehouse[仓储管理]
    end
    
    CRM --> Lead
    Lead --> Order
    Order --> Payment
    Order --> Stock
    Stock --> Warehouse
```

## 2. 应用架构图 (Application Architecture)

### 定义
描述应用系统的组成、交互关系和数据流。

### 关键要素
- 应用系统/服务
- API 接口
- 数据流
- 集成点
- 安全边界

### 最佳实践
- 明确系统边界
- 标注通信协议
- 区分同步/异步
- 突出核心应用

### 模板
```mermaid
graph TB
    subgraph "前端应用"
        WebApp[Web 应用]
        MobileApp[移动 App]
    end
    
    Gateway[API 网关]
    
    subgraph "后端服务"
        UserService[用户服务]
        OrderService[订单服务]
        PaymentService[支付服务]
    end
    
    subgraph "数据存储"
        MySQL[(MySQL)]
        Redis[(Redis)]
        MQ[消息队列]
    end
    
    WebApp --> Gateway
    MobileApp --> Gateway
    Gateway --> UserService
    Gateway --> OrderService
    Gateway --> PaymentService
    
    UserService --> MySQL
    OrderService --> MySQL
    PaymentService --> MySQL
    
    UserService --> Redis
    OrderService --> MQ
```

## 3. 技术架构图 (Technology Architecture)

### 定义
描述技术栈选型、技术组件及其层次关系。

### 关键要素
- 技术框架
- 编程语言
- 中间件
- 开发工具
- 技术标准

### 最佳实践
- 分层展示
- 标注版本号
- 说明选型理由
- 考虑技术债务

### 模板
```mermaid
graph TB
    subgraph "前端技术栈"
        React[React 18.2]
        TS[TypeScript 5.0]
        Vite[Vite 4.0]
    end
    
    subgraph "后端技术栈"
        Node[Node.js 20]
        Express[Express 4.18]
        Prisma[Prisma ORM]
    end
    
    subgraph "基础设施"
        Docker[Docker]
        K8s[Kubernetes]
        Nginx[Nginx]
    end
    
    subgraph "数据技术"
        PG[(PostgreSQL 15)]
        RedisDB[(Redis 7)]
        ES[(Elasticsearch 8)]
    end
```

## 4. 部署架构图 (Deployment Architecture)

### 定义
描述系统的物理部署、网络拓扑和运行环境。

### 关键要素
- 服务器/容器
- 网络设备
- 负载均衡
- 存储设备
- 安全组件

### 最佳实践
- 标注IP地址/端口
- 明确网络边界
- 标识单点故障
- 展示灾备方案

### 模板
```mermaid
graph TB
    subgraph "用户端"
        Users[用户]
    end
    
    subgraph "CDN 层"
        CDN[CDN]
    end
    
    subgraph "负载均衡层"
        LB1[LB-1<br/>主]
        LB2[LB-2<br/>备]
    end
    
    subgraph "应用服务器集群"
        App1[App-1<br/>10.0.1.11]
        App2[App-2<br/>10.0.1.12]
        App3[App-3<br/>10.0.1.13]
    end
    
    subgraph "数据库集群"
        Master[(Master<br/>10.0.2.10)]
        Slave1[(Slave-1<br/>10.0.2.11)]
        Slave2[(Slave-2<br/>10.0.2.12)]
    end
    
    Users --> CDN
    CDN --> LB1
    LB1 -.备份.-> LB2
    LB1 --> App1 & App2 & App3
    App1 & App2 & App3 --> Master
    Master --> Slave1 & Slave2
```

## 5. 数据架构图 (Data Architecture)

### 定义
描述数据的存储、流转和处理方式。

### 关键要素
- 数据源
- 数据流向
- 数据存储
- 数据处理
- 数据质量

### 最佳实践
- 标注数据类型
- 说明数据量级
- 标识实时/批处理
- 关注数据安全

### 模板
```mermaid
graph LR
    subgraph "数据采集"
        App[应用日志]
        DB[数据库CDC]
        API[API 接口]
    end
    
    subgraph "数据传输"
        Kafka[Kafka]
    end
    
    subgraph "数据处理"
        Flink[实时处理<br/>Flink]
        Spark[批处理<br/>Spark]
    end
    
    subgraph "数据存储"
        DW[(数据仓库)]
        Lake[(数据湖)]
        OLAP[(OLAP)]
    end
    
    subgraph "数据应用"
        BI[BI 报表]
        ML[机器学习]
    end
    
    App --> Kafka
    DB --> Kafka
    API --> Kafka
    
    Kafka --> Flink
    Kafka --> Spark
    
    Flink --> OLAP
    Spark --> DW
    Spark --> Lake
    
    DW --> BI
    Lake --> ML
```

## 6. 时序图 (Sequence Diagram)

### 定义
描述组件间按时间顺序的交互过程。

### 关键要素
- 参与者
- 消息
- 激活期
- 返回值
- 循环/条件

### 最佳实践
- 从左到右排列参与者
- 标注消息编号
- 区分同步/异步
- 突出关键路径

### 模板
```mermaid
sequenceDiagram
    participant U as 用户
    participant W as Web前端
    participant G as API网关
    participant A as 订单服务
    participant P as 支付服务
    participant D as 数据库
    
    U->>W: 1. 提交订单
    activate W
    W->>G: 2. POST /orders
    activate G
    G->>A: 3. 创建订单
    activate A
    A->>D: 4. 保存订单
    activate D
    D-->>A: 5. 订单ID
    deactivate D
    A->>P: 6. 发起支付
    activate P
    P-->>A: 7. 支付结果
    deactivate P
    A-->>G: 8. 订单详情
    deactivate A
    G-->>W: 9. 响应数据
    deactivate G
    W-->>U: 10. 显示结果
    deactivate W
```

## 7. C4 模型 (Context, Container, Component, Code)

### Level 1: 系统上下文图
```mermaid
graph TB
    User[用户]
    System[电商系统]
    Payment[支付平台]
    Logistics[物流系统]
    
    User -->|使用| System
    System -->|支付| Payment
    System -->|发货| Logistics
```

### Level 2: 容器图
```mermaid
graph TB
    subgraph "电商系统"
        Web[Web 应用<br/>React]
        API[API 服务<br/>Node.js]
        DB[(数据库<br/>PostgreSQL)]
        Cache[(缓存<br/>Redis)]
    end
    
    Web --> API
    API --> DB
    API --> Cache
```

### Level 3: 组件图
```mermaid
graph TB
    subgraph "订单服务"
        Controller[订单控制器]
        Service[订单业务逻辑]
        Repo[订单仓储]
        Event[事件发布]
    end
    
    Controller --> Service
    Service --> Repo
    Service --> Event
```

### Level 4: 代码图
- 通常使用 UML 类图
- 展示类、接口、关系
- 在 SKILL 中不详细展开

## 选择指南

| 场景 | 推荐类型 | 原因 |
|------|---------|------|
| 向业务人员介绍系统 | 业务架构图 | 无技术术语，易理解 |
| 技术方案评审 | 技术架构图 + 应用架构图 | 全面展示技术选型 |
| 运维部署 | 部署架构图 | 物理部署清晰 |
| 数据治理 | 数据架构图 | 数据流向明确 |
| 接口对接 | 时序图 | 交互顺序清楚 |
| 系统设计面试 | C4 模型 | 分层次递进展示 |
