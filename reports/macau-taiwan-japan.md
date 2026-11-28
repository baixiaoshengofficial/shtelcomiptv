# 澳门、台湾和日本地面台补源（2026-11-28）

本轮测试 155 个不同播放地址，澳门 13 个、台湾 52 个、日本 90 个。新增台湾 2 路、日本 1 路。主播放列表共 266 条播放项，含 146 条公网线路和 24 条 4K 播放项。

## 台湾

在隔离 Mihomo 实例中使用 `tw_cn2->twl` 和 `tw_cdt->twl`。在本机测试实例和软路由的同名节点上分别发出探针，逐个核对出口 IP 一致，并用同一 IP 地区数据库确认均位于台湾。播放测试从主列表采用的固定地址开始。

| 频道 | 实测分辨率 | 每条线路的连续取流 |
| --- | --- | ---: |
| 新唐人亚太台 | 854×480 | 45.01 秒 |
| 唯心电视台 | 854×480 | 45.06 秒 |

两路均核对了节目和台标，连续音视频全段解码通过，相邻解码时间戳的间隔均未超过 250 毫秒。TVBS 新闻、三立新闻、东森新闻、非凡新闻和年代新闻的候选未通过媒体取样。[新唐人亚太台直播](https://www.ntdtv.com.tw/live) · [中華電信 MOD 频道表](https://modp.cht.com.tw/download/channelprice.pdf?d=1)

## 日本

新增 **TUY テレビユー山形**，为 TBS 系的山形地面台。使用 `jp_iijv6` 和 `jp_cn2->iij` 播放 HEVC HLS，实测 1440×1080，两条线路均连续解码 34.08 秒，音视频时间戳未出现超过 250 毫秒的间隔。源的媒体分片使用 `.json` 后缀，FFmpeg 连播时显式指定 HLS 并允许该类分片，VLC 3.0.21 使用默认 HLS 识别也取到了音视频。[TUY 官网](https://www.tuy.co.jp/) · [TBS 的 TUY 新闻频道页](https://newsdig.tbs.co.jp/list/news/tuy)

NHK Eテレ、日视、朝日、TBS、东京电视台、富士和 TOKYO MX 的公开候选在取流时出现 403、连接错误或缺少可播放的媒体。山形 YTS 能取得部分样本，连续验证未通过。[日视的 TVer 播出说明](https://www.ntv.co.jp/ntvlive/) · [TBS 官方新闻直播](https://newsdig.tbs.co.jp/list/live)

## 澳门

现有节点中无澳门节点，筛查使用两条定位为香港的出口。澳广视澳门体育 93 和澳门综艺 95 的官网海外 CDN 返回版权提示画面，立法会入口当时只有待机画面。莲花卫视官网播放器使用短期签名，公开的固定候选未通过取流。澳亚卫视的备用地址也未通过验证，本轮澳门无新增。[澳广视直播](https://www.tdm.com.mo/zh-hant/live) · [澳门莲花卫视官网](https://www.lotustv.mo/)

## Clash 分流

两条台湾线路分别通过 `live.ntdtv.com` 和 `mobile.ccdntech.com` 取流，精确域名已同步至 `TwMandatory.list`。TUY 复用 `JpMandatory.list` 的 `tv-stream-test.daydreamer-json.cc` 规则。新规则在隔离 Mihomo 中验证，软路由更新订阅并重载后应用。[Clash 分流验证](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)
