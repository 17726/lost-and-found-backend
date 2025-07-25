# 校园失物招领平台 - 后端服务 (Lost & Found - Backend)

这是一个旨在解决校园信息不对称问题的全栈Web应用之后端服务。项目从零开始，独立开发，旨在实践并掌握现代Web后端开发的完整流程。

> **前端项目地址**: [lost-and-found-frontend](https://github.com/17726/lost-and-found-frontend)

---

## ✨ 项目亮点 (Highlights)

*   **RESTful API 设计**: 遵循RESTful最佳实践，提供清晰、规范的API接口。
*   **前后端分离架构**: 与Vue 3前端项目完全分离，通过Token进行无状态认证，支持未来扩展到移动端等其他客户端。
*   **模块化开发**: 基于Django App进行功能解耦，项目结构清晰，易于维护和扩展。
*   **权限与安全**: 实现了精细化的权限控制（如“仅所有者可编辑”）和基础的安全实践。

## 🚀 技术栈 (Tech Stack)

*   **框架**: Python, Django, Django REST Framework (DRF)
*   **数据库**: SQLite (开发阶段), PostgreSQL (生产规划)
*   **认证**: `TokenAuthentication` (基于Token的无状态认证)
*   **实时通讯 (规划中)**: Django Channels, WebSocket
*   **API文档与测试**: Apifox

##  API 功能模块

项目API严格遵循预先设计的[API文档](<>)进行开发。

-   [x] **模块一：用户认证 (User Authentication)**
    -   `POST /api/register/`: 用户注册
    -   `POST /api/login/`: 用户登录，获取Token
-   [x] **模块二：物品信息 (Items)**
    -   `GET /api/items/`: 获取/搜索/筛选物品列表
    -   `POST /api/items/`: 发布新物品
    -   `GET /api/items/{id}/`: 获取单个物品详情
    -   `PATCH /api/items/{id}/`: 修改物品信息 (仅所有者)
    -   `DELETE /api/items/{id}/`: 删除物品 (仅所有者)
-   [ ] **模块三：智能匹配与个人中心 (Matching & Personal)**
    -   `GET /api/items/{id}/matches/`: 获取物品的智能匹配结果
    -   `GET /api/items/mine/`: 获取我发布的所有物品
-   [ ] **模块四：站内信 (Chat)**
    -   `GET /api/rooms/`: 获取聊天室列表
    -   `POST /api/rooms/`: 创建/进入聊天室
    -   `GET /api/rooms/{room_name}/messages/`: 获取历史消息
    -   `POST /api/rooms/{room_name}/mark_as_read/`: 标记已读

## 本地开发指南

1.  克隆项目到本地:
    ```bash
    git clone git@github.com:17726/lost-and-found-backend.git
    cd lost-and-found-backend
    ```
2.  创建并激活Python虚拟环境:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```
3.  安装项目依赖:
    ```bash
    pip install -r requirements.txt
    ```
4.  执行数据库迁移:
    ```bash
    python manage.py migrate
    ```
5.  启动开发服务器:
    ```bash
    python manage.py runserver
    ```
    服务将在 `http://127.0.0.1:8000` 启动。

## 学习与成长记录

*   **2025.07.15**: 项目启动。完成了基于DRF的Token认证系统，实现了用户注册与登录功能。
*   **2025.07.22**: 完成了物品信息模块的全部CRUD API，并实现了基于`IsOwnerOrReadOnly`的自定义对象级权限控制。

---
It's time to start！