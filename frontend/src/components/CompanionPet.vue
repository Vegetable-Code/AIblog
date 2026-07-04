<template>
  <div
    class="fixed bottom-6 left-6 z-[100] select-none"
    @mouseenter="onHover"
    @mouseleave="onLeave"
    :class="petClass"
  >
    <!-- SVG 小狐狸 -->
    <svg
      :class="['transition-all duration-300 cursor-pointer', bodyClass]"
      :style="{ filter: sleep ? 'grayscale(0.5)' : 'none' }"
      width="80"
      height="80"
      viewBox="0 0 100 100"
      @click="onClick"
    >
      <!-- 左耳 -->
      <polygon points="30,42 15,12 38,32" :fill="earColor" class="transition-colors duration-300" />
      <!-- 右耳 -->
      <polygon points="70,42 85,12 62,32" :fill="earColor" class="transition-colors duration-300" />
      <!-- 左耳内侧 -->
      <polygon points="30,40 19,18 36,33" fill="#f472b6" opacity="0.4" />
      <!-- 右耳内侧 -->
      <polygon points="70,40 81,18 64,33" fill="#f472b6" opacity="0.4" />
      <!-- 脸 -->
      <ellipse cx="50" cy="52" rx="28" ry="25" :fill="faceColor" />
      <!-- 左眼 -->
      <g :class="eyeClass">
        <ellipse cx="39" cy="48" rx="5" ry="6" fill="white" />
        <ellipse cx="39" cy="48" rx="3" ry="3.5" fill="#1e293b" />
        <circle cx="37" cy="46" r="1.2" fill="white" />
      </g>
      <!-- 右眼 -->
      <g :class="eyeClass">
        <ellipse cx="61" cy="48" rx="5" ry="6" fill="white" />
        <ellipse cx="61" cy="48" rx="3" ry="3.5" fill="#1e293b" />
        <circle cx="59" cy="46" r="1.2" fill="white" />
      </g>
      <!-- 鼻子 -->
      <ellipse cx="50" cy="55" rx="3" ry="2" fill="#1e293b" />
      <!-- 嘴巴 -->
      <path d="M47,57 Q50,61 53,57" fill="none" stroke="#1e293b" stroke-width="1.2" stroke-linecap="round" />
      <!-- 胡须左 -->
      <line x1="15" y1="52" x2="34" y2="54" stroke="#94a3b8" stroke-width="0.8" stroke-linecap="round" />
      <line x1="14" y1="57" x2="34" y2="57" stroke="#94a3b8" stroke-width="0.8" stroke-linecap="round" />
      <!-- 胡须右 -->
      <line x1="85" y1="52" x2="66" y2="54" stroke="#94a3b8" stroke-width="0.8" stroke-linecap="round" />
      <line x1="86" y1="57" x2="66" y2="57" stroke="#94a3b8" stroke-width="0.8" stroke-linecap="round" />
      <!-- 身体 -->
      <ellipse cx="50" cy="78" rx="22" ry="14" :fill="bodyColor" />
      <!-- 尾巴 -->
      <path d="M72,78 Q90,60 82,48 Q78,42 80,50 Q82,60 72,78" :fill="tailColor" class="transition-transform duration-500" :class="{ 'origin-bottom-left rotate-12': wag }" />
      <!-- 睡觉 Zzz -->
      <g v-if="sleep" class="zzz">
        <text x="75" y="30" font-size="10" fill="#94a3b8" font-weight="bold" class="animate-bounce" style="animation-delay:0ms">Z</text>
        <text x="65" y="18" font-size="8" fill="#64748b" font-weight="bold" class="animate-bounce" style="animation-delay:200ms">z</text>
        <text x="72" y="8" font-size="6" fill="#475569" font-weight="bold" class="animate-bounce" style="animation-delay:400ms">z</text>
      </g>
      <!-- 爱心（点击后） -->
      <g v-if="showHeart" class="heart-anim">
        <text x="20" y="25" font-size="22" fill="#f472b6">❤️</text>
      </g>
      <!-- 气泡（悬停时） -->
      <g v-if="showBubble" class="bubble-anim">
        <rect x="10" y="-5" width="60" height="22" rx="10" fill="#1e293b" stroke="#475569" stroke-width="0.5" />
        <text x="40" y="10" font-size="9" fill="#94a3b8" text-anchor="middle">{{ bubbleText }}</text>
      </g>
    </svg>

    <!-- 名字标签 -->
    <div class="text-[10px] text-slate-500 text-center mt-0.5 tracking-wider">小狸</div>
  </div>
</template>

<style scoped>
/* 浮动呼吸动画 */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}
.float-anim {
  animation: float 3s ease-in-out infinite;
}

/* 摇尾巴 */
@keyframes wagTail {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(15deg); }
  75% { transform: rotate(-10deg); }
}
.wag-anim {
  animation: wagTail 0.4s ease-in-out 3;
}

/* 跳跃 */
@keyframes jump {
  0% { transform: translateY(0) scale(1); }
  30% { transform: translateY(-20px) scale(1.1); }
  50% { transform: translateY(-25px) scale(1.15); }
  70% { transform: translateY(-10px) scale(1.05); }
  100% { transform: translateY(0) scale(1); }
}
.jump-anim {
  animation: jump 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 爱心飞出 */
@keyframes heartFloat {
  0% { opacity: 1; transform: translateY(0) scale(1); }
  100% { opacity: 0; transform: translateY(-40px) scale(1.5); }
}
.heart-anim text {
  animation: heartFloat 0.8s ease-out forwards;
}

/* 气泡出现 */
@keyframes bubbleIn {
  from { opacity: 0; transform: translateY(5px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.bubble-anim {
  animation: bubbleIn 0.3s ease-out;
}

/* 眨眼 */
@keyframes blink {
  0%, 95%, 100% { transform: scaleY(1); }
  97% { transform: scaleY(0.1); }
}
.blink-anim {
  animation: blink 3s ease-in-out infinite;
}

/* 打盹抖动 */
@keyframes doze {
  0%, 100% { transform: translateY(0); }
  10% { transform: translateY(-1px); }
  20% { transform: translateY(0); }
}
.doze-anim {
  animation: doze 4s ease-in-out infinite;
}
</style>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 颜色模式（可根据暗色/亮色主题适配）
const isDark = ref(true)
const faceColor = computed(() => isDark.value ? '#fb923c' : '#fdba74')
const earColor = computed(() => isDark.value ? '#f97316' : '#fb923c')
const bodyColor = computed(() => isDark.value ? '#f97316' : '#fdba74')
const tailColor = computed(() => isDark.value ? '#ea580c' : '#fb923c')

// 状态
const sleep = ref(false)
const wag = ref(false)
const jump = ref(false)
const showHeart = ref(false)
const showBubble = ref(false)
const hovered = ref(false)
const bubbleText = ref('')

const petClass = computed(() => ({
  'float-anim': !jump.value && !sleep.value && !hovered.value,
  'doze-anim': sleep.value,
}))

const bodyClass = computed(() => {
  if (jump.value) return 'jump-anim'
  if (hovered.value) return 'scale-110'
  return ''
})

const eyeClass = computed(() => {
  if (sleep.value) return 'opacity-0'
  return 'blink-anim'
})

// 闲置计时器
let idleTimer = null
function resetIdleTimer() {
  sleep.value = false
  clearTimeout(idleTimer)
  idleTimer = setTimeout(() => {
    sleep.value = true
  }, 15000)
}

function onHover() {
  hovered.value = true
  showBubble.value = true
  const msgs = ['你好呀 👋', '戳我一下~', '今天心情不错!', '嘿嘿~']
  bubbleText.value = msgs[Math.floor(Math.random() * msgs.length)]
  resetIdleTimer()
}

function onLeave() {
  hovered.value = false
  showBubble.value = false
  jump.value = false
  resetIdleTimer()
}

function onClick() {
  jump.value = true
  showHeart.value = true
  wag.value = true
  setTimeout(() => {
    jump.value = false
    wag.value = false
    showHeart.value = false
  }, 800)
  resetIdleTimer()
}

onMounted(() => {
  resetIdleTimer()
  // 检测主题（监听 body class 变化）
  const observer = new MutationObserver(() => {
    isDark.value = !document.documentElement.classList.contains('light')
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  onUnmounted(() => observer.disconnect())
})

onUnmounted(() => {
  clearTimeout(idleTimer)
})
</script>
