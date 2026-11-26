# 港台韩国主流台播出时段复测（2026-11-26）

本轮在北京时间 17:30 前后测试 102 个固定候选，香港 23 个、台湾 48 个、韩国 31 个。新增 9 条后，主播放列表共 230 项，其中 110 条为公网线路。

| 地区 | 新增频道 | 实测画质 | Clash 规则 |
| --- | --- | --- | --- |
| 香港 | TVB 无线新闻台、凤凰卫视香港台 | 均为 720p | `HkMandatory.list` |
| 台湾 | 台视、中视、华视、民视、公视主频 | 台视 720p，其余 1080p | `TwMandatory.list` |
| 韩国 | KBS 1TV、KBS 2TV | 均为 720p | `KrMandatory.list` |

每条新增线路至少通过两次取流及画面核对，并取得约 16 至 18 秒的连续音视频。无线新闻台画面显示当日日期，凤凰香港台画面显示当天的滚动新闻，均随测试时间推进。凤凰香港台为 HTTP-FLV，播放需支持该格式。未收录此前播出归档画面的香港中转。[无线新闻台官网](https://news.tvb.com/tc/live/83) · [凤凰香港台官网](https://share.fengshows.com/live.html?channelID=r03&id=15e02d92-1698-416c-af2f-3e9a872b4d78)

台湾五台均通过指定的 `twl` 线路复测。两种外部查询本轮仍将受测 `twl` 定位为香港。民视主频首个出口返回 502，换其他 `twl` 出口成功，多个时点取得节目画面；五台共用一个公网媒体 IP。[台湾 MOD 频道表](https://modweb2.chtmod.tv/download/channelprice.pdf)

KBS 两台使用可重复请求的中转入口，由入口取得当次的官方媒体地址。规则覆盖入口、媒体和 HLS 密钥主机。KBS 1TV 期间有一次超时，单独重试后又成功连续取样。MBC 的官网匿名入口返回预览流，找到可播的独立地址为地方联播。SBS 官方媒体入口需要时效参数，固定 CDN 地址返回 403，可解码的中转为 CJB 地方台。本轮未收录 MBC 与 SBS 本台候选。[KBS ON AIR](https://onair.kbs.co.kr/) · [MBC 官网直播](https://onair.imbc.com/) · [SBS 官网直播](https://www.sbs.co.kr/live)

三地规则新增 5 条精确域名与 2 条单一 IP。明示 IP 的媒体入口用 `/32` 规则。更新 Clash 订阅并重载后应用新分流。[逐路播放数据](mainstream-daytime.json) · [Clash 分流验证](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)
