---
name: city-travel-guide
description: >
  七城旅游攻略 + 智能旅游规划 Skill，覆盖郴州、清远、衡阳、长沙、益阳、韶关、深圳、上海。
  支持城市深度攻略（景点/美食/避坑/小众秘境/消费档次）、个性化行程规划、
  天气查询、导航路线、预算方案、城市对比与旅行建议。
  当用户询问以下类型问题时触发：某城市有哪些好玩的地方、当地特色美食、
  旅游避坑注意事项、推荐景点/餐厅、按预算的旅游安排、几日游怎么规划、
  天气和路线建议、城市对比等。
read-when: >
  旅游攻略、旅游计划、出行规划、行程安排、景点推荐、必去景点、
  省钱旅游、自由行攻略、几日游、怎么安排、哪些值得去、哪些可以跳过、
  景点之间怎么走、交通方式、公交/驾车路线、高德地图导航、
  查询天气、出发前看天气、穿衣建议、紫外线指数、城市对比、
  哪个城市更适合旅游、旅行预算、路线规划
metadata: >
  {"openclaw":{"os":["linux","darwin","win32"],"requires":{"env":["AMAP_KEY"]},"note":"支持静态攻略与 AI 直接调用天气/导航 API，适合 WorkBuddy / Dify 等 Skill 场景"}}
---

# city-travel-guide — 七城旅游全攻略 + 智能旅行规划

## 覆盖城市

郴州 · 清远 · 衡阳 · 长沙 · 益阳 · 韶关 · 深圳 · 上海

---

## 触发词列表

### 城市游玩类
- "XX 有什么好玩的" / "XX 旅游攻略" / "去 XX 玩什么"
- "XX 必去景点" / "XX 值得去的地方" / "XX 旅游推荐"
- "XX 几日游怎么安排"

### 美食类
- "XX 有什么好吃的" / "XX 特色美食" / "XX 当地必吃"
- "去 XX 吃什么" / "XX 美食攻略"

### 避坑类
- "去 XX 需要注意什么" / "XX 旅游踩坑" / "XX 旅游避坑"
- "XX 旅游有什么坑" / "XX 旅游骗局"

### 推荐类
- "XX 有什么隐藏景点" / "XX 小众景点" / "推荐 XX 去哪里"
- "XX 最值得去的" / "XX 宝藏景点"

### 消费类
- "去 XX 旅游要花多少钱" / "XX 旅游预算" / "XX 高性价比旅游"
- "XX 穷游攻略" / "XX 旅游消费档次"

### 天气/路线类
- "XX 天气怎么样" / "XX 这几天适合旅游吗"
- "XX 旅游路线推荐" / "XX 几天行程怎么安排"
- "XX 现在漂流适合吗" / "去 XX 要带什么"

### 规划/对比类
- "我想去 XX 玩 3 天，预算多少，怎么安排"
- "长沙和深圳哪个更适合旅游"
- "郴州和衡阳哪个好玩"
- "帮我做一份 XX 的旅行计划"

---

## 能力概览

本 Skill 同时支持两类能力：

### 1) 城市知识库能力
- 景点推荐（每城 15+）
- 特色美食与具体店铺
- 旅游避坑手册
- 小众秘境 / 隐藏景点
- 价格档次与预算参考
- 城市对比与选择建议

### 2) 智能规划能力
- 根据出发日期、预算、旅行天数、体力、风格生成行程
- 自动筛选景点，处理高价/远郊/时间冲突
- 输出可执行的每日安排与关键建议
- 结合天气/导航/交通信息进行更实用的旅行建议

---

## 数据文件说明

本 Skill 参考数据分为多类文件，覆盖攻略与规划两部分：

| 文件 | 内容 | 作用 |
|------|------|------|
| `references/cities_data.md` | 七城景点/美食/路线/消费档次 | 旅游攻略核心资料 |
| `references/hidden_attractions.md` | 小众隐藏景点全收录 | 低调宝藏地推荐 |
| `references/recommended_shops.md` | 推荐店铺手册 | 美食店铺与必点菜 |
| `references/recommendations.md` | 最值得去的景点与城市精选 | 精选推荐 |
| `references/price_database.md` | 景点/美食/住宿价格数据库 | 预算与价格参考 |
| `references/pitfalls_and_tips.md` | 避坑手册 | 真实坑点与解决办法 |
| `references/cities_attractions.md` | 规划所需景点元数据 | 行程生成数据 |
| `references/food_guide.md` | 美食价格手册 | 预算与餐饮规划 |
| `references/money_saving.md` | 省钱攻略 | 预算控制 |
| `references/travel_schema.md` | 数据库结构示例 | 可选后台模型 |
| `references/travel_api.md` | API 接口说明 | 可选后端设计 |
| `references/amap_api.md` | 高德 API 文档 | 天气/导航接口说明 |

---

## 执行逻辑

### Step 1 — 识别意图与城市

分析用户问题，提取：
- 目标城市（单城 / 多城 / 全部）
- 查询类型：景点 / 美食 / 避坑 / 推荐 / 预算 / 天气 / 路线 / 综合攻略 / 规划行程
- 用户约束：预算、天数、出发日期、旅行风格、体力、是否带家人/情侣/朋友

### Step 2 — 选择数据源

- 用户问“景点/景区” → 读 `cities_data.md`
- 用户问“美食/吃什么” → 读 `cities_data.md` + `recommended_shops.md`
- 用户问“具体店铺/必吃店” → 优先读 `recommended_shops.md`
- 用户问“门票/价格/预算” → 必须读 `price_database.md`
- 用户问“避坑/注意事项” → 读 `pitfalls_and_tips.md`
- 用户问“推荐/宝藏/隐藏” → 读 `recommendations.md` / `hidden_attractions.md`
- 用户问“天气/这几天适合旅游吗” → 调用天气查询 API
- 用户问“路线/几天怎么安排” → 调用导航/行程规划逻辑
- 用户要求“综合攻略”或“帮我做计划”→ 读取相关全部文件

### Step 3 — 构建回答结构

按用户需求输出以下任意组合：

```
## [城市名] 旅游攻略

### 🌤️ 天气预报（如用户问天气）
### 🗺️ 必去景点
### 🍜 特色美食
### ⚠️ 避坑提示
### 💡 推荐精选
### 🌿 隐藏秘境
### 💰 消费档次
### 📅 推荐行程（如用户问路线或想做计划）
```

### Step 4 — 价格数据必须标注来源

- 任何景点门票价格必须标注来源
- 任何美食价格必须标注来源
- 格式：`XX元/人 | [来源](链接) | 2026-04`
- 每次回答结尾提醒：`💡 以上价格仅供参考，请以实际为准`

---

## 旅行规划能力

### 输入字段（必填或推荐）

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `dest_city` | 目的地城市 | — |
| `travel_days` | 出行天数 | — |
| `depart_date` | 出发日期 | 今天 |
| `budget_cny` | 总预算（元） | — |
| `travel_style` | 旅行风格（可多选） | 文化、美食 |
| `group_type` | 出行类型：solo/couple/family/friends | solo |
| `mobility` | 体力：high/mid/low | mid |

### 可选字段
- `budget_level`：budget / mid / luxury
- `prefer_free`：是否优先免费景点
- `avoid_crowded`：是否避开拥挤景点
- `include_disney`：是否纳入迪士尼等全天景点
- `origin_city`：出发城市
- `need_navi`：是否需要导航
- `need_weather`：是否需要天气

### 行程生成思路

1. 先筛选目的地城市和用户偏好
2. 按预算和体力选择景点
3. 排除不适合的高价/远郊项目
4. 将景点按天分组并安排顺序
5. 结合天气和交通做修正
6. 输出：每日路线 + 建议时长 + 预算分配 + 注意事项

---

## 天气查询功能（高德天气 API）

### 触发时机
- 用户问"XX 天气怎么样" / "XX 这几天适合旅游吗"
- 用户规划行程时需要考虑天气
- 用户问“漂流/日出/登山”等天气敏感活动

### 执行步骤

1. 调用天气查询 API
2. 获取实时天气 + 未来3天预报 + 生活指数
3. 结合用户活动类型给出建议

### 示例

```
GET https://restapi.amap.com/v3/weather/weatherInfo
  ?key={AMAP_KEY}
  &city=郴州
  &extensions=all
  &output=JSON
```

返回字段重点：
- `lives[0].weather`
- `lives[0].temperature`
- `lives[0].humidity`
- `forecasts[0].casts[]`
- `forecasts[0].index[]`

---

## 导航路线功能（高德地图 API）

### 触发时机
- 用户问“从 A 到 B 怎么走更方便”
- 用户需要景点间交通建议
- 用户想知道路线耗时和出行方式

### 执行步骤

1. 先地理编码（地名 → 经纬度）
2. 再调用路线规划 API
3. 返回驾车 / 公交 / 步行建议，并说明距离、耗时和费用

### 示例

```
GET https://restapi.amap.com/v3/geocode/geo
  ?key={AMAP_KEY}
  &address=长沙橘子洲
  &city=长沙
```

---

## 输出质量要求

1. 景点数量：每城不少于 15 个，注明门票价格及最佳时间
2. 美食描述：包含特色、推荐店铺、价格参考（必须标注来源）
3. 避坑提示：使用表格形式，覆盖典型坑点与解决办法
4. 消费档次：必须给出三档明确金额区间
5. 天气路线：规划行程时必须含天气因素和时间安排
6. 实用性：信息必须对用户有明确帮助

---

## 适配说明

本 Skill 兼容以下使用场景：
- WorkBuddy Skill
- Dify 插件式知识库
- GitHub Raw 导入
- 本地脚本检索和开发扩展

---

## 快速检索命令参考

```bash
# 查询某城市美食
python scripts/city_travel_search.py --city 郴州 --type food

# 查询某城市景点
python scripts/city_travel_search.py --city 长沙 --type attraction

# 查询避坑信息
python scripts/city_travel_search.py --city 深圳 --type pitfall

# 验证景点数量
python scripts/city_travel_search.py --count

# 全部城市相关信息
python scripts/city_travel_search.py --type all
```

---

## API Key 配置汇总

| 功能 | 配置文件 | 申请地址 |
|------|---------|---------|
| 高德地图 | `scripts/amap_config.py` | https://console.amap.com/dev/key/app |
| 和风天气 | `scripts/weather_config.py` | https://dev.qweather.com/ |

> 免费额度：高德地图每日 5000 次；和风天气免费版每日 1000 次。

---

## License

MIT License

---

## 作者

- GitHub: [yao1987825](https://github.com/yao1987825)
- Skill 平台: [WorkBuddy](https://www.codebuddy.cn)
