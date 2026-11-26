# 韩国 MBC 本台补源与 SBS 复测（2026-11-26）

测试了 30 个候选地址，用 IPPure 和 Cloudflare 核对韩国出口。MBC 本台通过并加入主源，SBS 本台候选等待稳定性复测。主播放列表增至 231 条，其中 111 条为公网线路。

| 频道 | 本台身份核对 | 播放结果 |
| --- | --- | --- |
| MBC 本台 | 台标及《오늘N》《연금복권 720+》与本台当时播出相符。同期江原地区台画面不同 | 720p，连续取流 255.12 秒并解码 7,652 帧，视频时间戳无断档。切换节目后再次通过 |
| SBS 本台 | 画面播出《생방송 투데이》和《뉴스헌터스》，并通过台标及 CJB 对照区分两台 | 韩国出口下 FFmpeg 长样本最长跳段约 8 秒，VLC 经同一韩国出口复测也有跳段 |

MBC 使用公开的固定中转入口，页面请求可重新取得当次媒体地址。MBC 独立短测有一次分片下载不完整，后续连续取样通过。SBS 的默认路由下可在 VLC 连续播放，但该次连接没有固定走韩国，因此仅作为对照记录。[MBC《오늘N》官网](https://m.imbc.com/program/1003106100000100000) · [MBC 节目表](https://schedule.imbc.com/) · [SBS 当日节目表](https://www.sbs.co.kr/m/live/app/schedule)

MBC 的入口复用 `KrMandatory.list` 里的 `koreatv.dothome.co.kr`，新增精确媒体域名 `live.imnews.imbc.com`。更新 Clash 订阅并重载后应用。[逐路数据](seoul-main-tv.json) · [Clash 路由验证](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)
