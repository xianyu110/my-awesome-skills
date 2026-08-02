# 支付宝当面付协议与排障参考

## 目录

- 请求签名
- 通知验签
- 密钥与运行时
- 响应和二维码
- 业务一致性
- 排障矩阵
- 官方资料

## 请求签名

按支付宝 OpenAPI 2.0 与官方 Node SDK 的行为生成 `alipay.trade.precreate` 请求：

1. 组装实际要发送的公共参数：`app_id`、`method`、`format`、`charset`、`sign_type`、`timestamp`、`version`、`notify_url`。
2. 将业务参数序列化为紧凑、稳定的 `biz_content` JSON；同一字符串必须同时参与签名和发送。
3. 排除 `sign`，不要排除 `sign_type`。按参数名升序排列，拼成 `key=value&key=value`。
4. 对未 URL 编码的 UTF-8 原文执行 RSA2，即 RSA PKCS#1 v1.5 + SHA-256，输出 Base64 签名。
5. 完成签名后才对 URL 或 form 字段编码。公共参数可放网关 URL，`biz_content` 放 POST body，与官方 Node SDK 的 OpenAPI 2.0 请求方式保持一致。

不要让请求签名和通知验签共用一个“删字段”函数。它们方向不同、兼容规则也不同。

可用虚构值检查字段集合，禁止把真实值写入测试快照：

```text
app_id=your-app-id&biz_content={"out_trade_no":"ORDER_TEST_001","subject":"测试套餐","total_amount":"0.01"}&charset=UTF-8&format=JSON&method=alipay.trade.precreate&notify_url=https://example.com/api/payment/notify/alipay&sign_type=RSA2&timestamp=2099-01-01 00:00:00&version=1.0
```

若支付宝错误信息给出“网关生成的验签字符串”，只在本地脱敏后按字段名比较：

- 是否遗漏 `sign_type`
- `biz_content` 是否与发送内容逐字节一致
- `notify_url`、大小写、空格和时间戳是否一致
- 是否在签名前 URL 编码
- 是否把 undefined、空字段或不同 JSON 键顺序带入一侧

## 通知验签

按以下顺序处理通知：

1. 解析表单一次并读取 `sign` 与 `sign_type`。
2. 复制通知字段并删除 `sign`。
3. 按字段名升序拼接原值，不要再次 `decodeURIComponent`。
4. 先保留 `sign_type` 验签；为兼容支付宝官方 Node SDK 的历史规则，失败后再删除 `sign_type` 重试。
5. 使用支付宝公钥验签，不是应用公钥。
6. 验签成功后再做业务字段检查。

不要记录通知原文。测试回调时使用运行时生成的临时密钥和完全虚构的数据。

## 密钥与运行时

明确每种密钥的用途：

| 材料 | 用途 | 存放位置 |
| --- | --- | --- |
| 应用私钥 | 商户请求加签 | 仅服务端 Secret |
| 应用公钥 | 由支付宝验证商户签名 | 上传支付宝开放平台 |
| 支付宝公钥 | 验证响应与通知 | 仅服务端配置 |

Cloudflare Workers 使用 Web Crypto 时：

- 私钥使用 PKCS#8 DER 导入，公钥使用 SPKI DER 导入。
- 算法使用 `RSASSA-PKCS1-v1_5`，哈希使用 `SHA-256`。
- 兼容 PEM 头尾、空白、真实换行和 Secret 中的字面量 `\n`。
- 若现有私钥为 PKCS#1，在可信本地环境转换为 PKCS#8 后重新写入 Secret；不要提交转换产物。
- 不要把 Node `crypto` 示例直接假定为 Worker 可用，先确认兼容标志和构建结果。

## 响应和二维码

- 判断 `alipay_trade_precreate_response.code` 是否为 `10000`。
- 从成功响应读取 `qr_code`。该值是二维码内容，不是图片 URL，也不是跳转页面 HTML。
- 用前端 QR 组件将该字符串渲染成二维码，并保留订单状态轮询。
- 不要导航到 `data:text/html`；浏览器通常禁止顶层页面跳转到 data URL，而且这不是当面付预创建的交付方式。
- 验证支付宝响应签名时优先使用官方 SDK；自实现必须基于原始响应中精确的响应节点字符串，不能对 JSON 重新序列化后验签。

## 业务一致性

通知或主动查询确认成功后，同时验证：

- `app_id` 等于当前服务端配置
- `out_trade_no` 对应本地订单且属于当前商户
- `total_amount` 与订单快照完全一致
- 商品、权益数量和有效期来自服务端订单快照
- 交易状态为可接受的成功终态

在单一事务或等效原子流程中更新订单并写权益流水。为权益流水建立唯一键，例如 `(order_no, grant_type)`。让“订单已支付但权益缺失”的修复也复用该函数。

## 排障矩阵

| 现象 | 优先假设 | 最小实验 |
| --- | --- | --- |
| 网关提示验签出错 | 请求漏签 `sign_type` 或签名原文与发送字段不同 | 用虚构值输出字段名列表和哈希，比较网关提示字段集合 |
| 同一密钥在别处可用 | 本实现的规范化或编码错误 | 用同一组虚构参数同时跑官方 SDK 与本地实现，仅比较规范字符串和验签布尔值 |
| 返回成功但没有二维码 | 读错响应层级或调用了 page pay | 仅记录 code、sub_code 及 `qr_code` 是否存在 |
| 二维码无法展示 | 把二维码内容当 URL/HTML 跳转 | 将 `qr_code` 原样交给 QR 组件渲染 |
| 通知验签失败 | 用错公钥、二次解码或 `sign_type` 规则不匹配 | 使用 `checkNotifySignV2` 行为对照，分别保留/排除 `sign_type` |
| 已支付但权益未到账 | 通知不可达或订单更新非幂等 | 主动查询对账，并检查唯一权益流水与修复路径 |
| 本地正常、Worker 失败 | PEM 格式、PKCS#1/PKCS#8 或 Node API 不兼容 | 在 Worker 测试环境只验证临时密钥的 sign/verify 闭环 |

## 官方资料

- 支付宝 OpenAPI 2.0 签名说明：<https://opendocs.alipay.com/common/02kf5q>
- 支付宝官方 Node SDK：<https://github.com/alipay/alipay-sdk-nodejs-all>
- 官方 SDK 请求加签实现：<https://github.com/alipay/alipay-sdk-nodejs-all/blob/master/src/util.ts>
- 官方 SDK 请求传输与通知验签实现：<https://github.com/alipay/alipay-sdk-nodejs-all/blob/master/src/alipay.ts>
