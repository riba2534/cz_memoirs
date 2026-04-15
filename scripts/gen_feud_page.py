#!/usr/bin/env python3
"""Generate the Twitter feud markdown page from twitter-feud.json."""
import json
from pathlib import Path
from datetime import datetime

import os
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, 'scripts', 'feud-raw')
DATA = os.path.join(REPO_ROOT, 'site', 'public', 'data', 'twitter-feud.json')
OUT = os.path.join(REPO_ROOT, 'site', 'chapters', '27-twitter-feud.md')

# Chinese translations for English tweets, keyed by ID.
# For tweets that are already Chinese, key maps to empty string (no zh section).
TRANSLATIONS = {
    # 2022 FTX tweets
    '1589861637271715840':
        '如果 FTX 不幸变成下一个 LUNA，行业里没有任何人能从这场事故中获益，包括币安。用户和监管都会对整个行业失去信心。我希望 CZ 能考虑停止抛售 FTT，和 SBF 重新谈一笔。',
    '1589864353435910144':
        '去中心化是加密行业的基石。如果币安拿下 100% 市场份额、BNB 市值超过 BTC，这个行业就完了，CZ 也会失去一切。帮助 FTX 走出当前的流言，才是对 CZ 最好的选择。',

    # CZ 书发布相关
    '2039913572239868338':
        '《Freedom of Money》一书最新进度：计划下周正式发布。除非编辑把我拉回去再改一遍——那就还得等几天。🤣',
    '2039915098211561947':
        '忘了说，这本书的所有销售收入都会捐给慈善机构。我不是想靠这本书赚钱。🤣',
    '2041541368971993389':
        '和 @scottmelker 坐下来聊聊这本书，还有一些我从未公开谈过的事情。初稿大概是 6 个月前写完的——之后花了太多时间打磨。',
    '2041687406802284699':
        '《Freedom of Money》已经在部分国家上线。应该在 4 月 9 日那一天全球读者就都能买到了。',
    '2042047410340331894':
        '这本书的精装版和平装版现在都可以在 Amazon 上买到了！🙏',

    # Star Xu 4.8
    '2041763367292170477': '',  # already Chinese
    '2041766531122823215':
        '我本无意再提这些 CZ 年轻时的旧账。但既然因为那本书又被卷进来，那就重申一次事实。\n\n'
        '他在 OKCoin 任职期间，伪造合约的证据 12 年前就已经公开在网上。当时发布的 YouTube 视频至今仍在：\n\n'
        'https://t.co/UTEhtlHE7X\n\n'
        '视频时间轴：\n'
        '• 0:00 — 接入公证处网络\n'
        '• 1:00 — 登录财务会计的 QQ\n'
        '• 1:26 — 搜索前员工的联系人与聊天记录\n'
        '• 1:35 — 聊天记录与此前发送的所有附件出现在右侧。可以看到发给会计的 v7 与 v8 两版合约（v7 发送于 2014-12-16 15:17:24；v8 发送于 2015-12-16 19:29:47）\n'
        '• 1:55 — 打开 v8 合约审阅（即含 6 个月终止条款的版本）\n'
        '• 2:15 — 合同最后一行可见 6 个月终止条款\n'
        '• 2:22 — 打开 v7 合约审阅\n'
        '• 2:54 — 打开前员工的护照（已打码）\n'
        '• 3:02 — 前员工公开的 QQ 账号\n\n'
        '看到这些证据后，他当时的回应是：自己不常用 QQ，账号可能被我雇佣的另一位 OKCoin 员工登录过，然后伪造了这些聊天记录。\n\n'
        '你相信这种解释吗？\n\n'
        '他当时提供的完整解释如下：\n\n'
        'https://t.co/nRMiqz97It',
    '2041785361807114422':
        '在监狱里待了四个月之后，他仍然继续对世界说谎。我只能说：一个惯于撒谎的人，即使经历过牢狱之灾，也不会改变他的本性。',

    # Heyi 4.8
    '2041826090197320037': '',  # already Chinese

    # Star Xu 4.9 morning
    '2042055343598166499': '',  # already Chinese

    '2042130369294860397': '',  # already Chinese (CN version)
    '2042130511456563276':
        '我本无意再翻 CZ 的旧账，但他那本充满谎言的书无端把我卷了进来。\n\n'
        '他一直有一个长期习惯：对公众、对媒体、对全世界说误导性的话。遗憾的是，这种扭曲事实的倾向似乎始终没变。\n\n'
        '根据 CoinDesk 的报道，他的妻子曾向法官递交一封支持信。在那篇报道里，她始终将两人称为「丈夫」与「妻子」，而没有使用「前妻」或「前夫」这样的字眼。（我非常尊重她的忠诚与坚毅。）\n\n'
        '然而在他自己的书和媒体采访中，他对婚姻状态一直含糊其辞——时而说是分居，时而暗示已经离婚。那到底真实情况是什么？离婚是否发生在他出狱之后？\n\n'
        '如果他们确实已经离婚，他在币安的股份是否已按法律进行了合法分割？这不仅是法律问题，也是一个丈夫最基本的道德责任与诚信问题。Jeff Bezos 和 Bill Gates 离婚时都是依法与配偶完成资产分割的。',

    '2042195656048365782': '',  # already Chinese
    '2042197860599652512':
        'CZ 反复讲「卖房买比特币」的故事。但这故事背后的完整真相是什么？那栋房子的首付最初是谁出的？被卖掉的又究竟是谁的房子？\n\n'
        '当他把这个故事当成个人成就反复炫耀、把自己包装成先知的时候，他有没有想过他岳父岳母的感受——那两位当年支持女儿女婿、如今已经年迈的老人？\n\n'
        '其实有很多事我从未公开过，事实上我连重提都不愿意。借他人不幸、用私生活进行道德攻击，从来都不是我的原则。若不是那本充满谎言的书把我硬生生拖进来，我绝不会再提这些旧账。',

    '2042211764956508335': '',  # already Chinese
    '2042212044502618535': '',  # English version of CN above — no separate zh

    # CZ 4.9 main counter
    '2042278660149842029':
        '我通常不理会这些无中生有的攻击。但是……\n\n'
        '你现在就可以道歉了。我已经正式离婚。\n\n'
        '我不会在网上发布任何法律文件，因为我尊重前妻的隐私，也珍惜我们曾经在一起的时光。\n\n'
        '我很乐意赌 10 亿美金（或者你任选的任何数字）：我已经正式离婚（而且早就离了）。\n\n'
        '如果你愿意接这个对赌，我们可以请律师来验证我的离婚协议，非常简单。\n\n'
        '这个对赌邀约永久有效，什么时候你准备好都可以。但如果你 24 小时内不接，那就清楚地证明了到底是谁在对公众误导。\n\n'
        '我要去忙更有意义的事了。',

    # Star Xu 4.9 CN (after CZ)
    '2042278971879116989': '',  # already Chinese

    '2042281554135994831':
        'OKX 和币安都受多个监管机构监管。作为一家受监管公司的最终受益人（UBO），公开发起 10 亿美金的对赌，这显然不符合专业规范。我很好奇，币安的监管机构是否会接受这种行为。\n\n'
        '至于你是否在误导公众、对世界撒谎，其实有一个非常简单的检验方法：你在币安的股份是否已经依法与前妻完成分割？Bill Gates 和 Jeff Bezos 离婚时的做法，就是资产分割应有的样子。',

    # Heyi 4.9 replies
    '2042283789330550885': '',  # Chinese already

    # CZ 4.9 second punch
    '2042294828243832927':
        '正如我说的，「或者任何你挑的数字」，大小不限。\n\n'
        '拿出点男人的担当，道歉吧。别试图转移话题，也别试图转移责任。\n\n'
        '这事从头到尾只关乎一件事：你究竟有没有在公开场合对我说谎。',

    # CZ 17:49 read the book
    '2042298803366023192':
        '去读那本书吧，真的很好玩！🤣\n\n'
        '有声书版本正在做。有意思的是，AI 用我自己的声音读出来，我都分不出真假，唯一的破绽是——它不像我那样会卡壳。',

    # Heyi replies 18:21 / 18:25 / 19:05
    '2042306830072778952': '',
    '2042307898848534953': '',
    '2042317983356174593': '',

    # Heyi 19:34 prediction market bilingual - already bilingual
    '2042325362202333581': '',
    '2042330194342551711':
        '来看看，从概率上来看：\n「徐明星会向 CZ 道歉吗？」',
    '2042338415870443732': '',  # Chinese only

    # Star Xu 23:47 decline bet
    '2042389031955415448':
        '再说一遍：作为 OKX 的 CEO，基于我们公司的合规文化，我不适合参与这种公开「对赌」的游戏。但如果你真的有诚意，请让你的律师把经双方签字的离婚协议正式发送给我们的律师——只要文件是真的，我会立即公开道歉。\n\n'
        '至于你在书和媒体上对我和我公司的其他攻击，我也会通过合法合规的渠道逐一回应。',

    # Heyi 4.10
    '2042459400296685583': '',
    '2042463425360441575': '',
    '2042464003092283448': '',

    # OKX 九妹 4.10 反击
    '2042524484167700755': '',  # already Chinese, bilingual not needed
    '2042408507077771473': '',  # already Chinese
    '2042409000260812984': '',
    '2042409912878444751': '',
    '2042502471361441987': '',

    # 4.10 何一防御立场
    '2042470815661244453': '',  # 05:12 "我们没有主动诋毁过谁，一直被追着碰瓷"

    # 4.11 余波阶段 — CZ 继续书籍营销 + 九妹隔空暗讽
    '2042778101961134291':
        '真有意思，能从和我见过面的人的视角里学到这么多。很高兴他们后来都发展得不错。还看到了很多我自己都没见过的老照片。\n\n点燃一个一个的小火种。喜欢这种感觉！',
    '2042798246402101740': '',  # 02:53 Chinese
    '2043062801271324855':
        '来自 Forbes 的报道，有好有坏的评价都有。\n\n「《Freedom of Money: A Memoir of Protecting Users, Resilience, and the Founding of Binance》[...] 已在 Amazon Kindle 上架，售价 9.99 美元，目前已经是 Kindle 全站排行第 4 名。」\n\n上架才 3 天。🤣',
    '2042989574394466811': '',  # 九妹 15:34 CN 暗讽

    # 4.12 何一感慨 CZ 往事视频
    '2043403499573010534': '',  # 何一 4.12 18:58 "准备出发的 CZ，BNB 破发后开播的 CZ"

    # 4.12-4.13 币安叙事收尾期
    '2043324805894578681': '',  # CZ 4.12 13:46 「写出来就像我在夸币安一样」
    '2043498497744285729': '',  # 何一 4.13 01:16 澄清币安产品线
    '2043515208853795288':
        '哇，感谢这么多年的支持！\n\n我没有当时直播的视频，看了真的好惨的样子😂 感谢分享！',
    '2043516390653489599': '',  # CZ 4.13 02:27 Allan 都被建模了

    # 4.13 晚间 何一对 CZ 公共形象的战略表态
    '2043808460341395640': '',  # 何一 4.13 21:48 「CZ 公开做项目顾问不是理智的决策」

    # 4.14 书籍营销延续 — FOX TV 访谈 + 盗版提醒
    '2044063354189127962':
        '刚刚结束和 Charlie Gasparino 的 FOX TV 访谈。有谁有视频链接？',
    '2044077924865749138': '',  # 何一 4.14 15:38 盗版书识别
    '2044109444208799783':
        '说得在理，我不想把它写成一本自怜的书 😂',
    '2044115885254652056':
        '这是 FOX 访谈的视频片段。非常感谢 @CGasparino 🙏\n\nhttps://t.co/5z3UqHca4Q',

    # 4.14-4.15 书籍营销收尾 — Santos + AMA 直播
    '2044107562212000177':
        '很难想象，如果 Michael Santos 不用在监狱里度过那 26 年，他本可以做成多少事……他是我见过最自律、最勤奋的人之一。',
    '2044237628489511308':
        '书发布以来，社区一直在沸腾——表情包、迷你电影……还有人给我列了「我喜欢和讨厌的人」的排名（顺便说一句，是错的）😂\n\n明天将在 Binance Square 做一场直播 AMA，11 小时后开始，欢迎随便提问。直播期间会送出 10 本签名书。\n\n我在监狱里待了 4 个月，辣一点的问题应该没问题。\n\n📅 4 月 15 日 | 晚上 9 点 GMT+8\n🔗 https://t.co/DMQUIT7oFY',

    # 4.10 九妹 clean-up 跟推
    '2042410307092693258': '',  # 01:12 "被颠倒是非写进书里"
    '2042416393786950075': '',  # 01:36 "烤火" 比喻
    '2042525977407033694': '',  # 08:51 "尊重对手，写几条就回几条"

    # 4.10 何一 AI 水军 + 祸水东引 + 合规金身
    '2042579221378146423': '',  # 12:23 AI 水军
    '2042588208068800528': '',  # 12:59 祸水东引借刀杀人
    '2042628617696337971': '',  # 15:39 币圈黑社会塑合规金身

    # 4.10 下午 战火外溢
    '2042572358016237731': '',  # CZ short CN reply
    '2042584477696655727': '',  # Heyi CN reply re Bitget
    '2042633428948992396':
        '媒体关于币安「员工安置方案」的报道是误导性的，又在试图对 UAE 做负面文章。这根本不是什么新鲜事。币安一直为员工提供灵活的办公地点选择，并根据具体情况给予合理的搬迁方案（这些我在书里已经讲过）。\n\n'
        '我个人认为，UAE 依然是全世界最安全的国家之一，比世界上许多热门旅游国家都安全得多。\n\n'
        '事实上，我可能很快就会在迪拜办一场新书签售会。谁想来？',
}

# Which tweets should be highlighted (major turning points)
HIGHLIGHT = {
    '2041766531122823215',  # Star 4.8 bomb
    '2042278660149842029',  # CZ 1B bet
    '2042281554135994831',  # Star UBO counter
    '2042389031955415448',  # Star decline
}

# Stage grouping: tweet_id → stage_info. Stages are inserted as markers between tweets.
STAGE_MARKERS = {
    '1589861637271715840': {
        'act': '序 幕 · 2022',
        'title': '## 第一幕：2022，FTX 暴雷中的公开喊话',
        'note': '本书正文写到 FTX 暴雷与币安最后一刻退出收购 FTX（见第 18 章《加密的至暗时刻》）。但书中未提的是，FTX 雷声最响的那个清晨，徐明星曾公开发两条英文长推点名 CZ——那是他 2026 年回击的感情前哨。',
    },
    '2039913572239868338': {
        'act': '铺 垫',
        'title': '## 第二幕：2026 年 4 月 3–7 日，书的发布倒计时',
        'note': 'CZ 这一周高频预告书的发布——捐给慈善、书名由来、与 @scottmelker 的长访谈、Amazon 上线——完全没有预料到 4 月 8 日清晨，昔日旧友会用同一个话题发动奇袭。',
    },
    '2041684295303954874': None,  # no marker
    '2041763367292170477': {
        'act': '开 炮',
        'title': '## 第三幕：2026.04.08，12 年前的视频重见天日',
        'day': '2026 / 04 / 08',
        'note': '这是整场风波的起点。徐明星先发了中文版，不到 15 分钟后再发英文版，两条核心文案同步，然后补了一条"监狱四个月也没改掉撒谎本性"的补刀。',
    },
    '2042055343598166499': {
        'act': '清 晨',
        'title': '## 第四幕：2026.04.09 凌晨到中午，连珠炮',
        'day': '2026 / 04 / 09',
    },
    '2042278660149842029': {
        'act': 'C Z 出 手',
        'title': '## 第五幕：2026.04.09 16:29，CZ 用「10 亿美金」反杀',
        'note': '这是整场交锋中阅读量最高的一条——2,527 万阅读、6,273 赞、2,656 条回复。CZ 把徐明星 4 小时前的挑战原句引用，以同样的格式正面反击。',
    },
    '2042278971879116989': {
        'act': '再 一 枪',
        'title': '## 第六幕：2026.04.09 16:30–16:40，徐明星追击',
    },
    '2042283789330550885': {
        'act': '何 一 下 场',
        'title': '## 第七幕：2026.04.09 16:49–20:26，何一组合拳 + CZ 收尾',
        'note': '10 亿对赌发出后，何一连发 4 条推，从「打钱还是道歉」到「1B 给我们买 BNB 发给大家」，全程把徐明星钉在墙上；CZ 则补了一句「任选数字」再回到轻松模式——「去读那本书吧」。',
    },
    '2042389031955415448': {
        'act': '深 夜 回 应',
        'title': '## 第八幕：2026.04.09 23:47，徐明星婉拒对赌',
    },
    '2042408507077771473': {
        'act': '九 妹 开 场',
        'title': '## 第九幕：2026.04.10，OKX 九妹连发 5 推下场',
        'day': '2026 / 04 / 10',
        'note': '4 月 10 日凌晨开始，OKX 老员工九妹（@Cryptosis9_OKX）第一个从 OKX 一侧下场，5 条推文分三波：凌晨的「虚张声势 + 声东击西」长文分析、上午的短讽回击、下午 08:45 的 4 点正面反驳何一「一举六得」长文。',
    },
    '2042459400296685583': {
        'act': '何 一 长 推',
        'title': '## 第十幕：2026.04.10 04:27，何一「一举六得」长文反戈',
        'note': '这是何一的高潮回应——一千字长文，列出徐明星这场攻击背后的「一举六得」六层算计，直接把话题从「CZ 婚姻」扳回「OKX 用碰瓷抢市场份额」。这条推文直接触发了 4 小时后 OKX 员工 @Cryptosis9_OKX（九妹）亲自下场的 4 点正面反驳。',
    },
    '2042524484167700755': {
        'act': '九 妹 正 面 回 应',
        'title': '## 第十一幕：2026.04.10 08:45，九妹 4 点反驳「一举六得」',
        'note': '何一那条「一举六得」长文点燃了 OKX 团队。九妹在 4 小时后发出 4 点反驳，主攻 1011 事件、BNB 链 MEME、合规、首富叙事——把战线从「3 位老板互撕」扩大为「两家公司的 PR 对冲」。她在推文中直接贴出何一长文的截图作为被回应的对象。',
    },
    '2042584477696655727': {
        'act': '战 火 外 溢',
        'title': '## 第十二幕：2026.04.10 下午，战火从 OKX 扩散到 Bitget 与 UAE 搬迁新闻',
        'note': '围绕回忆录的骂战已经把舆论烧热，任何针对币安的消息都会被立刻回击。下午先是何一怼 Bitget 恶意传播币安赔偿谣言、为币安「同舟计划」澄清；接着 CZ 正面回应 CoinDesk / 吴说关于「币安员工大规模撤离 UAE」的报道，并反手发出 Dubai 签售会邀约。战局从「CZ × 徐明星 × 九妹」三向互撕，进一步扩散为「币安 VS 所有质疑者」。',
    },
    '2042778101961134291': {
        'act': '余 波 · 书 评 季',
        'title': '## 第十三幕：2026.04.11，骂战降温 + 书籍营销进入 Forbes 书评季',
        'day': '2026 / 04 / 11',
        'note': '骂战 72 小时后明显降温。CZ 这一天回到书籍营销节奏——晒与读者见面后的老照片、回应读者提问、分享 Forbes 的书评以及 Kindle 畅销榜排名。九妹在一条针对第三方的回复里抛出一句「脏事儿干多了总有一天会被反噬」的暗讽，但再无长文输出。徐明星与何一均未继续发话。',
    },
}

X_LOGO = '''<svg class="tweet-card__logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'''


def parse_created(s):
    return datetime.strptime(s, '%a %b %d %H:%M:%S %z %Y')


def role_class(screen_name):
    return {
        'cz_binance': 'cz',
        'star_okx': 'star',
        'heyibinance': 'heyi',
        'Cryptosis9_OKX': 'ninemei',
    }.get(screen_name, '')


def avatar_path(screen_name):
    return {
        'cz_binance': '/images/twitter-feud/avatar-cz.jpg',
        'star_okx': '/images/twitter-feud/avatar-star.jpg',
        'heyibinance': '/images/twitter-feud/avatar-heyi.jpg',
        'Cryptosis9_OKX': '/images/twitter-feud/avatar-9mei.jpg',
    }.get(screen_name, '')


def fmt_count(n):
    if n is None: return '0'
    try: n = int(n)
    except: return str(n)
    if n >= 10000:
        return f'{n/10000:.1f} 万'
    return f'{n:,}'


def text_to_html(text):
    """Convert newlines to <br> and escape none (text is trusted from Twitter API)."""
    return (text or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') \
        .replace('\n\n', '<br><br>').replace('\n', '<br>')


def render_quoted(q):
    if not q:
        return ''
    qtxt = text_to_html(q.get('text',''))
    if len(qtxt) > 900:
        qtxt = qtxt[:900] + '…'
    return (
        '<div class="tweet-card__quoted">'
        f'<div class="tweet-card__quoted-head">↳ 引用 <strong>@{q["screen_name"]}</strong>'
        f' · {parse_created(q["created_at"]).strftime("%m-%d %H:%M UTC")}</div>'
        f'<div class="tweet-card__quoted-body">{qtxt}</div>'
        '</div>'
    )


def render_card(t):
    sn = t['screen_name']
    role = role_class(sn)
    highlight = ' tweet-card--highlight' if t['id'] in HIGHLIGHT else ''
    cls = f'tweet-card tweet-card--{role}{highlight}' if role else 'tweet-card'
    dt = parse_created(t['created_at'])
    ts = dt.strftime('%Y-%m-%d %H:%M UTC')

    text_html = text_to_html(t['text'])
    zh = TRANSLATIONS.get(t['id'], '')
    zh_html = f'<div class="tweet-card__body tweet-card__body--zh">{text_to_html(zh)}</div>' if zh else ''

    quoted_html = render_quoted(t.get('quoted_tweet'))

    # Map tweet_id → (local_image_filename, optional_caption)
    LOCAL_MEDIA = {
        '2039913572239868338': ('cz-book-cover.jpg', '📎 推文配图：《Freedom of Money》书籍封面'),
        '2042130369294860397': ('star-marriage-cn.jpg', '📎 推文配图：CoinDesk 报道截图（CZ 妻子法官求情信相关）'),
        '2042130511456563276': ('star-marriage-en.jpg', '📎 推文配图：CoinDesk 报道截图（CZ 妻子法官求情信相关）'),
        '2042524484167700755': ('9mei-quoted-heyi.jpg', '📎 推文配图：何一 4 月 10 日清晨 04:27 的「一举六得」千字长文原推截图'),
    }
    media_html = ''
    if t.get('media'):
        for m in t['media']:
            if m.get('type') == 'photo':
                if t['id'] in LOCAL_MEDIA:
                    fname, cap = LOCAL_MEDIA[t['id']]
                    src = f'/images/twitter-feud/{fname}'
                    caption = f'<div class="tweet-card__media-caption">{cap}</div>'
                else:
                    src = m.get('url', '')
                    caption = ''
                media_html += f'<div class="tweet-card__media"><img src="{src}" alt="attached media">{caption}</div>'

    likes = fmt_count(t.get('likes'))
    rts = fmt_count(t.get('retweets'))
    repl = fmt_count(t.get('replies'))
    views = fmt_count(t.get('views'))

    metrics = (
        f'<span>💬 {repl}</span>'
        f'<span>🔁 {rts}</span>'
        f'<span>❤️ {likes}</span>'
        f'<span>👁 {views}</span>'
    )

    return (
        f'<div class="{cls}">'
        '<div class="tweet-card__head">'
        f'<img class="tweet-card__avatar" src="{avatar_path(sn)}" alt="{t["author"]}">'
        '<div class="tweet-card__meta">'
        f'<div class="tweet-card__name">{t["author"]} <span class="tweet-card__verified">✓</span></div>'
        f'<div class="tweet-card__handle">@{sn} · {ts}</div>'
        '</div>'
        f'{X_LOGO}'
        '</div>'
        f'<div class="tweet-card__body">{text_html}</div>'
        f'{zh_html}'
        f'{media_html}'
        f'{quoted_html}'
        f'<div class="tweet-card__metrics">{metrics}</div>'
        f'<a class="tweet-card__link" href="{t["url"]}" target="_blank" rel="noopener">查看原推 →</a>'
        '</div>'
    )


def render_stage(info):
    if not info: return ''
    out = []
    if 'title' in info:
        out.append(info['title'])
    if 'day' in info:
        out.append(f'<div class="feud-day"><span class="feud-day__label">{info["day"]}</span></div>')
    if 'act' in info:
        out.append(f'<div class="feud-act"><strong>{info["act"]}</strong></div>')
    if 'note' in info:
        out.append(f'<div class="feud-note">\n\n{info["note"]}\n\n</div>')
    return '\n\n'.join(out) + '\n\n'


def main():
    # Always rebuild tweets list from raw per-id JSONs in scripts/feud-raw/
    # then write back both the site JSON and the page markdown.
    from pathlib import Path
    raws = []
    for f in sorted(Path(RAW_DIR).glob('*.json')):
        try:
            raws.append(json.loads(f.read_text()))
        except Exception as e:
            print(f'[warn] cannot parse {f}: {e}')
    raws.sort(key=lambda x: parse_created(x['created_at']))
    def _slim(r, is_quote=False):
        out = {
            'id': r['id'],
            'author': r['author'],
            'screen_name': r['screen_name'],
            'text': r['text'],
            'created_at': r['created_at'],
            'created_at_iso': parse_created(r['created_at']).strftime('%Y-%m-%d %H:%M UTC'),
            'likes': r.get('likes',0),
            'retweets': r.get('retweets',0),
            'replies': r.get('replies',0),
            'views': r.get('views',0),
            'url': r.get('url', f'https://x.com/i/status/{r["id"]}'),
        }
        if r.get('media'):
            out['media'] = r['media']
        if not is_quote and r.get('quoted_tweet'):
            out['quoted_tweet'] = _slim(r['quoted_tweet'], is_quote=True)
        return out
    tweets = [_slim(r) for r in raws]
    Path(DATA).write_text(json.dumps(tweets, ensure_ascii=False, indent=2))

    head = '''---
title: "番外：Twitter 风暴"
---

# Twitter 风暴：回忆录引爆的 11 年恩怨

<div class="feud-hero">
  <div class="feud-hero__tag">BONUS CHAPTER</div>
  <div class="feud-hero__title">当 2015 与 2026 在时间线上对撞</div>
  <div class="feud-hero__sub">CZ × 徐明星 × 何一 × OKX 九妹 · 一本回忆录引爆的旧债清算</div>
  <div class="feud-hero__avatars">
    <img src="/images/twitter-feud/avatar-cz.jpg" alt="CZ">
    <img src="/images/twitter-feud/avatar-star.jpg" alt="Star Xu">
    <img src="/images/twitter-feud/avatar-heyi.jpg" alt="He Yi">
    <img src="/images/twitter-feud/avatar-9mei.jpg" alt="9mei">
  </div>
</div>

## 缘起

本书正体中文版于 2026 年 4 月上架。书中第 9 章「加密世界 2013」里的「北京岁月」一节，CZ 重述了 2014–2015 年他在 OKCoin 的那段经历：10% 股权、被重谈股权后辞职、Roger Ver 与徐明星因 bitcoin.com 域名费公开翻脸、徐明星转而指责他「任职时伪造了合约」，以及何一拒绝公开指责他并辞职声援。

书里 CZ 对这段话的定调非常轻描淡写：「事实是，这件事发生时我早已离职，我根本没见过他口中那份『假合约』。」

这段话点燃了 OKX 创始人徐明星。2026 年 4 月 8 日到 10 日的 80 小时里，他在 X 上连发中英双语共 9 条长推清算旧账；CZ 发出「10 亿美金赌已离婚」的反杀，又跟了一条「任选数字，拿出点男人的担当」的追击；何一连发 7 条追打、开出币安 App 的链上预测市场「徐明星会否公开道歉？」，并在 4 月 10 日清晨发出一篇千字长文《一举六得》直接把战火引回 OKX 的商业逻辑；4 小时后，OKX 老员工九妹（@Cryptosis9_OKX）亲自下场，发 4 点反驳延续战局。本页按时间顺序收录这一时段四方的 **全部相关原推**（含中英双语版本、引用链、@ 回复、媒体截图），配对方互相引用时的嵌套卡与原推链接。

<div class="feud-note">

读者从书里看到的是 CZ 自述的 2015 往事；从这一页，则是同一段往事里另一位当事人 11 年后的反驳，以及本轮交锋中每一条推文的原始证据。本页不做评判，只把时间、文本、数据排好，让读者自行比对。本页所有推文均通过公开 X GraphQL API 抓取，原推 URL 全量标注。

</div>

## 时间线总览

<div class="feud-axis">
  <div class="feud-axis__node"><span class="feud-axis__date">2014.04</span>CZ 加入 OKCoin，获得 10% 股权</div>
  <div class="feud-axis__node"><span class="feud-axis__date">2015.01</span>徐明星欲重谈股权 → CZ 递辞呈</div>
  <div class="feud-axis__node"><span class="feud-axis__date">2015.05</span>Roger Ver 与徐明星公开翻脸；徐明星指 CZ「伪造合约」，CZ 发 Reddit 帖澄清</div>
  <div class="feud-axis__node"><span class="feud-axis__date">2015</span>徐明星向何一施压未果，何一辞职声援 CZ</div>
  <div class="feud-axis__node"><span class="feud-axis__date">2022.11</span>FTX 暴雷，徐明星公开喊话 CZ 停止抛售 FTT</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.03</span>CZ 宣布《Freedom of Money》下周发布</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.08</span>徐明星甩出 12 年前 v7 / v8 合约的 YouTube 取证视频</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.09</span>CZ 10 亿对赌 → 徐明星追击 → 何一组合拳 → Star 深夜拒赌</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.10 01:05</span>OKX 九妹 @Cryptosis9_OKX 凌晨首发「虚张声势 + 声东击西」长文</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.10 04:27</span>何一「一举六得」千字长文反戈</div>
  <div class="feud-axis__node feud-axis__node--hot"><span class="feud-axis__date">2026.04.10 08:45</span>九妹 4 点正面反驳「一举六得」</div>
</div>

## 背景书摘：第 9 章《北京岁月》

<div class="feud-note">

以下摘自本书第 9 章——CZ 本人对这段往事的叙述。徐明星 2026 年 4 月 8 日的反击，正是对这段内容的直接回应。

</div>

> 2015 年 1 月，当徐明星试图重新谈判我那 10% 的股权时，我没有犹豫，直接递上了辞呈。
>
> 在我离开北京几个月后，Roger Ver 和徐明星因为 bitcoin.com 域名使用费公开撕破脸。⋯⋯几天后，徐明星突然声称，问题源于我任职时「伪造了合约」。事实是，这件事发生时我早已离职，我根本没见过他口中那份「假合约」。
>
> 2015 年 5 月，我在 Reddit 发帖澄清：我从未伪造任何文件，也完全没有动机这么做。⋯⋯徐明星对此极为不满，对我进行人身攻击，甚至还向何一施压，要求她公开指责我。何一拒绝了，并选择辞职。

书里这段的下一句，是 CZ 对这段关系的一锤定音：「从此开始了针对我与何一的持续攻击。」 十一年后，被点名的徐明星等到了回击的机会——CZ 的书。

'''

    parts = [head]
    for t in tweets:
        marker = STAGE_MARKERS.get(t['id'])
        if marker:
            parts.append(render_stage(marker))
        parts.append(render_card(t))
        parts.append('\n\n')

    tail = '''

## 尾声

这一轮交锋从 4 月 8 日清晨 6 点 21 分徐明星第一条中文长推开始，到 4 月 10 日上午 8 点 45 分 OKX 九妹的 4 点反驳发出为止，持续了约 74 小时。期间徐明星发布了 9 条核心反击推文（中英双语），CZ 发了 3 条正面回应，何一发了 7 条贴身紧逼加一篇「一举六得」千字长文，OKX 员工九妹接力发 4 点鞭炮，加上双方 10 余条 @ 往复。

十一年前北京五道口，v7 与 v8 两个版本的合同、一段 3 分 2 秒的 YouTube 取证视频、一篇 Reddit 澄清帖，没能让双方达成任何共识。十一年后，一本回忆录把这段旧事重新写了一遍，另一方的所有情绪和档案也因此重新回到公众视野。

书里那句「从此开始了针对我与何一的持续攻击」，和 Twitter 上那句「如果不是那本充满谎言的书把我硬生生拖进来」，至今仍是同一件事的两种讲法。真相究竟在哪一边，本页不做评判——把证据、时间、原推全部排好，剩下的交给读者。

<div class="feud-disclaimer">

本页所有推文均通过公开 X GraphQL API（x-api skill）抓取，原推 URL 已全部标注；数字互动指标采集时间为 2026-04-10。中文翻译为编者整理，力求忠实原意；Star_OKX 的攻击推文本人原本就同时发布了中英双语版本，本页均按发布顺序完整呈现。<br>
原始 JSON 数据：<a href="/data/twitter-feud.json" target="_blank">/data/twitter-feud.json</a>

</div>
'''
    parts.append(tail)

    Path(OUT).write_text(''.join(parts))
    print(f'wrote {OUT}')
    print(f'total cards: {len(tweets)}')


if __name__ == '__main__':
    main()
