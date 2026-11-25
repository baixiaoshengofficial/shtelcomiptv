# 地区分流及直播补源核验（2026-11-25）

## 原有公网源

原有 26 条公网源本轮全部取得可解码媒体：25 条首轮通过，RTHK 第二台出现一次 TLS 连接超时后单独复测通过。完整首轮、重试与观察到的请求主机见 [public-stream-audit.json](public-stream-audit.json)。本轮没有重测全部组播源。

## 新增线路

首轮报告完成：2026-11-25T21:41:51+08:00；独立复测报告完成：2026-11-25T21:42:34+08:00。三路均为 1920×1080，经真实 HLS 分片下载、ffprobe 识别、ffmpeg 解码至少 2 秒且不少于 25 帧，并检查两轮样本画面。

| 线路 | 结果 | 画面核对 |
| --- | --- | --- |
| 港台电视32 | 两轮通过并加入 | RTHK32 台标，正常节目 |
| 港台电视33 | 两轮通过并加入 | RTHK33 台标，转播 CCTV-1 |
| 港台电视34 | 两轮通过并加入 | RTHK34 台标，转播 CGTN Documentary |
| 港台电视35 | 未加入 | 入口健康探测成功，媒体清单返回 404 |
| 大爱1 | 未加入 | 入口健康探测成功，媒体 GET 返回 403 |

因此新增的是三条播放线路，不是三个全新节目内容。香港线路的控制接口连接记录在测试时显示 `DomainSuffix(akamaized.net)` → `🚀 节点选择` → `🐸 手动切换` → 香港命名节点；没有修改全局模式和现有策略选择。节点地区依据配置名称，未据此宣称已核验 IP 地理归属。

合并后 149 条播放项、19 个非空分组；逐条比对确认原有 146 条内容完整保留，24 条 4K 线路不变、无重复 URL、重复合并不改变播放列表。两轮原始结果见 [regional-discovery.json](regional-discovery.json)、[regional-recheck.json](regional-recheck.json)；入选参数和完整性检查见 [regional-selected.json](regional-selected.json)。

## 地区出口与规则

[rules 仓库](https://github.com/baixiaoshengofficial/rules) 新增七份 IPTV 分流列表，30 个精确域名和两个单一 IP 规则，覆盖当前 29 条公网线路已观察到的请求主机。凤凰中转入口与跳转主机、KBS 中转入口与分片主机、NHK 分离音视频主机均单独覆盖。组播继续使用原家庭代理。

控制接口按指定地区节点做 URL 健康探测，结果见 [regional-http-probes.json](regional-http-probes.json)。例如 NHK：日本节点约 60 ms、直连约 319 ms；Arirang：韩国节点约 61 ms、直连约 223 ms。它们是 HTTP 响应对照，未测视频持续吞吐，不能替代媒体解码；实际媒体测试仍走修改规则前的家庭分流。

新规则通过离线及真实 Subconverter/Mihomo 转换、路由验证，详见 [规则验证报告](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)。需要用户在 Nikki/OpenClash 更新订阅并重载后生效，未替换运行中的路由器配置。当前只是短样本可用性，不保证全天候稳定。
