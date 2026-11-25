# 亚洲与美国节目补充（2026-11-26）

本轮筛查 73 个不同播放地址，新增 24 条。主源由 194 条增至 218 条，含 98 条公网线路。新增项中 21 条为 1080p、2 条为 720p、1 条为 480p。

| 地区 | 测试地址 | 新增 | 实测出口 |
| --- | ---: | ---: | --- |
| 日本 | 22 | 13 | 两个日本出口 |
| 美国 | 24 | 10 | 经 IPPure 和 Cloudflare 核对的美国出口 |
| 澳门 | 3 | 1 | 两个香港出口 |
| 香港 | 2 | 0 | 香港 |
| 台湾 | 9 | 0 | 软路由台湾组的 `twl` 线路，本轮外部查询显示香港 |
| 韩国 | 13 | 0 | 韩国 |

## 新增节目

- 日本 13 条均为 1080p，涵盖日本时代剧 TV、Animax FREE、Lemino TV、日本露营与户外、Business Premium、GOLF LIFE、九州全览、PIA 落语、围棋将棋 Light、日本料理频道、东海 Locipo、手冢制作 TV 和观旅日本。这些是免费网络编排频道（FAST）。[Fast TV 官方节目表](https://fastv.jp/channel/)
- 美国新增 PBS KMOS 密苏里（720p）、FOX Weather、LiveNOW from FOX、Scripps News（720p）、Documentary+、PBS Nature、PBS Travel、PBS Antiques Roadshow、PBS Retro 和 Better Life Nature（480p）。[FOX Weather](https://www.foxweather.com/live) · [LiveNOW from FOX](https://www.livenowfox.com/where-to-watch) · [Scripps News](https://www.scrippsnews.com/live) · [PBS Nature](https://www.pbs.org/wnet/nature/faq/)
- 澳门新增澳视葡文（1080p）。两个香港出口均看到了节目画面。澳广视标注部分节目受版权地区限制，澳视澳门体育和澳门综艺本轮均只显示地区提示卡。[澳广视官网直播](https://www.tdm.com.mo/zh-hant/live)

## 播放与分流验证

每条新增线路至少两轮下载媒体并解码，单轮至少 2 秒和 25 帧。取样画面核对了节目内容，遇到间歇画面的线路另取样确认。结果对应本轮的短样本，未逐条复测原有播放项。[逐路验证记录](variety-expansion.json)

日本和美国分别新增 3 条和 10 条精确域名规则，澳视葡文复用 `live5.tdm.com.mo` 的香港规则。三条 Roku 线路的测试使用了支持标准 HLS AES-128 的播放器。家庭网关更新 Clash 订阅并重载后即可加载新规则。[Clash 线路与主机映射](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-routing.json)

凤凰卫视香港台本轮未确认有效画面。台湾候选遇到 HTTP 502 或样本不足，韩国候选则遇到网络或分片问题。日本 FNN Prime Online 可解码，但媒体入口和现有美国线路共用域名，当前域名规则无法分别指定出口。共同通信 News 在第二次测试返回 403。美国的 Bloomberg 线路未确认所列频道身份，Smithsonian 候选需要共用的跨区入口。这些地址均未收录。
