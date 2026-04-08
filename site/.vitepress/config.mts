import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '币安人生',
  description: '幸运、韧性与保护用户的回忆录 — 赵长鹏自传',
  base: '/',

  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { href: 'https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap', rel: 'stylesheet' }],
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '开始阅读', link: '/chapters/00-recommendations' },
    ],

    sidebar: [
      {
        text: '序',
        items: [
          { text: '推荐语', link: '/chapters/00-recommendations' },
          { text: '献词', link: '/chapters/01-dedication' },
          { text: '序言：外面没有别人', link: '/chapters/02-preface' },
          { text: '前言', link: '/chapters/03-foreword' },
        ]
      },
      {
        text: '早年岁月',
        items: [
          { text: '早年岁月', link: '/chapters/05-early-years' },
          { text: '温哥华，1989-1995', link: '/chapters/06-vancouver' },
          { text: '麦基尔岁月，1995-1999', link: '/chapters/07-mcgill' },
          { text: '东京岁月', link: '/chapters/08-tokyo-years' },
        ]
      },
      {
        text: '走进加密世界',
        items: [
          { text: '初识比特币：2013', link: '/chapters/09-bitcoin-2013' },
          { text: '比捷科技', link: '/chapters/10-bijie-tech' },
          { text: '币安诞生', link: '/chapters/11-binance-birth' },
        ]
      },
      {
        text: '币安崛起',
        items: [
          { text: '币安上线', link: '/chapters/04-binance-launch' },
          { text: '中国禁令', link: '/chapters/12-china-ban' },
          { text: '东京', link: '/chapters/13-tokyo' },
          { text: '世界第一', link: '/chapters/14-number-one' },
          { text: '一周年庆典', link: '/chapters/15-anniversary' },
        ]
      },
      {
        text: '挑战与风暴',
        items: [
          { text: '2019 加密寒冬', link: '/chapters/16-crypto-winter-2019' },
          { text: '2020', link: '/chapters/17-year-2020' },
          { text: '棘手案例', link: '/chapters/18-tricky-cases' },
          { text: '2021', link: '/chapters/19-year-2021' },
          { text: '2022年，漫游地球', link: '/chapters/20-roaming-earth-2022' },
        ]
      },
      {
        text: '美国之路',
        items: [
          { text: '2023年，司法部谈判', link: '/chapters/21-doj-2023' },
          { text: '飞去美国', link: '/chapters/22-flying-to-america' },
          { text: '美国的"支持加密"时代', link: '/chapters/23-pro-crypto-era' },
          { text: '特赦', link: '/chapters/24-pardon' },
        ]
      },
      {
        text: '尾声',
        items: [
          { text: '结语', link: '/chapters/25-epilogue' },
          { text: '附录：CZ 的原则', link: '/chapters/26-cz-principles' },
        ]
      },
    ],

    outline: {
      level: [2, 3],
      label: '本章目录',
    },

    docFooter: {
      prev: '上一章',
      next: '下一章',
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/riba2534/cz_memoirs' },
    ],

    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '返回顶部',
  },
})
