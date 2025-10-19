# 📚 项目文档中心

**客户资料收集系统 (CCD) - 文档导航**

---

## 🎯 快速导航

### 新用户从这里开始

| 文档 | 说明 | 位置 |
|------|------|------|
| **README.md** | 项目概述和技术架构 | 项目根目录 |
| **QUICK_START.md** | 快速开始指南 | 项目根目录 |
| **用户使用指南** | 完整操作手册 | docs/guides/USER_GUIDE.md |

### 开发者文档

| 文档 | 说明 | 位置 |
|------|------|------|
| **后端文档** | Django后端开发文档 | backend/README.md |
| **前端文档** | Vue前端开发文档 | frontend/README.md |
| **部署文档** | 生产环境部署指南 | deployment/README.md |

---

## 📖 文档列表

### 核心文档

#### 1. 项目说明
- **README.md** - 项目概述、技术架构、功能介绍
- **PROJECT_SUMMARY.md** - 项目总结
- **PROJECT_STRUCTURE.md** - 项目结构说明

#### 2. 开始使用
- **QUICK_START.md** - 快速开始指南（英文）
- **WINDOWS_SETUP_CN.md** - Windows环境设置指南（中文）
- **docs/guides/USER_GUIDE.md** - 完整用户使用手册

#### 3. 变更记录
- **CHANGELOG.md** - 版本更新日志
- **docs/PROJECT_CHANGELOG.md** - 详细项目更新记录

---

## 📂 文档目录结构

```
CCD/
├── README.md                      # 项目主文档
├── QUICK_START.md                 # 快速开始
├── CHANGELOG.md                   # 更新日志
├── PROJECT_SUMMARY.md             # 项目总结
├── PROJECT_STRUCTURE.md           # 项目结构
├── WINDOWS_SETUP_CN.md            # Windows设置
│
├── docs/                          # 文档中心
│   ├── README.md                  # 文档导航（本文件）
│   ├── PROJECT_CHANGELOG.md       # 详细更新记录
│   │
│   ├── guides/                    # 用户指南
│   │   └── USER_GUIDE.md         # 完整用户手册
│   │
│   └── history/                   # 历史记录（已归档）
│       └── ...                   # 旧的诊断和修复报告
│
├── backend/                       # 后端代码
│   └── README.md                  # 后端文档
│
├── frontend/                      # 前端代码
│   └── README.md                  # 前端文档
│
└── deployment/                    # 部署配置
    └── README.md                  # 部署文档
```

---

## 🎓 按角色查找文档

### 👥 最终用户
1. **docs/guides/USER_GUIDE.md** - 系统使用完整指南
   - 如何登录系统
   - 如何管理客户
   - 如何上传和预览文件
   - 常见问题解答

### 👨‍💼 项目经理
1. **PROJECT_SUMMARY.md** - 项目整体情况
2. **docs/PROJECT_CHANGELOG.md** - 功能完成情况
3. **CHANGELOG.md** - 版本历史

### 👨‍💻 开发人员

#### 后端开发
1. **backend/README.md** - 后端开发指南
   - Django项目结构
   - API接口说明
   - 数据库模型
   - 开发环境配置

#### 前端开发
1. **frontend/README.md** - 前端开发指南
   - Vue项目结构
   - 组件说明
   - 路由配置
   - 状态管理

#### 全栈开发
1. **QUICK_START.md** - 快速搭建开发环境
2. **WINDOWS_SETUP_CN.md** - Windows环境配置

### 🚀 运维人员
1. **deployment/README.md** - 生产环境部署
   - Nginx配置
   - Gunicorn配置
   - Systemd服务配置
   - 自动化部署脚本

---

## 🔍 按主题查找文档

### 环境搭建
```
QUICK_START.md              # 基础环境搭建
WINDOWS_SETUP_CN.md         # Windows专用指南
backend/README.md           # 后端环境
frontend/README.md          # 前端环境
```

### 功能使用
```
docs/guides/USER_GUIDE.md   # 完整用户指南
├── 客户管理
├── 文件上传
├── 文件预览
└── 常见问题
```

### 技术实现
```
PROJECT_STRUCTURE.md        # 项目架构
backend/README.md           # 后端技术
frontend/README.md          # 前端技术
```

### 部署运维
```
deployment/README.md        # 部署指南
├── Nginx配置
├── Gunicorn配置
└── 系统服务配置
```

### 项目历史
```
CHANGELOG.md                      # 版本历史
docs/PROJECT_CHANGELOG.md         # 详细更新记录
docs/history/                     # 历史修复记录
```

---

## 📊 功能清单

### ✅ 已完成功能

#### 核心功能
- [x] 用户认证系统
- [x] 客户管理（CRUD）
- [x] 资料类型管理
- [x] 文件上传（图片/视频/PDF）
- [x] 文件预览
- [x] 资料完整性检查
- [x] 响应式设计

#### PC端功能
- [x] 拖拽上传
- [x] 批量上传
- [x] PDF在线预览
- [x] 图片预览（缩放/旋转）
- [x] 视频播放
- [x] 客户列表（搜索/筛选/分页）

#### 移动端功能
- [x] 拍照上传
- [x] 相册选择
- [x] 图片压缩
- [x] 文件预览
- [x] 卡片式列表
- [x] 上传后自动刷新

### 🎯 待开发功能
- [ ] 云存储集成（OSS/COS）
- [ ] OCR识别
- [ ] 工作流审批
- [ ] 消息通知
- [ ] 统计报表
- [ ] 数据导出
- [ ] Docker部署

---

## 🆘 获取帮助

### 常见问题

**Q: 如何开始使用系统？**
- 查看 **docs/guides/USER_GUIDE.md**

**Q: 如何搭建开发环境？**
- 查看 **QUICK_START.md** 或 **WINDOWS_SETUP_CN.md**

**Q: API接口文档在哪里？**
- 查看 **backend/README.md**

**Q: 如何部署到生产环境？**
- 查看 **deployment/README.md**

**Q: 项目更新记录在哪里？**
- 查看 **CHANGELOG.md** 和 **docs/PROJECT_CHANGELOG.md**

---

## 📝 文档贡献

### 文档更新原则
1. 保持文档与代码同步
2. 使用清晰的标题和结构
3. 添加必要的示例和截图
4. 及时更新变更记录

### 文档命名规范
- 核心文档：大写_下划线（如：README.md）
- 模块文档：模块名/README.md
- 指南文档：docs/guides/文档名.md
- 历史文档：docs/history/文档名.md

---

## 📅 最后更新

- **日期**: 2025-10-19
- **版本**: v1.0
- **维护者**: 系统管理员

---

## 🎉 感谢使用

感谢您使用客户资料收集系统！

如有任何问题或建议，欢迎反馈。

---

**💡 提示**: 建议先阅读主 README.md 了解项目概况，然后根据您的角色选择相应文档深入学习。

