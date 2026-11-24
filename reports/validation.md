# 直播源测试报告

测试完成：2026-11-24T22:11:12+08:00（北京时间）。

## 播放列表分组

原有 106 条播放项全部保留；12 条原有 4K 标注源独立分组。本次新增 11 条通过测试的源，最终 117 条播放项、14 个非空分组。

| 分组 | 播放项 |
| --- | ---: |
| 4K超高清 | 12 |
| 央视频道 | 17 |
| 卫视频道 | 35 |
| 上海本地 | 3 |
| 体育竞技 | 5 |
| 影视剧场 | 8 |
| 少儿动漫 | 5 |
| 财经理财 | 4 |
| 纪实科教 | 3 |
| 生活休闲 | 7 |
| 教育课堂 | 6 |
| 地方频道 | 2 |
| 国际频道 | 4 |
| 广播电台 | 6 |

## EMOS 源可用性检查

读取 75 个频道、89 条源记录，去除 1 条重复 URL 后为 88 条记录。通过 11 条、失败 42 条、平台内部代号 32 条、点播影片 2 条、非直播订阅 1 条。

测试方法：下载原 URL 的 HLS 播放列表和真实分片（主列表选择最高带宽线路），识别音视频轨道，并解码至少 2 秒；视频要求至少成功解码 25 帧。新增视频另检查了样本画面。合并保留原始 URL，未将临时分片链接写入 M3U。

| 频道 | 类型 / 实测分辨率 | 解码秒数 | 视频帧数 | 新增地址 |
| --- | --- | ---: | ---: | --- |
| RTHK第一台 | 广播音频 | 3.0 | 0 | https://rthkradio1-live.akamaized.net/hls/live/2035313/radio1/master.m3u8 |
| RTHK第二台 | 广播音频 | 3.0 | 0 | https://rthkradio2-live.akamaized.net/hls/live/2040078/radio2/master.m3u8 |
| RTHK第三台 | 广播音频 | 3.0 | 0 | https://rthkradio3-live.akamaized.net/hls/live/2040079/radio3/master.m3u8 |
| RTHK第四台 | 广播音频 | 3.0 | 0 | https://rthkradio4-live.akamaized.net/hls/live/2040080/radio4/master.m3u8 |
| RTHK第五台 | 广播音频 | 3.0 | 0 | https://rthkradio5-live.akamaized.net/hls/live/2040081/radio5/master.m3u8 |
| RTHK普通话台 | 广播音频 | 3.0 | 0 | https://rthkradiopth-live.akamaized.net/hls/live/2040082/radiopth/master.m3u8 |
| 广东珠江 | 1920×1080 | 3.006 | 75 | http://r.jdshipin.com/sE5vO |
| 广东珠江 | 1920×1080 | 3.0 | 73 | http://218.13.170.98:9901/tsfile/live/1000_1.m3u8?key=txiptv&playlive=1&authid=0 |
| CGNTVJapan | 1920×1080 | 3.003 | 90 | https://d2p4mrcwl6ly4.cloudfront.net/out/v1/8d50f69fdbbf411a8d302743e4263716/CGNWebLiveJP.m3u8 |
| BreadTV | 1920×1080 | 3.0 | 86 | https://video.bread-tv.com:8091/hls-live24/online/index.m3u8 |
| CGTN | 1920×1080 | 3.007 | 90 | https://amg00405-rakutentv-cgtn-rakuten-i9tar.amagi.tv/master.m3u8 |

## 未加入的源

- 32 条“官方源”是 `cctv1`、`bjws` 等内部代号，不是独立播放 URL。
- 42 条测试失败：包括 IP 白名单拒绝、超时、连接失败或无有效媒体。逐条原因见 `validation.json`；没有根据网页上的“正常”标签判定通过。
- 其中 CCTV16 4K、湖南卫视 4K 未通过；本次没有新增 4K。
- 两条点播影片不属于直播；“杂七杂八”的订阅下载后是升级、教程和打赏 MP4。

## 原有源与文件完整性检查

- 原有局域网 CCTV-1 抽样下载约 6.7 MB，ffprobe 识别为 H.264 1920×1080、MP2 音频；未逐条测试原有 106 条源。
- 原有所有 URL、频道名称、台标、EPG 属性和头部信息保持完整；仅调整分组、顺序和空行。
- 新增 URL 集合与测试通过 URL 集合完全相同；所有 4K 名称条目均在“4K超高清”。
- 重复合并不会新增重复 URL，也不会改变播放列表内容；`git diff --check` 通过。

播放列表 SHA-256：`1e89d0473450934121b2338ee44b73edb331a8bfb2e3e4b9cdfce2b63e751f54`

以上是 2026-11-24 当前网络下的短样本测试结果，不代表持续可用或所有网络均可访问。
