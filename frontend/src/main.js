import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 根据设备类型引入不同的UI库
import { isMobile } from './utils/device'

if (typeof window !== 'undefined' && typeof window.URL !== 'undefined' && typeof window.URL.parse !== 'function') {
  window.URL.parse = (input, base) => {
    try {
      return base ? new window.URL(input, base) : new window.URL(input)
    } catch (error) {
      return null
    }
  }
}

const app = createApp(App)
const pinia = createPinia()

// 初始化应用
async function initApp() {
  if (isMobile()) {
    // 移动端使用 Vant
    await import('vant/lib/index.css')
    await import('@vant/touch-emulator') // PC端模拟移动端touch事件

    // 按需引入Vant组件
    const Vant = await import('vant')
    app.use(Vant.Button)
    app.use(Vant.Form)
    app.use(Vant.Field)
    app.use(Vant.CellGroup)
    app.use(Vant.Cell)
    app.use(Vant.List)
    app.use(Vant.Empty)
    app.use(Vant.Uploader)
    app.use(Vant.Image)
    app.use(Vant.ImagePreview)
    app.use(Vant.Dialog)
    app.use(Vant.NavBar)
    app.use(Vant.Tab)
    app.use(Vant.Tabs)
    app.use(Vant.Tag)
    app.use(Vant.Search)
    app.use(Vant.Popup)
    app.use(Vant.ActionSheet)
    app.use(Vant.Toast)
    app.use(Vant.Loading)
    app.use(Vant.Overlay)
    app.use(Vant.PullRefresh)
    app.use(Vant.Divider)
    app.use(Vant.Progress)
    app.use(Vant.NoticeBar)
    app.use(Vant.Icon)
    app.use(Vant.Picker)
  } else {
    // PC端使用 Element Plus
    await import('element-plus/dist/index.css')
    const ElementPlus = await import('element-plus')
    app.use(ElementPlus.default)
  }

  app.use(pinia)
  app.use(router)
  app.mount('#app')
}

initApp()

