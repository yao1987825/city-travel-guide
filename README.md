# 🗺️ city-travel-guide

> 七城旅游攻略 + 智能旅游规划 Skill，已整合城市深度攻略与自动行程规划两大能力
>
> 覆盖郴州 · 清远 · 衡阳 · 长沙 · 益阳 · 韶关 · 深圳 · 上海

[![GitHub Repo](https://img.shields.io/badge/GitHub-yao1987825%2Fcity--travel--guide-brightgreen?style=flat-square&logo=github)](https://github.com/yao1987825/city-travel-guide)

---

## 项目定位

本项目是两套旅游能力的合并版：

- 城市旅游知识库：景点、美食、避坑、店铺、小众秘境、消费档次
- 智能旅行规划：按天数/预算/风格/体力自动生成行程
- 实用工具：天气查询、导航路线、城市对比、目的地推荐

也就是说，项目不再只提供“攻略”，而是同时提供“知道去哪 + 怎么安排 + 什么时候去 + 怎么走”的完整旅行助手能力。

---

## 合并后的核心能力

- 🧭 个性化行程规划：根据预算、天数、出发日期、旅行风格生成每日安排
- 🗺️ 城市深度攻略：支持郴州、清远、衡阳、长沙、益阳、韶关、深圳，扩展上海和通用旅游信息
- 🍽️ 美食与店铺推荐：基于城市美食手册、店铺清单、价格参考
- 🌤️ 天气查询：支持目的地实时天气与未来几日天气建议
- 🚗 路线导航：可结合高德地图规划景点间路线
- 💡 避坑与隐藏秘境：覆盖真实坑点、网红景点、低调宝藏地
- 📊 预算分档：穷游 / 舒适 / 轻奢三档方案

---

## 覆盖城市

| 城市 | 特色 | 说明 |
|------|------|------|
| 郴州 | 丹霞/自然/温泉 | 适合周末与亲子出游 |
| 清远 | 溶洞/漂流/山水 | 适合自然风景优先 |
| 衡阳 | 名山/古城/人文 | 适合文化+山水混搭 |
| 长沙 | 城市夜游/美食/历史 | 普适度高，适合短途休闲 |
| 益阳 | 茶马古道/湖光山色 | 适合轻度放松型旅行 |
| 韶关 | 丹霞/古道/山地 | 适合全域旅行 |
| 深圳 | 海滨/城景/亲子 | 适合城市感体验 |
| 上海 | 城市观光/夜游/文化 | 适合短期城市规划 |

---

## 适用场景

### 1. 纯攻略查询

- “长沙有什么好玩的？”
- “郴州最值得去的 3 个地方是什么？”
- “深圳有什么小众景点？”

### 2. 行程规划

- “我 3 天去郴州，预算 2500，适合带家人，怎么安排？”
- “我打算去长沙 2 天，喜欢美食和拍照，给我一个详细路线”
- “上海 3 日游，预算 3000，适合情侣出行”

### 3. 旅行决策辅助

- “长沙和深圳哪个更适合旅游？”
- “清远和韶关哪一个更适合自然风景？”
- “今天适不适合去衡阳登山？”

---

## 目录结构

```text
city-travel-guide/
├── README.md
├── SKILL.md
├── references/
│   ├── cities_data.md
│   ├── hidden_attractions.md
│   ├── recommended_shops.md
│   ├── recommendations.md
│   ├── price_database.md
│   ├── pitfalls_and_tips.md
│   └── ...
├── scripts/
│   ├── city_travel_search.py
│   ├── weather_config.py
│   ├── xhs_main.py
│   └── ...
├── images/
└── ...
```

---

## 兼容说明

本仓库已经吸收了 `travel-planner` 的旅游规划能力：

- 规划逻辑保留
- 城市资料更丰富
- 提示词更完整
- 结构更适合 WorkBuddy / Dify 等 Skill 场景

如果已有旧项目依赖 `travel-planner`，建议统一切到本仓库作为主入口。

---

## 使用方式

### 方式一：WorkBuddy Skill 市场安装

在 WorkBuddy 中搜索 `city-travel-guide` 并安装。

### 方式二：直接导入 GitHub Raw

```text
https://raw.githubusercontent.com/yao1987825/city-travel-guide/main/SKILL.md
```

### 方式三：本地使用

```bash
python scripts/city_travel_search.py --count
python scripts/city_travel_search.py --city 郴州 --type attraction
python scripts/city_travel_search.py --city 长沙 --type food
```

---

## License

MIT License

---

## 作者

- GitHub: [yao1987825](https://github.com/yao1987825)
- Skill 平台: [WorkBuddy](https://www.codebuddy.cn)
