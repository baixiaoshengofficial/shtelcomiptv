# 上海电信 IPTV

日常使用文件：[`shtelconiptv.m3u`](shtelconiptv.m3u)。

## 澳门、台湾和日本地面台补源（2026-11-28）

主播放列表现有 **266 条播放项**，含 146 条公网线路。台湾新增新唐人亚太台、唯心电视台，日本新增 TBS 系山形地面台 TUY。[本轮播放验证](reports/macau-taiwan-japan.md)

## 港澳台日韩美直播补源（2026-11-28）

该轮主播放列表为 **263 条播放项**，含 143 条公网线路。新增 14 路，包括 TVB 星河台、韓流チャンネル、联合新闻电视台、ABC News Live 和 Reuters 60。入选线路均通过两轮解码和连续取流。[本轮播放验证](reports/regional-live-expansion.md)

## 韩国地方台与美国新闻气象频道（2026-11-27）

该轮主播放列表为 **249 条播放项**，含 129 条公网线路。新增 17 个频道，包括 YTN、MBC 地方台、SBS 地方联播台、CBS News 24/7 和 WeatherNation。[本轮播放验证](reports/regional-local-expansion.md)

## 韩国 SBS 本台（2026-11-27）

该轮主播放列表为 **232 条播放项**，含 112 条公网线路。SBS 本台 720p 的入口和媒体均由软路由转至韩国组的 `kr_jp_cdt->oracle`，4 分钟取流音视频均未发现跳段。[SBS 播放复测](reports/sbs-route-retest.md)

## 韩国 MBC 本台补源与 SBS 复测（2026-11-26）

该轮主播放列表扩充到 **231 条播放项**，含 111 条公网线路。MBC 本台新增 720p 线路，入口和媒体主机走 Clash 韩国组。该轮的 SBS 本台候选在韩国节点出现跳段。[本台实测报告](reports/seoul-main-tv.md)

## 港台韩国主流台播出时段复测（2026-11-26）

该轮主播放列表扩充到 **230 条播放项**，含 110 条公网线路。新增无线新闻台、凤凰卫视香港台、台视／中视／华视／民视／公视主频，以及 KBS 1TV、KBS 2TV。新增线路均在对应节点实测，台湾使用 `twl`。[主流台实测报告](reports/mainstream-daytime.md)

## 港台韩国主流台复查（2026-11-26）

该轮主播放列表扩充到 **221 条播放项**，其中 101 条为公网线路。新增 TVB 明珠台、ViuTVsix 和 SBS 江原 G1 地方联播台。香港两路均以 1080p 播放，G1 实测为 720p。[主流台验证报告](reports/mainstream-followup.md)

Clash 的 `📺 IPTV中转` 已撤销。BreadTV 和 CGTN Rakuten 走香港，Love Nature 4K 走美国。更新 Nikki/OpenClash 订阅并重载配置后生效。

## 亚洲与美国节目补充（2026-11-26）

该轮主播放列表扩充到 **218 条播放项**，其中 98 条为公网线路。新增日本 13 条、美国 10 条和澳门 1 条。包括 Animax FREE、Lemino TV、日本时代剧 TV、PBS Nature、FOX Weather、LiveNOW from FOX 和澳视葡文。新增线路均通过至少两轮媒体解码，并核对了节目画面。

日本和美国的媒体域名已同步到 Clash 对应地区组，澳视葡文复用香港组。更新 Clash 订阅并重载后，再刷新播放器的主播放列表。[补源与验证报告](reports/variety-expansion.md)

## 台湾线路复测（2026-11-26）

该轮主播放列表扩充到 **194 条播放项**。民视新闻台 1080p 与原住民族电视台 720p 均在软路由两条 `twl` 线路上通过取流、解码及画面核对。五个重点主频仍待可播放的固定地址。

Clash 台湾组覆盖两路实际媒体主机。民视新闻台复用已有中转 IP 规则，原住民族电视台新增一条精确域名分流规则。[台湾播放测试](reports/twl-playback.md)

## 优先主流台补源（2026-11-25）

该轮主播放列表扩充到 **192 条播放项**。香港 HOY 76、77、78 和韩国 SBS JTV 全州联播台通过对应地区出口的取流、解码及节目画面核对。HOY 三台使用官网 HLS 地址，JTV 为全州地方台。

新增线路已在 Clash 规则中绑定对应地区，更新订阅并重载后生效。香港其他重点台、日本五大商业电视台和台湾主台的测试进展见 [主流台专项报告](reports/mainstream-priority.md)。

## 公开直播扩充（2026-11-25）

该轮主播放列表扩充到 **188 条播放项**，含 68 条公网线路。此次搜索筛查 81 个候选地址，新增 26 个频道。两轮媒体解码及画面核对通过后才加入。具体频道和分流见 [补源验证报告](reports/web-expansion.md)。

## 港澳台日韩美补源（2026-11-25）

该轮主播放列表扩充到 **162 条播放项**，其中 42 条为公网线路。筛查 31 个候选地址后新增 13 路，涵盖澳门、台湾、日本、韩国和美国。入选线路均有两次成功媒体解码及人工画面核对。香港无新增通过项。详见 [地区补源报告](reports/country-expansion.md)。

[Clash 规则仓库](https://github.com/baixiaoshengofficial/rules) 将香港、台湾、日本的 IPTV 主机并入对应 Mandatory 列表，韩国和美国直接绑定各自节点组。澳广视使用香港出口。更新规则订阅并重载后应用这次分流。

## 地区分流与补充线路（2026-11-25 晚）

该轮主播放列表扩充到 **149 条播放项**。新增港台电视 32、33、34 三路 1080p 线路，两轮媒体解码及人工画面核对通过；33、34 分别转播 CCTV-1 和 CGTN Documentary，不计作三个全新节目内容。原有 146 条播放项及 24 条 4K 线路保持不变。

已在 [rules 仓库](https://github.com/baixiaoshengofficial/rules) 按香港、台湾、日本、韩国、美国、国际中转及国内直连整理公网 IPTV 分流，覆盖已观察到的入口、跳转和媒体主机。更新规则订阅并重载 Nikki/OpenClash 后生效，播放器主源订阅地址不变。组播仍使用原家庭代理。

原有 26 条公网线路本轮也已下载媒体并解码：25 条首轮通过，香港电台第二台一次 TLS 超时后独立复测通过。新增候选 35 台后续媒体清单返回 404、大爱源返回 403，未加入。地区 HTTP 探测与媒体测试分开记录，不将入口 HTTP 200 视为整路直播可用；详情见 [`reports/regional-validation.md`](reports/regional-validation.md)。

## 港台日韩补全（2026-11-25）

该轮主播放列表扩充到 **146 条播放项、19 个非空分组**。新增 9 路：凤凰卫视中文台、凤凰卫视资讯台、TVB翡翠台、TVB Plus、港台电视31、TVBS欢乐节目线路、NHK WORLD-JAPAN、Arirang TV、KBS WORLD，分别放入港澳、台湾、日本、韩国分组。

这 9 路均经过两轮真实媒体下载、ffprobe 识别和 ffmpeg 解码，并人工检查复测画面。最近一轮开始于北京时间 2026-11-25 21:20，8 路为 1920×1080，NHK WORLD-JAPAN 为 1280×720；NHK 的分离音轨另行下载、解码验证。来源分别标记为“官方CDN”和“公网中转”，这些新增地址均为公网单播。

TVBS 按画面台标标注为欢乐节目线路；NHK WORLD-JAPAN 是英语国际频道。未通过测试或未确认直播时效的候选不加入。原有 137 条播放项、EPG 信息及 24 条 4K 线路保持不变。本轮复测范围是这 9 条新增线路，不代表重新测过全部 146 条，也不代表长期稳定。详情见 [`reports/asia-validation.md`](reports/asia-validation.md)。

## 其他组播频道补全（2026-11-25）

该轮主播放列表扩充到 **137 条播放项**。本轮增加8条家庭组播地址：

- 6条新频道/节目线路：BesTV电影导视、央广购物、东方购物1、东方购物2、好享购物、环球购物（聚鲨环球精选）。购物台放入单独的“购物频道”组。
- 2条已有频道的1080p版本：CCTV-16、多彩文体，单独统计，不计作新台。
- “欢笑剧场4K”按实际台标与SMG官方更名公告更新显示为“多彩文体4K（原欢笑剧场）”；原有EPG编号、EPG名称、台标和播放地址保留。

组播通过现有家庭代理取流，未修改路由器配置。入选地址经过两轮解码测试及画面核对；宣传动画、黑场、信号中断卡、未确认身份的节目流和仅HTTP 200却无视频数据的地址不加入。详情见 [`reports/multicast-validation.md`](reports/multicast-validation.md)。

## 4K 补全（2026-11-25）

该轮主播放列表扩充到 **129 条播放项**。首组“4K超高清”包含 **19 个不同频道、24 条线路**，本轮组播补全未改变4K组的线路数量。

- 新增 7 个原列表没有的 4K 频道：BesTV4K动画、BesTV4K电影、BesTV4K纪实、苏州4K、美丽河北4K、Love Nature 4K、Bloomberg TV+ 4K。
- 新增 5 条备用线路：CCTV-4K、CCTV-16 4K、欢笑剧场4K 的上海组播备用，以及湖南卫视4K、浙江卫视4K 的公网备用。备用不计入新增频道数，显示名带“备用”。
- 全部 12 条新增地址经过发现阶段测试和独立复测，实测均为 3840×2160，并成功解码视频。原有 12 条 4K 源也已实测通过。
- BesTV 三路使用家庭代理 `192.168.100.252:5678` 和新发现的组播频道地址；美丽河北为风光直播，不是河北卫视。仅修改播放列表，没有更改路由器配置。
- 标称 4K 但实测为 1080p / 1440p，或只有信号中断画面的候选源均未加入。原有 117 条条目及其地址、EPG、台标完整保留。

最新测试和来源见 [`reports/4k-validation.md`](reports/4k-validation.md)，入选源的实测参数见 [`reports/4k-selected.json`](reports/4k-selected.json)。所有测试均为当时家庭网络下的短样本测试，不代表长期稳定性。

## 分组和补源（2026-11-24）

- 原有 106 条播放项全部保留，局域网地址、频道名称、台标和 EPG 信息不变。
- 12 条名称标注为 4K 的原有源集中到首个分组“4K超高清”；这 12 条按原有标注分类，未逐条实测分辨率。
- 其余按央视、卫视、上海本地、体育、影视、少儿、财经、纪实科教、生活、教育等分类。
- 从 [EMOS 直播列表](https://emos.club/live?library=0&channel=0) 读取 75 个频道、89 条源记录，URL 去重后得到 88 条记录。
- 仅加入实测通过的 11 条源：5 条视频源、6 条广播源。该轮合并后为 117 条播放项，14 个非空分组。
- 新增视频源：广东珠江 2 条、CGNTVJapan、BreadTV、CGTN 各 1 条，样本实测均为 1920×1080。新增源名称带 `[EMOS]`，同频道不同 URL 保留为备用线路。
- 网站的 4K 候选源未通过测试，没有新增 4K 源。平台内部代号、测试失败地址、点播电影和升级宣传订阅均未加入。

新增源均已下载真实媒体分片，经 ffprobe 识别、ffmpeg 解码至少 2 秒；视频至少成功解码 25 帧，并检查了视频样本画面。测试是当时网络下的短样本验证，不代表长期稳定性。原有局域网源仅抽样验证了 CCTV-1，样本为 1080p；没有声称原有 106 条全部实测通过。

测试明细见 [`reports/validation.md`](reports/validation.md)，每条源的地址、实测参数和失败原因见 [`reports/validation.json`](reports/validation.json)。抓取快照见 [`reports/emos-sources.json`](reports/emos-sources.json)，不包含账号登录令牌。

## 在播放器中使用

导入本地的 `shtelconiptv.m3u` 即可。原有地址依赖能够访问 `192.168.100.252:5678` 的家庭网络。

在线订阅请使用本仓库 `main` 分支的 `shtelconiptv.m3u` 原始文件地址：

```text
https://raw.githubusercontent.com/baixiaoshengofficial/shtelcomiptv/main/shtelconiptv.m3u
```

## 重新测试和补源

需要 Python 3.10+、curl、ffprobe 和 ffmpeg，无第三方 Python 依赖。在项目目录执行：

```sh
python3 scripts/refresh_playlist.py
```

脚本读取已有抓取快照，重新测试候选源，按 URL 去重，只补入本轮通过且尚未存在的源；保留播放列表中的已有条目。它不会自动抓取登录后的新频道，不会删除后来失效的已有源。每轮结果写入 `reports/validation.json`；`validation.md` 是本次整理时的摘要。

只重新分组、使用已有测试结果时，可执行 `python3 scripts/refresh_playlist.py --reuse-report`。此选项不联网，不构成新的可用性验证。

4K 源检测可使用 `scripts/audit_streams.py`，输入为含 `channel`、`url` 的 JSON 数组，组播代理请使用单线程：

```sh
python3 scripts/audit_streams.py --input candidates.json --output report.json --workers 1 --sample-seconds 8
```

本次 4K 候选分别存放在四份发现/复测报告中；`python3 scripts/merge_4k.py` 只会合并两轮都通过、实测至少 3840×2160 的地址，按 URL 去重。它只读取测试报告，不会重新联网检测；报告必须已经完整生成。

其他组播频道用 `reports/multicast-reviewed.json` 记录人工核对的身份，配合 `multicast-discovery.json` 和 `multicast-recheck.json` 两轮报告，由 `python3 scripts/merge_multicast.py` 合并。该命令同样只读取已有报告，不重新联网检测。

港台日韩候选见 `reports/asia-candidates.json`。`python3 scripts/merge_asia.py` 仅合并 `asia-discovery.json` 和 `asia-recheck.json` 两轮都通过且有人工画面核对标记的源，按 URL 去重；此命令只读取报告，不会重新联网测试。

港台电视补充线路由 `python3 scripts/merge_regional.py` 读取 `regional-discovery.json` 与 `regional-recheck.json` 合并，只接受两轮通过且人工核对的源；该命令不联网重测。

## 原始说明

原 m3u 文件通过 [epg.112114.xyz](https://epg.112114.xyz/) 工具生成。
