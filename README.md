# 上海电信 IPTV

日常使用文件：[`shtelconiptv.m3u`](shtelconiptv.m3u)。

## 分组和补源（2026-11-24）

- 原有 106 条播放项全部保留，局域网地址、频道名称、台标和 EPG 信息不变。
- 12 条名称标注为 4K 的原有源集中到首个分组“4K超高清”；这 12 条按原有标注分类，未逐条实测分辨率。
- 其余按央视、卫视、上海本地、体育、影视、少儿、财经、纪实科教、生活、教育等分类。
- 从 [EMOS 直播列表](https://emos.club/live?library=0&channel=0) 读取 75 个频道、89 条源记录，URL 去重后得到 88 条记录。
- 仅加入实测通过的 11 条源：5 条视频源、6 条广播源。现在共 117 条播放项，14 个非空分组。
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

## 原始说明

原 m3u 文件通过 [epg.112114.xyz](https://epg.112114.xyz/) 工具生成。
