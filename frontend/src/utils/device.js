/**
 * 设备检测工具
 */

export function isMobile() {
  const ua = navigator.userAgent
  const mobileAgents = ['Android', 'iPhone', 'iPad', 'iPod', 'Windows Phone']
  
  // 检查用户代理字符串
  for (const agent of mobileAgents) {
    if (ua.includes(agent)) {
      return true
    }
  }
  
  // 检查屏幕宽度
  if (window.innerWidth <= 768) {
    return true
  }
  
  return false
}

export function isIOS() {
  return /iPhone|iPad|iPod/i.test(navigator.userAgent)
}

export function isAndroid() {
  return /Android/i.test(navigator.userAgent)
}

