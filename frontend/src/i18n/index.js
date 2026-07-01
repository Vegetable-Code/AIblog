import { createI18n } from 'vue-i18n'
import axios from 'axios'

import zhCN from './zh-CN.json'
import enUS from './en-US.json'
import jaJP from './ja-JP.json'

// Detect initial locale: localStorage > browser language > default
function detectLocale() {
  const saved = localStorage.getItem('locale')
  if (saved) return saved

  const lang = navigator.language || navigator.userLanguage || ''
  if (lang.startsWith('zh')) return 'zh-CN'
  if (lang.startsWith('ja')) return 'ja-JP'
  if (lang.startsWith('ko')) return 'ko-KR'

  return 'zh-CN'  // default
}

const i18n = createI18n({
  legacy: false,
  locale: detectLocale(),
  fallbackLocale: 'zh-CN',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS,
    'ja-JP': jaJP,
  },
})

// Async: try to get locale from backend (IP-based)
export async function initLocale() {
  try {
    const saved = localStorage.getItem('locale')
    if (saved) return saved  // user's manual choice takes priority

    const res = await axios.get('/api/v1/i18n/locale', { timeout: 3000 })
    const locale = res.data.locale
    if (locale && ['zh-CN', 'en-US', 'ja-JP', 'zh-TW', 'ko-KR', 'de-DE', 'fr-FR', 'ru-RU', 'pt-BR'].includes(locale)) {
      const normalized = locale === 'zh-TW' ? 'zh-CN' : locale  // fallback unsupported
      i18n.global.locale.value = normalized
      return normalized
    }
  } catch (e) {
    // ignore - use default
  }
  return i18n.global.locale.value
}

// Switch locale manually (stored in localStorage)
export function setLocale(locale) {
  const normalized = ['zh-CN', 'en-US', 'ja-JP', 'zh-TW', 'ko-KR', 'de-DE', 'fr-FR', 'ru-RU', 'pt-BR'].includes(locale)
    ? locale
    : 'zh-CN'
  const target = normalized === 'zh-TW' ? 'zh-CN' : normalized
  i18n.global.locale.value = target
  localStorage.setItem('locale', target)
  document.documentElement.lang = target
}

export default i18n
