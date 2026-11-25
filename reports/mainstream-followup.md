# 港台韩国主流台复查（2026-11-26）

本轮用对应节点测试 143 个不同固定地址。格式可识别、能解码、台标和节目画面正确的线路，复测通过后才加入。主播放列表由 218 条增至 221 条，含 101 条公网线路。

| 地区 | 测试地址 | 新增 |
| --- | ---: | --- |
| 香港 | 63 | TVB 明珠台、ViuTVsix，均为 1080p |
| 台湾 | 32 | 暂无 |
| 韩国 | 48 | SBS 江原 G1 地方联播台，720p |

## 播放验证

- **明珠台、ViuTVsix** 分别用两个香港出口取流并核对节目画面。两路均连续取样约 14 秒，并在 macOS 原生 AVPlayer 中收到视频帧。中转的媒体分片使用非标准后缀，默认 FFmpeg 和本次 VLC 取样模式未直接通过这两条线路。[TVB 节目表](https://programme.tvb.com/) · [ViuTVsix 节目表](https://viu.tv/epg/96)
- **SBS 江原 G1** 在韩国节点上多次解码，台标和《지금은 지방시대》与当晚当地节目表相符。该路是 SBS 地方联播，在标准 FFmpeg HLS 取样中通过。[G1 官网节目表](https://www.g1tv.co.kr/schedule/?mid=165_166)
- **无线新闻台** 一个候选播出前一天的新闻，另一路是娱乐新闻。官网提供带时效的播放地址。**凤凰卫视香港台** 有中转能解码，但画面日期显示 9 月 24 日，未收录。[香港持牌频道表](https://www.ofca.gov.hk/filemanager/ofca/sc/content_108/channel_list_chi.pdf) · [无线新闻台官网](https://news.tvb.com/tc/live/83)
- **台视、中视、华视、民视、公视主频** 均用 `twl` 测试。台视一条可解码的候选为台视新闻。两种外部查询对软路由台湾组的七条 `twl` 线路均返回 `HK`，测试仍按指定使用 `twl`。公视公布的网页直播入口可单独使用。[公视官方收看说明](https://info.pts.org.tw/%E5%B9%B4%E5%A0%B1%E5%8F%8A%E8%A8%8A%E6%81%AF%E5%B0%88%E5%8D%80/%E5%85%B6%E4%BB%96%E6%94%B6%E7%9C%8B%E6%96%B9%E5%BC%8F)
- **KBS 1TV / 2TV、MBC、SBS 本台** 暂未入选。部分地址仅在当时输出测试画面，其他地址无法取得媒体、要求临时签名或实际为地方联播。KBS 的官网播放页单独可选。[KBS ON AIR](https://onair.kbs.co.kr/)

## Clash 分流

新入选的两路香港频道复用已有精确域名规则，G1 新增一条单一 IP 规则走韩国。旧 `📺 IPTV中转` 策略组已移除，三路原有媒体均在目标出口解码通过，BreadTV、CGTN Rakuten 走香港，Love Nature 4K 走美国。CGTN Rakuten 在软路由明确指定直连时连接超时。测试后恢复了软路由原策略选择。[逐路验证数据](mainstream-followup.json) · [Clash 验证](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)
