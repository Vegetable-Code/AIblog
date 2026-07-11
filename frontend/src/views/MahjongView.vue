<template>
  <div class="min-h-[70vh]">
    <div v-if="!room" class="max-w-md mx-auto pt-20">
      <div class="bg-slate-800 rounded-2xl p-8 border border-slate-700 shadow-xl text-center">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </div>
        <h2 class="text-2xl font-bold text-white mb-2">广东麻将</h2>
        <p class="text-slate-400 text-sm mb-6">多人在线对战的广东麻将游戏</p>
        <div class="space-y-3">
          <div class="flex gap-3">
            <input v-model="nickname" placeholder="输入昵称"
              class="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 text-sm"
              maxlength="10" @keyup.enter="createRoom" />
            <input v-model="roomIdInput" placeholder="房间号"
              class="w-28 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 text-sm"
              maxlength="4" @keyup.enter="joinRoom" />
          </div>
          <div class="flex gap-3">
            <button @click="createRoom"
              class="flex-1 py-2.5 px-4 bg-gradient-to-r from-cyan-500 to-emerald-500 text-white font-medium rounded-xl hover:from-cyan-400 hover:to-emerald-400 transition-all text-sm">
              创建房间
            </button>
            <button @click="joinRoom" :disabled="!roomIdInput"
              class="flex-1 py-2.5 px-4 bg-slate-700 text-white font-medium rounded-xl hover:bg-slate-600 transition-all text-sm disabled:opacity-40">
              加入房间
            </button>
          </div>
          <p v-if="error" class="text-red-400 text-xs mt-2">{{ error }}</p>
        </div>
      </div>
    </div>
    <div v-else class="relative">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-3">
          <div class="px-3 py-1.5 bg-slate-800 rounded-xl border border-slate-700 text-sm">
            <span class="text-slate-500">房间</span>
            <span class="text-cyan-400 font-mono ml-1">{{ roomId }}</span>
          </div>
          <div class="px-3 py-1.5 bg-slate-800 rounded-xl border border-slate-700 text-sm">
            <span class="text-slate-500">余牌</span>
            <span class="text-white font-mono ml-1">{{ gameState?.wall_count ?? 0 }}</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span v-if="gameStatus === 'playing'" class="text-xs text-emerald-400 animate-pulse">游戏中</span>
          <button @click="leaveRoom" class="px-3 py-1.5 text-xs text-slate-500 hover:text-red-400 bg-slate-800 rounded-xl border border-slate-700 transition-colors">离开</button>
        </div>
      </div>
      <div class="relative bg-slate-800/50 border border-slate-700 rounded-2xl p-4 md:p-6 min-h-[500px]">
        <div class="flex justify-center mb-6">
          <div v-if="onlinePlayers[2]" class="text-center">
            <div class="w-12 h-12 mx-auto rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center text-white font-bold text-sm border-2"
              :class="currentTurn === 2 ? 'border-cyan-400 animate-pulse' : 'border-transparent'">{{ onlinePlayers[2].nickname[0] }}</div>
            <p class="text-xs text-slate-400 mt-1">{{ onlinePlayers[2].nickname }}</p>
            <p class="text-xs text-slate-500">{{ handCount(2) }}枚</p>
            <div class="flex gap-1 justify-center mt-1">
              <template v-for="m in (onlinePlayers[2].melds || [])" :key="m[1] + m[2]">
                <div class="w-5 h-7 rounded text-[8px] flex items-center justify-center bg-slate-700 text-slate-300 font-mono">{{ tileLabel(m[1]) }}</div>
              </template>
            </div>
          </div>
          <div v-else class="w-12 h-12 rounded-full bg-slate-700/50 border-2 border-dashed border-slate-600 flex items-center justify-center text-slate-500 text-xs mx-auto">等待中</div>
        </div>
        <div class="flex items-start justify-between mb-6 gap-4">
          <div class="flex flex-col items-center gap-2 pt-6" v-if="onlinePlayers[3]">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center text-white font-bold text-xs border-2"
              :class="currentTurn === 3 ? 'border-cyan-400 animate-pulse' : 'border-transparent'">{{ onlinePlayers[3].nickname[0] }}</div>
            <p class="text-xs text-slate-400">{{ onlinePlayers[3].nickname }}</p>
            <p class="text-xs text-slate-500">{{ handCount(3) }}枚</p>
          </div>
          <div class="flex-1 min-h-[200px]">
            <div class="relative bg-slate-900/50 rounded-xl border border-slate-700/50 p-4 min-h-[160px]">
              <div class="flex flex-wrap gap-1 justify-center">
                <template v-for="(discard, di) in discards" :key="di">
                  <div class="w-8 h-10 rounded text-xs flex items-center justify-center font-medium"
                    :class="getTileClass(discard)" :style="getTileStyle(discard)">{{ tileLabel(discard) }}</div>
                </template>
                <div v-if="discards.length === 0" class="text-slate-600 text-xs text-center w-full py-8">等待出牌...</div>
              </div>
            </div>
            <div class="flex justify-center gap-3 mt-4">
              <div v-if="lastDiscardTile" class="w-12 h-14 rounded-lg text-sm flex items-center justify-center font-bold animate-bounce"
                :class="getTileClass(lastDiscardTile)" :style="getTileStyle(lastDiscardTile)">{{ tileLabel(lastDiscardTile) }}</div>
            </div>
            <div v-if="pendingActions.length > 0" class="flex justify-center gap-2 mt-4">
              <button v-for="act in pendingActions" :key="act" @click="sendAction(act)"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
                :class="act === 'hu' ? 'bg-red-500 hover:bg-red-400 text-white' : act === 'pung' ? 'bg-emerald-500 hover:bg-emerald-400 text-white' : act === 'kong' ? 'bg-amber-500 hover:bg-amber-400 text-white' : 'bg-slate-700 hover:bg-slate-600 text-white'">
                {{ actionLabel(act) }}
              </button>
            </div>
          </div>
          <div class="flex flex-col items-center gap-2 pt-6" v-if="onlinePlayers[1]">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center text-white font-bold text-xs border-2"
              :class="currentTurn === 1 ? 'border-cyan-400 animate-pulse' : 'border-transparent'">{{ onlinePlayers[1].nickname[0] }}</div>
            <p class="text-xs text-slate-400">{{ onlinePlayers[1].nickname }}</p>
            <p class="text-xs text-slate-500">{{ handCount(1) }}枚</p>
          </div>
        </div>
        <div class="border-t border-slate-700 pt-4">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-emerald-500 flex items-center justify-center text-white font-bold text-xs">{{ (nickname || 'U')[0] }}</div>
            <span class="text-sm text-slate-300">{{ nickname }}</span>
            <span class="text-xs text-slate-500">(你)</span>
            <div class="flex gap-1 ml-2">
              <template v-for="m in (myMelds || [])" :key="m[1]">
                <div class="w-7 h-9 rounded text-[10px] flex items-center justify-center bg-slate-700 text-slate-300 font-mono border border-slate-600">{{ tileLabel(m[1]) }}</div>
              </template>
            </div>
          </div>
          <div class="flex flex-wrap gap-1 justify-center">
            <template v-for="(tile, ti) in myHand" :key="ti">
              <button @click="discardTile(tile)" :disabled="!isMyTurn || pendingActions.length > 0"
                class="w-9 h-12 rounded text-xs flex items-center justify-center font-medium transition-all duration-150 hover:scale-110 hover:-translate-y-1 disabled:opacity-80 disabled:hover:scale-100 disabled:hover:translate-y-0"
                :class="['tile-btn', getTileClass(tile), selectedTile === tile ? 'ring-2 ring-cyan-400 scale-110 -translate-y-1' : '']"
                :style="getTileStyle(tile)">{{ tileLabel(tile) }}</button>
            </template>
            <div v-if="myHand.length === 0 && gameStatus === 'playing'" class="text-slate-600 text-xs py-6">手牌为空</div>
          </div>
          <div v-if="isMyTurn && !pendingActions.length" class="flex justify-center gap-2 mt-4">
            <button @click="discardSelected" class="px-4 py-2 bg-cyan-500 text-white rounded-lg text-sm font-medium hover:bg-cyan-400 transition-all" :disabled="!selectedTile">出牌</button>
          </div>
          <div v-else-if="gameStatus === 'waiting'" class="flex justify-center mt-4">
            <button @click="sendReady" class="px-6 py-2.5 bg-gradient-to-r from-emerald-500 to-cyan-500 text-white font-medium rounded-xl hover:from-emerald-400 hover:to-cyan-400 transition-all text-sm">准备</button>
          </div>
        </div>
        <div v-if="gameOver" class="absolute inset-0 bg-slate-900/90 rounded-2xl flex items-center justify-center z-10">
          <div class="text-center">
            <div class="text-4xl mb-3">{{ gameOver.winner === myPid ? '🏆' : '😞' }}</div>
            <h3 class="text-2xl font-bold text-white mb-2">{{ gameOver.winner === myPid ? '你赢了！' : gameOver.winner_nickname + ' 赢了' }}</h3>
            <p class="text-slate-400 text-sm mb-6">胡牌: {{ gameOver.win_tile }}</p>
            <button @click="goToLobby" class="px-6 py-2.5 bg-slate-700 text-white rounded-xl hover:bg-slate-600 transition-all text-sm">返回大厅</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'

const nickname = ref(localStorage.getItem('mahjong_nickname') || '')
const roomIdInput = ref('')
const error = ref('')
const room = ref(null)
const roomId = ref('')
const ws = ref(null)
const gameState = ref(null)
const myPid = ref(-1)
const myHand = ref([])
const myMelds = ref([])
const onlinePlayers = ref({})
const currentTurn = ref(-1)
const lastDiscardTile = ref(null)
const discards = ref([])
const pendingActions = ref([])
const selectedTile = ref(null)
const gameOver = ref(null)
const gameStatus = ref('waiting')

const isMyTurn = computed(() => currentTurn.value === myPid.value)

const TILE_BG = {
  w: 'bg-gradient-to-b from-red-50 to-red-100 border-red-200 text-red-700',
  t: 'bg-gradient-to-b from-emerald-50 to-emerald-100 border-emerald-200 text-emerald-700',
  s: 'bg-gradient-to-b from-amber-50 to-amber-100 border-amber-200 text-amber-700',
  honor: 'bg-gradient-to-b from-slate-100 to-slate-200 border-slate-300 text-slate-700',
}
const SUIT_CN = { w: '万', t: '筒', s: '条' }
const NUM_CN = ['一','二','三','四','五','六','七','八','九']
const HONOR_LABEL = { dong: '东', nan: '南', xi: '西', bei: '北', zhong: '中', fa: '发', bai: '白' }

function getTileClass(tile) {
  if (['dong','nan','xi','bei','zhong','fa','bai'].includes(tile)) return TILE_BG.honor
  return TILE_BG[tile[0]] || TILE_BG.honor
}
function getTileStyle(tile) {
  return { borderWidth: '1px', borderStyle: 'solid' }
}
function tileLabel(tile) {
  if (tile in HONOR_LABEL) return HONOR_LABEL[tile]
  const s = tile[0], n = parseInt(tile[1])
  return NUM_CN[n-1] + SUIT_CN[s]
}
function actionLabel(act) {
  return { hu: '胡牌', pung: '碰', kong: '杠', pass: '过' }[act] || act
}
function handCount(pid) {
  const p = onlinePlayers.value[pid]
  if (!p) return 0
  return p.hand_len ?? 0
}

function apiBase() {
  const loc = window.location
  if (loc.hostname === 'localhost' || loc.hostname === '127.0.0.1') return 'http://localhost:8001/api/v1'
  return '/api/v1'
}
function wsBase() {
  const loc = window.location
  if (loc.hostname === 'localhost' || loc.hostname === '127.0.0.1') return 'ws://localhost:8001'
  const proto = loc.protocol === 'https:' ? 'wss:' : 'ws:'
  return proto + '//' + loc.host
}

async function createRoom() {
  if (!nickname.value.trim()) { error.value = '请输入昵称'; return }
  localStorage.setItem('mahjong_nickname', nickname.value.trim())
  error.value = ''
  try {
    const res = await fetch(apiBase() + '/game/room/create', { method: 'POST' })
    const data = await res.json()
    roomIdInput.value = data.room_id
    joinRoom()
  } catch(e) { error.value = '创建房间失败: ' + e.message }
}

async function joinRoom() {
  if (!nickname.value.trim()) { error.value = '请输入昵称'; return }
  if (!roomIdInput.value.trim()) { error.value = '请输入房间号'; return }
  localStorage.setItem('mahjong_nickname', nickname.value.trim())
  error.value = ''
  roomId.value = roomIdInput.value.trim().toUpperCase()
  connectWebSocket()
}

function connectWebSocket() {
  const url = wsBase() + '/api/v1/ws/game/' + roomId.value
  const socket = new WebSocket(url)
  ws.value = socket
  room.value = {}
  socket.onopen = () => {
    socket.send(JSON.stringify({ type: 'join', nickname: nickname.value.trim() }))
  }
  socket.onmessage = (e) => { handleMessage(JSON.parse(e.data)) }
  socket.onclose = () => { if (room.value) { error.value = '连接已断开' }; ws.value = null }
  socket.onerror = () => { error.value = '连接错误' }
}

function handleMessage(msg) {
  switch (msg.type) {
    case 'joined':
    myPid.value = msg.pid
    onlinePlayers.value[msg.pid] = { nickname: nickname.value, hand_len: 0, melds: [], ready: false }
    break
    case 'existing_players':
    for (const p of msg.players) {
        if (!onlinePlayers.value[p.pid])
            onlinePlayers.value[p.pid] = { nickname: p.nickname, hand_len: 0, melds: [], ready: p.ready }
    }
    break
case 'player_joined':
      if (!onlinePlayers.value[msg.pid]) onlinePlayers.value[msg.pid] = { nickname: msg.nickname, hand_len: 0, melds: [] }
      break
    case 'game_start':
      gameStatus.value = 'playing'
      myPid.value = msg.your_seat
      myHand.value = msg.hand
      myMelds.value = []
      currentTurn.value = msg.dealer
      lastDiscardTile.value = null
      discards.value = []
      pendingActions.value = []
      gameOver.value = null
      for (const p of msg.players) onlinePlayers.value[p.pid] = { nickname: p.nickname, hand_len: p.hand_len, melds: [] }
      break
    case 'your_turn': currentTurn.value = myPid.value; break
    case 'draw': myHand.value = msg.hand; break
    case 'player_drew':
      if (onlinePlayers.value[msg.pid]) onlinePlayers.value[msg.pid].hand_len += 1
      break
    case 'discard':
      if (msg.pid === myPid.value) myHand.value = msg.hand
      lastDiscardTile.value = msg.tile
      discards.value.push(msg.tile)
      if (msg.pid !== myPid.value && onlinePlayers.value[msg.pid])
        onlinePlayers.value[msg.pid].hand_len = Math.max(0, (onlinePlayers.value[msg.pid].hand_len || 0) - 1)
      currentTurn.value = -1
      break
    case 'action_prompt':
      pendingActions.value = msg.actions
      break
    case 'action_result':
      pendingActions.value = []
      break
    case 'action_taken':
      currentTurn.value = msg.pid
      if (msg.action === 'pung' || msg.action === 'kong') {
        if (onlinePlayers.value[msg.pid]) {
          onlinePlayers.value[msg.pid].hand_len = Math.max(0, (onlinePlayers.value[msg.pid].hand_len || 0) - (msg.action === 'pung' ? 2 : 3))
          if (!onlinePlayers.value[msg.pid].melds) onlinePlayers.value[msg.pid].melds = []
          onlinePlayers.value[msg.pid].melds.push([msg.action, msg.tile, msg.from_pid])
        }
      }
      pendingActions.value = []
      break
    case 'game_over':
      gameOver.value = msg
      gameStatus.value = 'over'
      if (msg.winner === myPid.value) myHand.value = msg.hand
      pendingActions.value = []
      break
    case 'draw_standoff':
      gameStatus.value = 'over'
      break
    case 'error':
      error.value = msg.message
      break
  }
}

function discardTile(tile) {
  selectedTile.value = tile
  error.value = ''
  if (isMyTurn.value && !pendingActions.value.length) sendDiscard(tile)
}
function sendDiscard(tile) {
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    ws.value.send(JSON.stringify({ type: 'discard', tile }))
    selectedTile.value = null
  }
}
function discardSelected() { if (selectedTile.value) sendDiscard(selectedTile.value) }
function sendAction(action) {
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    ws.value.send(JSON.stringify({ type: 'action', action }))
    pendingActions.value = []
  }
}
function sendReady() {
  if (ws.value && ws.value.readyState === WebSocket.OPEN)
    ws.value.send(JSON.stringify({ type: 'ready' }))
}
function leaveRoom() { if (ws.value) { ws.value.close(); ws.value = null }; goToLobby() }
function goToLobby() {
  room.value = null; myHand.value = []; myMelds.value = []; onlinePlayers.value = {}
  currentTurn.value = -1; lastDiscardTile.value = null; discards.value = []
  pendingActions.value = []; gameOver.value = null; gameStatus.value = 'waiting'; gameState.value = null
}

onBeforeUnmount(() => { if (ws.value) { ws.value.close(); ws.value = null } })
</script>

<style scoped>
.tile-btn { cursor: pointer; user-select: none; }
.tile-btn:disabled { cursor: default; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.animate-bounce { animation: bounce 0.6s ease infinite; }
</style>
