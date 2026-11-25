# 港澳台日韩美公开直播扩充（2026-11-25）

比较了各地电视台官网和公开直播目录，筛查 81 个不同地址。30 个地址首轮解码通过，29 个地址通过独立的第二轮解码，结合两轮画面检查及去重，共加入 26 个频道。主播放列表合并后共 188 项，其中 68 项为公网线路。原有 162 项的地址与 EPG 属性逐条核验。

| 地区 | 新增 | 频道 |
| --- | ---: | --- |
| 香港 | 2 | Pet Club TV、ViuTV |
| 澳门 | 1 | 澳门卫星频道 96 |
| 台湾 | 4 | CGNTV 中文台、GOOD 2、人间卫视、大立电视台 |
| 日本 | 4 | NHK 综合台、QVC 日本、Shop Channel 日本、樱桃电视台 |
| 韩国 | 10 | ABN 韩国、EBS English、EBS Plus 2、TBS 首尔、TV Chosun、TV Chosun 2、国乐放送 Gugak TV、韩国农业电视 NBS、韩国国防电视、韩国开放大学 OUN |
| 美国 | 5 | Court TV、Create TV（MPT）、FOX 35 奥兰多、KTVU FOX 2 旧金山、Newsmax2 |

每次测试下载直播分片，使用 ffprobe 确认识别到媒体轨道，使用 ffmpeg 解码至少 2 秒且视频样本不少于 25 帧。画面有黑屏、限制提示或频道身份存疑时暂缓添加。NHK 综合台使用公网中转，两轮通过后额外测试有一次解码失败。ViuTV 也使用公网中转。原目录标为 FOX Weather 的两条地址按实播画面和分发路径更名为 KTVU FOX 2 旧金山和 FOX 35 奥兰多。Newsmax2 只收录通过复测的较高画质地址。明珠台、无綫新闻台、HOY 76 和凤凰香港台本轮未通过。

发现参考包括 [各地区公开清单](https://github.com/iptv-org/iptv/tree/master/streams)、[ViuTV](https://viu.tv/)、[澳广视直播](https://www.tdm.com.mo/zh-hant/live)、[韩国国乐放送](https://www.igbf.kr/gugak_web/Player/LivePlayer.jsp)、[KTVU FOX 2](https://www.ktvu.com/live) 和 [FOX 35 Orlando](https://www.fox35orlando.com/live)。非官方中转只依据实际节目样本识别。

新增入口和实际观察到的媒体主机已按地区并入 [Clash 规则仓库](https://github.com/baixiaoshengofficial/rules)。澳门继续使用香港出口。直播媒体样本走测试时家庭网络的现有策略，新分流需要更新路由器订阅并重载。[逐条测试报告](web-expansion.json)
