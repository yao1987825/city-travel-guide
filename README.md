## 📖 项目简介

`city-travel-guide` 是一个专为 AI 旅行助手（WorkBuddy）设计的旅游知识库 Skill，涵盖中国中部和南部七座特色城市的景点、美食、避坑和小众秘境数据。

### 🎯 核心能力

- **景点推荐**：每城 15+ 景点，含实时票价、最佳游览季节、适合人群
- **美食指南**：当地特色美食 + 具体店铺推荐（含地址、人均消费、必点菜）
- **避坑手册**：城市专属坑点 + 真实破解方法
- **小众秘境**：59+ 个当地人才知道的隐藏宝地（小红书攻略实采）
- **消费分级**：低/中/高三档预算指南
- **智能规划**：支持行程生成、天气分析、高德导航、路线规划

---

## 🌍 覆盖城市

| 城市 | 景点数 | 特色标签 |
|------|--------|---------|
| 🏙️ **郴州** | 15+ | 丹霞高椅岭、东江湖雾漫、仰天湖草原、莽山温泉 |
| 🏔️ **清远** | 15+ | 古龙峡漂流、连州地下河、英德溶洞、阳山云海 |
| ⛰️ **衡阳** | 15+ | 南岳衡山、石鼓书院、雨母山艺术村落、岐山雾海 |
| 🏯 **长沙** | 16+ | 岳麓山、橘子洲、费大厨/茶颜悦色、裕湘纱厂 |
| 🎋 **益阳** | 15+ | 安化茶马古道、桃江竹海、罗文花海、云台山云海 |
| 🏛️ **韶关** | 15+ | 丹霞山、南华寺、南岭红沙漠、梅关古道 |
| 🌆 **深圳** | 16+ | 大梅沙/小梅沙、甘坑客家小镇、世界之窗、中英街 |

---

## 🔧 本地使用与命令示例

### 1) 查询城市数据

```bash
# 验证景点数量
python scripts/city_travel_search.py --count

# 按城市查询景点
python scripts/city_travel_search.py --city 郴州 --type attraction

# 按城市查询美食
python scripts/city_travel_search.py --city 深圳 --type food

# 按关键词查询（如搜索温泉、漂流、避坑等）
python scripts/city_travel_search.py --keyword 免费

# 查询推荐景点/隐藏秘境
python scripts/city_travel_search.py --type recommend
```

### 2) 生成旅游规划

```bash
# 交互式输入旅行偏好，生成 3 日/5 日等行程
python scripts/generate_plan.py --interactive

# 读取 profile.json 生成行程 JSON + SQL + FastAPI 骨架
python scripts/generate_plan.py --profile ./travel_profile.json --output ./travel_output

# 使用默认配置生成示例旅行计划
python scripts/generate_plan.py
```

### 3) 高德地图导航 / 天气查询

```bash
# 单段路线查询：起点/终点/交通方式
python scripts/amap_nav.py --from "长沙橘子洲" --to "岳麓山" --city 长沙 --mode transit

# 驾车路线查询
python scripts/amap_nav.py --from "深圳湾" --to "世界之窗" --city 深圳 --mode driving

# 步行路线查询
python scripts/amap_nav.py --from "外滩" --to "豫园" --city 上海 --mode walking

# 查询实时天气 + 未来 3 天预报
python scripts/amap_nav.py --weather 郴州

# 仅查询实时天气
python scripts/amap_nav.py --weather-live 长沙
```

### 4) 旅行路线规划（按城市天气智能推荐）

```bash
# 生成某城市的天气适配型路线建议
python scripts/itinerary_planner.py --city 郴州 --days 2 --budget 中档 --date 2026-04-15
```

### 5) 环境变量

```bash
# 复制示例文件并填入高德 Key
cp .env.example .env
```

`.env` 中至少配置：

```env
AMAP_KEY=your_amap_key_here
```

---

## 📡 数据来源（35+ 平台）

| 类别 | 来源 |
|------|------|
| **景点票价** | 官方景区网站、湖南省发改委、丹霞山官网、小红书实时 |
| **美食店铺** | 大众点评 2025 必吃榜、携程美食林、美团、小红书热门 |
| **隐藏秘境** | 小红书爆款攻略、搜狐旅游、车主指南、清远本地宝 |
| **避坑指南** | 花路网、大众点评、携程游记、真实游客反馈 |
| **旅行路线** | 携程、马蜂窝、本地宝官方攻略 |
| **价格数据** | 小红书 xhs-k-search 实时获取（2026-04-11） |
| **美食图片** | 小红书热门帖子封面（点赞数 100+） |
| **景点图片** | 高德地图 POI 实景图 + 小红书实拍 |

> 数据采集时间：2026 年 4 月 11 日 | 价格信息为市场参考价，实际以景区/餐厅为准

---

## ✨ 亮点功能

### 🤫 隐藏秘境（小众人少景美）

59+ 个当地人才知道的宝藏地，标注：
- 📍 **具体地址**（可直接导航）
- 🎫 **门票**（免费景点单独标注）
- 📸 **出片指数 / 适合季节**
- 💡 **推荐理由**

### 🏪 店铺推荐（小红书+大众点评实采）

- 具体店名、地址、人均消费（小红书实时价格）
- 必点菜推荐
- 按预算快速选店（<20元 / 20-60元 / 60-100元 / 100+元）
- 按场景选店（独旅早餐 / 带父母 / 情侣 / 深夜宵夜 / 文化体验）
- 🔥 小红书热门标注（点赞数/收藏数）

### ⚠️ 避坑手册

- 城市专属坑点表格
- 真实破解方法
- 通用实用 Tips（交通/季节/预约）

### 📸 小红书图片库

- 自动获取热门帖子封面图
- 美食/景点分类整理
- 点赞数 > 100 的高质量内容
- 每月自动更新（通过 xhs-k-search）

---

## 🔧 扩展与贡献

欢迎提交 Issue 或 Pull Request！

### 扩展城市

1. 在 `references/cities_data.md` 按模板添加新城市章节
2. 在 `references/recommended_shops.md` 添加推荐店铺
3. 在 `references/hidden_attractions.md` 添加小众秘境
4. 更新 `SKILL.md` 触发词列表和覆盖城市

### 数据规范

- 景点必须包含：名称、地址（大致范围即可）、门票、最佳季节、特色
- 美食必须包含：店名、地址、人均消费、必点菜
- 避坑条目必须包含：坑点、详细说明、破解方法

---

## 📄 License

MIT License — 欢迎自由使用、修改和分发

---

## 👤 作者

- **GitHub**: [yao1987825](https://github.com/yao1987825)
- **Skill 平台**: [WorkBuddy](https://www.codebuddy.cn)

---

> 💡 **提示**：数据会持续更新，关注本仓库获取最新版本！



---

## 📌 统一命令速查（新增）

```bash
# 城市查询
python scripts/city_travel_search.py --city 郴州 --type attraction
python scripts/city_travel_search.py --city 深圳 --type food
python scripts/city_travel_search.py --keyword 温泉

# 行程生成
python scripts/generate_plan.py --interactive
python scripts/generate_plan.py --profile ./travel_profile.json --output ./travel_output

# 高德导航 / 天气
python scripts/amap_nav.py --from "长沙橘子洲" --to "岳麓山" --city 长沙 --mode transit
python scripts/amap_nav.py --weather 郴州
python scripts/amap_nav.py --weather-live 深圳

# 天气适配行程推荐
python scripts/itinerary_planner.py --city 郴州 --days 2 --budget 中档
```

以上命令已统一覆盖城市攻略、旅行规划、导航与天气查询四类能力，便于本地开发和调试。
