# SBS 本台播放复测

## 2026-11-27 软路由实测

更新 `subscribepro` 并重载 Nikki 后，新加载的 7 条韩国分流规则全部生效。韩国组固定选用 `kr_jp_cdt->oracle`，操作前后 36 个策略组的类型、成员与固定选择一致。

| SBS 请求 | 命中规则 | 实际链路 | 观察到的连接 |
| --- | --- | --- | ---: |
| 入口 `www.hwado.net` | 精确域名 | `🇰🇷 韩国节点` → `kr_jp_cdt->oracle` | 1 |
| 媒体 `tvlive.sbs.co.kr` | 精确域名 | `🇰🇷 韩国节点` → `kr_jp_cdt->oracle` | 158 |

通过软路由连续取流 240.001 秒。SBS 本台视频为 1280×720 H.264，音频为 AAC。以相邻解码时间戳间隔超过 250 毫秒为跳段判定，视频和音频均为 0 次。最长间隔分别为 34 毫秒和 21 毫秒。全段解码通过，取流日志无分片跳过或 HTTP 错误。[Clash 运行验证](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md#sbs-本台)

## 2026-11-26 固定入口与线路对照

`韩国频道` 新增 SBS 本台 720p。固定入口为 `http://www.hwado.net/webtv/catv/5002_688FE102.php`，重新打开入口会取得当次的播放地址。四个时点的画面均可辨认 SBS 台标和《뉴스헌터스》，与测试时段的 SBS 本台节目表一致。[SBS 当日节目表](https://www.sbs.co.kr/m/live/app/schedule)

| 接入方式 | 样本 | 视频跳段 | 音频跳段 | 最长视频间隔 |
| --- | ---: | ---: | ---: | ---: |
| 直接接入韩国出口 | 214.19 秒 | 23 | 22 | 8.04 秒 |
| 经香港节点接入同一韩国出口 | 215.02 秒 | 0 | 0 | 0.034 秒 |
| 经香港节点重新打开固定入口 | 125.02 秒 | 0 | 0 | 0.034 秒 |

两种路径均由 Cloudflare 和 IPPure 识别为韩国出口。样本按相邻解码时间戳间隔超 250 毫秒统计跳段。第二、第三个样本均通过 H.264 视频与 AAC 音频完整解码。同步抽查每条路径的 66 个分片，经香港节点的下载耗时中位数约 0.98 秒，直接接入约 5.81 秒。当时家庭网关的韩国组只有一条实际节点，另四条订阅备用节点均未建立可验证的韩国出口。

另外试了 18 个地址，含地方联播对照。新发现的 `xyktmobile00.s.gy` 固定入口返回站点停用页面；其他候选返回空跳转、证书错误或无法取得媒体。SBS 官网提供登录后的完整直播。[公开候选提交](https://github.com/iptv-org/iptv/issues/52825) · [SBS 直播说明](https://play.sbs.co.kr/m/notice.html)

`KrMandatory.list` 已登记固定入口 `www.hwado.net` 和实际媒体主机 `tvlive.sbs.co.kr`。[Clash 分流与软路由配置说明](https://github.com/baixiaoshengofficial/rules/blob/main/reports/iptv-validation.md)
