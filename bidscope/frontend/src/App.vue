<template>
  <div class="page">
    <header class="hero">
      <div>
        <p class="eyebrow">BidScope / 标讯罗盘</p>
        <h1>一句话完成多源标讯检索、证据去重与 Word 交付</h1>
        <p class="subtitle">Vue 3 + FastAPI 工程雏形；AI 只做语义理解，事实字段、去重、增量和报告由确定性程序完成。</p>
      </div>
      <div class="badge">Demo</div>
    </header>

    <section class="panel ask-panel">
      <label>自然语言需求</label>
      <textarea v-model="query" rows="3" placeholder="最近3个月上海服务器与算力招标，请每天9:00汇总发送给我"></textarea>
      <div class="actions">
        <button @click="submit" :disabled="loading">{{ loading ? '运行中...' : '开始检索' }}</button>
        <button class="ghost" @click="query='最近一个月安徽充电站和AI基础设施招标'">填入安徽示例</button>
      </div>
    </section>

    <section v-if="sources.length" class="grid">
      <div class="card" v-for="s in sources" :key="s.source_id">
        <strong>{{ s.source_name }}</strong>
        <span>{{ s.tier }} · {{ s.access_status }}</span>
        <p>{{ s.note }}</p>
      </div>
    </section>

    <section v-if="result" class="panel">
      <div class="section-title">
        <h2>结构化意图</h2>
        <span class="status">{{ result.status }}</span>
      </div>
      <div class="intent-grid">
        <div><b>主题</b><span>{{ result.intent.topic }}</span></div>
        <div><b>地区</b><span>{{ result.intent.regions.join('、') }}</span></div>
        <div><b>时间</b><span>{{ fmtDate(result.intent.start_at) }} 至 {{ fmtDate(result.intent.end_at) }}</span></div>
        <div><b>频率</b><span>{{ result.intent.schedule_text || '一次性查询' }}</span></div>
      </div>
      <p v-if="result.intent.clarification_questions.length" class="warn">{{ result.intent.clarification_questions.join('；') }}</p>
    </section>

    <section v-if="result" class="panel">
      <div class="section-title">
        <h2>来源计划</h2>
      </div>
      <table>
        <thead><tr><th>来源</th><th>证据等级</th><th>访问状态</th><th>模式</th></tr></thead>
        <tbody>
          <tr v-for="p in result.source_plan" :key="p.source_id">
            <td>{{ p.source_name }}</td><td>{{ p.tier }}</td><td>{{ p.access_status }}</td><td>{{ p.mode }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="result" class="panel">
      <div class="section-title">
        <h2>标讯结果</h2>
        <a v-if="result.report_download_url" class="download" :href="reportUrl(result.report_download_url)">下载 Word</a>
      </div>
      <div class="stats">
        <span>新增 {{ result.notices.length }} 条</span>
        <span>去重 {{ result.duplicate_count }} 条</span>
        <span>受限字段 {{ result.restricted_count }} 条</span>
      </div>
      <div class="notice" v-for="n in result.notices" :key="n.id">
        <div class="notice-head">
          <h3>{{ n.title }}</h3>
          <span :class="['tier', n.source_tier.startsWith('T0') ? 't0' : 't2']">{{ n.source_tier }}</span>
        </div>
        <p>{{ n.core_content }}</p>
        <div class="meta">
          <span>{{ n.region }}</span>
          <span>{{ fmtDate(n.published_at) }}</span>
          <span>{{ n.notice_stage }}</span>
          <span>相关性 {{ n.relevance_score }}</span>
        </div>
        <p class="reason">{{ n.relevance_reason }}</p>
        <p v-if="n.restricted_fields.length" class="warn">受限字段：{{ n.restricted_fields.join('、') }}。系统未尝试恢复。</p>
        <a :href="n.source_url" target="_blank">查看来源链接</a>
      </div>
    </section>

    <section v-if="result" class="panel log">
      <h2>运行日志</h2>
      <p v-for="m in result.messages" :key="m">{{ m }}</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { createRun, getSources, reportUrl } from './api'

const query = ref('最近3个月上海服务器与算力招标，请每天9:00汇总发送给我')
const loading = ref(false)
const result = ref<any>(null)
const sources = ref<any[]>([])

onMounted(async () => {
  sources.value = await getSources()
})

async function submit() {
  loading.value = true
  try {
    result.value = await createRun(query.value)
  } finally {
    loading.value = false
  }
}

function fmtDate(value: string) {
  return new Date(value).toLocaleString('zh-CN', { hour12: false })
}
</script>
