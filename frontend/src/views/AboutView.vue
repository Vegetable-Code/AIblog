<template>
  <div class="fade-in-up max-w-3xl mx-auto">
    <div class="text-center py-10 mb-8">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-violet-500/20 flex items-center justify-center mx-auto mb-4">
        <span class="text-2xl font-bold gradient-text">AI</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-bold text-white mb-3 tracking-tight">{{ $t('about.title') }}<span class="gradient-text">本站</span></h1>
      <p class="text-slate-400">{{ $t('about.subtitle') }}</p>
    </div>

    <div class="glass-card rounded-2xl p-8 md:p-10 space-y-6">
      <p class="text-slate-300 leading-relaxed">
        你好！我是本站的作者，一名专注于 <span class="text-cyan-400 font-medium">AI 应用工程</span> 的开发者。
        这里记录了我对深度学习、大语言模型、工程实践和前沿技术的思考与探索。
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-slate-800/40 rounded-xl p-5 border border-slate-700/40">
          <div class="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-3">
            <svg class="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <h3 class="text-white font-medium mb-1">{{ $t('about.full_stack') }}</h3>
          <p class="text-slate-500 text-sm">{{ $t('about.full_stack_desc') }}</p>
        </div>
        <div class="bg-slate-800/40 rounded-xl p-5 border border-slate-700/40">
          <div class="w-8 h-8 rounded-lg bg-violet-500/20 flex items-center justify-center mb-3">
            <svg class="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/></svg>
          </div>
          <h3 class="text-white font-medium mb-1">{{ $t('about.markdown') }}</h3>
          <p class="text-slate-500 text-sm">原生 {{ $t('about.markdown') }} 编辑与渲染</p>
        </div>
        <div class="bg-slate-800/40 rounded-xl p-5 border border-slate-700/40">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center mb-3">
            <svg class="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/></svg>
          </div>
          <h3 class="text-white font-medium mb-1">{{ $t('about.user_system') }}</h3>
          <p class="text-slate-500 text-sm">{{ $t('about.user_system_desc') }}</p>
        </div>
        <div class="bg-slate-800/40 rounded-xl p-5 border border-slate-700/40">
          <div class="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center mb-3">
            <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
          </div>
          <h3 class="text-white font-medium mb-1">{{ $t('about.comments') }}</h3>
          <p class="text-slate-500 text-sm">{{ $t('about.comments_desc') }}</p>
        </div>
      </div>

      <div class="flex flex-wrap gap-3 pt-4">
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">Python</span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">Vue.js</span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">FastAPI</span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">PyTorch</span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">LLM</span>
        <span class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm border border-slate-700">Docker</span>
      </div>
    </div>
  </div>
</template>
