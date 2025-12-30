<template>
    <main class="page">
        <header class="hero">
            <div>
                <p class="eyebrow">TMS Console</p>
                <h1>运单管理</h1>
                <p class="lede">创建、查询、更新、删除运单，支持状态与费用记录，后端 FastAPI。</p>
            </div>
            <el-tag type="info" effect="dark">Local-only</el-tag>
        </header>
        <el-card class="card" shadow="hover" body-style="padding: 0; height: 100%;">
            <ShipmentTable />
        </el-card>
    </main>
</template>

<script setup lang="ts">
import { ElCard, ElTag } from "element-plus";
import ShipmentTable from "./components/ShipmentTable.vue";
</script>

<style scoped>
.page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px 16px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow: hidden;
}

.hero {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    padding: 12px 4px;
}

.eyebrow {
    letter-spacing: 0.08em;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 8px;
}

h1 {
    margin: 0 0 8px;
    font-size: 30px;
}

.lede {
    margin: 0;
    color: #475569;
}

.card {
    flex: 1;
    overflow: hidden;
    border-radius: 16px;
}
</style>
