---
name: google-maps-automation
description: "通过 Rube MCP（Composio）自动化 Google Maps 任务：地址地理编码、搜索地点、获取路线、计算路线矩阵、反向地理编码、自动补全、获取地点详情。请始终先搜索工具以获取最新模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Maps 自动化

通过 Rube MCP（Composio）使用 Google Maps 对地址进行地理编码、搜索地点、获取路线、计算距离矩阵，以及检索地点详情。

**工具包文档**：[composio.dev/toolkits/google_maps](https://composio.dev/toolkits/google_maps)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 已通过 `RUBE_MANAGE_CONNECTIONS` 为工具包 `google_maps` 建立活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具模式

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `google_maps` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 对地址进行地理编码
使用 `GOOGLE_MAPS_GEOCODING_API` 将街道地址转换为地理坐标（经纬度）。
```
Tool: GOOGLE_MAPS_GEOCODING_API
Parameters:
  - address: 要进行地理编码的街道地址或 plus code
  - latlng: 用于反向地理编码的经纬度（例如 "40.714224,-73.961452"）
  - place_id: 用于地点地理编码的地点 ID
  - language: 结果使用的语言
  - region: 区域偏好（ccTLD 代码）
  - bounds: 用于视口偏好的边界框
  - components: 组件过滤器（例如 "postal_code:94043|country:US"）
```

### 2. 搜索地点
使用 `GOOGLE_MAPS_TEXT_SEARCH` 通过自由文本查询查找地点。
```
Tool: GOOGLE_MAPS_TEXT_SEARCH
Parameters:
  - textQuery（必填）: 搜索文本（例如 "restaurants in London"）
  - fieldMask: 要返回的字段（例如 "displayName,formattedAddress,rating"）
  - maxResultCount: 最大结果数（1-20，默认 10）
```

### 3. 获取两个位置之间的路线
使用 `GOOGLE_MAPS_GET_ROUTE` 计算路线，包括距离和用时。
```
Tool: GOOGLE_MAPS_GET_ROUTE
Parameters:
  - origin_address（必填）: 起点（地址或 "lat,lng"）
  - destination_address（必填）: 终点（地址或 "lat,lng"）
  - travelMode: DRIVE、BICYCLE、WALK、TWO_WHEELER 或 TRANSIT
  - routingPreference: TRAFFIC_UNAWARE、TRAFFIC_AWARE、TRAFFIC_AWARE_OPTIMAL
  - computeAlternativeRoutes: 是否返回备选路线（布尔值）
  - units: METRIC 或 IMPERIAL
  - languageCode: BCP-47 语言代码
  - routeModifiers_avoidTolls / avoidHighways / avoidFerries: 路线偏好
```

### 4. 计算距离矩阵
使用 `GOOGLE_MAPS_COMPUTE_ROUTE_MATRIX` 计算多个起点与终点之间的距离和用时。
```
Tool: GOOGLE_MAPS_COMPUTE_ROUTE_MATRIX
Parameters:
  - origins（必填）: 起点位置数组（地址字符串或经纬度对象）
  - destinations（必填）: 终点位置数组
  - travelMode: DRIVE、BICYCLE、WALK、TWO_WHEELER 或 TRANSIT
  - routingPreference: TRAFFIC_UNAWARE、TRAFFIC_AWARE、TRAFFIC_AWARE_OPTIMAL
  - fieldMask: 要包含的响应字段
  - units: METRIC 或 IMPERIAL
```

### 5. 获取地点详情
使用 `GOOGLE_MAPS_GET_PLACE_DETAILS` 检索特定地点的详细信息。
```
Tool: GOOGLE_MAPS_GET_PLACE_DETAILS
Description: 使用资源名称（places/{place_id} 格式）检索某地点的详细信息。
  返回营业时间、联系方式、评价等。
Note: 调用 RUBE_SEARCH_TOOLS 以获取此工具的完整模式。
```

### 6. 搜索附近地点
使用 `GOOGLE_MAPS_NEARBY_SEARCH` 查找某点周围圆形区域内的地点。
```
Tool: GOOGLE_MAPS_NEARBY_SEARCH
Parameters:
  - latitude（必填）: 中心纬度（-90 到 90）
  - longitude（必填）: 中心经度（-180 到 180）
  - radius（必填）: 搜索半径，单位为米（最大 50000）
  - includedTypes: 要包含的地点类型（例如 ["restaurant", "cafe"]）
  - excludedTypes: 要排除的地点类型
  - fieldMask: 要返回的字段
  - maxResultCount: 最大结果数（1-20）
```

## 常见模式

- **先地理编码再获取路线**：使用 `GOOGLE_MAPS_GEOCODING_API` 将地址转换为坐标，再用 `GOOGLE_MAPS_GET_ROUTE` 获取它们之间的路线。
- **先搜索再获取详情**：使用 `GOOGLE_MAPS_TEXT_SEARCH` 查找地点，再用 `GOOGLE_MAPS_GET_PLACE_DETAILS` 获取更丰富的元数据（营业时间、联系方式、评价）。
- **自动补全体验**：在用户输入地址或地点名称时，使用 `GOOGLE_MAPS_AUTOCOMPLETE` 提供输入联想建议。
- **反向地理编码**：使用 `GOOGLE_MAPS_GEOCODE_LOCATION` 将坐标转换回人类可读的地址。
- **批量距离计算**：对多对多的距离计算使用 `GOOGLE_MAPS_COMPUTE_ROUTE_MATRIX`，而不要反复调用 `GOOGLE_MAPS_GET_ROUTE`。
- **嵌入地图**：使用 `GOOGLE_MAPS_MAPS_EMBED_API` 为地点、路线或搜索结果生成可嵌入的地图 URL。

## 已知坑点

- **路线矩阵结果结构**：`GOOGLE_MAPS_COMPUTE_ROUTE_MATRIX` 返回的结果位于 `data.elements` 下，包含 `originIndex` 和 `destinationIndex` 以及 `distanceMeters` 和 `duration`——而不是 `routes[]` 结构。
- **时长格式**：`GOOGLE_MAPS_GET_ROUTE` 在 `data.response_data.routes` 中以字符串形式返回时长，如 `"937s"`。在进行数值比较前必须先解析这些字符串。
- **用于链式调用的地点 ID**：在调用 `GOOGLE_MAPS_GET_PLACE_DETAILS` 获取更丰富的字段时，使用从 `GOOGLE_MAPS_TEXT_SEARCH` 返回的地点标识符。
- **反向地理编码的输入**：`GOOGLE_MAPS_GEOCODE_LOCATION` 是以坐标驱动的。确保传入经纬度（而不是地址字符串），以避免查找不匹配。
- **路线偏好限制**：当 `travelMode` 为 WALK、BICYCLE 或 TRANSIT 时，不能设置 `routingPreference`——这些模式下必须省略该参数。
- **附近搜索的类型有效性**：`"food"` 不是 `GOOGLE_MAPS_NEARBY_SEARCH` 的有效类型（它属于 Table B）。请改用具体类型，如 `restaurant`、`cafe`、`bakery`、`fast_food_restaurant`。
- **嵌入 API 仅支持 API 密钥**：`GOOGLE_MAPS_MAPS_EMBED_API` 需要 API 密钥，不支持 OAuth2。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 地址地理编码 | `GOOGLE_MAPS_GEOCODING_API` | `address` 或 `latlng` 或 `place_id` |
| 反向地理编码 | `GOOGLE_MAPS_GEOCODE_LOCATION` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 文本搜索 | `GOOGLE_MAPS_TEXT_SEARCH` | `textQuery`、`fieldMask`、`maxResultCount` |
| 附近搜索 | `GOOGLE_MAPS_NEARBY_SEARCH` | `latitude`、`longitude`、`radius`、`includedTypes` |
| 获取路线 | `GOOGLE_MAPS_GET_ROUTE` | `origin_address`、`destination_address`、`travelMode` |
| 距离矩阵 | `GOOGLE_MAPS_COMPUTE_ROUTE_MATRIX` | `origins`、`destinations`、`travelMode` |
| 地点详情 | `GOOGLE_MAPS_GET_PLACE_DETAILS` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 自动补全 | `GOOGLE_MAPS_AUTOCOMPLETE` | `input`、`includedRegionCodes`、`locationBias` |
| 地点照片 | `GOOGLE_MAPS_PLACE_PHOTO` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 嵌入地图 | `GOOGLE_MAPS_MAPS_EMBED_API` | `mode`，以及模式相关的其他参数 |

---
*Powered by [Composio](https://composio.dev)*
