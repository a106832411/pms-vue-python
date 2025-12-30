<template>
    <div class="table-shell">
        <div class="toolbar">
            <div>
                <p class="label">运单列表</p>
                <h2>全部运单</h2>
            </div>
            <div class="header-actions">
                <el-button type="primary" @click="openCreate">新建运单</el-button>
                <el-button @click="fetchShipments" :loading="loading">刷新</el-button>
            </div>
        </div>

        <el-card class="table-card" shadow="never" body-style="padding: 0; height: 100%;">
            <el-table :data="shipments" :max-height="tableHeight" border stripe v-loading="loading"
                header-cell-class-name="table-header" empty-text="暂无数据">
                <el-table-column prop="tracking_number" label="运单号" width="160" />
                <el-table-column label="状态" width="120">
                    <template #default="{ row }">
                        <el-tag :type="statusType[row.status]" effect="light">{{ statusLabel[row.status] }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="路线" min-width="200">
                    <template #default="{ row }">
                        {{ row.origin }} → {{ row.destination }}
                    </template>
                </el-table-column>
                <el-table-column prop="carrier" label="承运商" width="120" />
                <el-table-column prop="weight_kg" label="重量(kg)" width="110" />
                <el-table-column label="费用" width="120">
                    <template #default="{ row }">¥{{ row.cost.toFixed(2) }}</template>
                </el-table-column>
                <el-table-column label="发货 / 收货" min-width="180">
                    <template #default="{ row }">{{ row.shipper }} / {{ row.consignee }}</template>
                </el-table-column>
                <el-table-column label="操作" width="160" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link size="small" @click="startEdit(row)">编辑</el-button>
                        <el-button type="danger" link size="small" :loading="saving"
                            @click="remove(row.id)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <div class="pagination">
            <el-pagination background layout="sizes, prev, pager, next, jumper, total" :current-page="page"
                :page-size="pageSize" :page-sizes="pageSizes" :total="total" @size-change="handleSizeChange"
                @current-change="handleCurrentChange" />
        </div>

        <el-dialog v-model="showModal" :title="editingId ? '更新运单' : '创建运单'" width="760px" destroy-on-close>
            <el-form :model="form" label-width="96px" status-icon>
                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="运单号" required>
                            <el-input v-model="form.tracking_number" placeholder="TMS-2024-001" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="承运商">
                            <el-input v-model="form.carrier" placeholder="SF Express" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="发货方" required>
                            <el-input v-model="form.shipper" placeholder="深圳仓" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="收货方" required>
                            <el-input v-model="form.consignee" placeholder="上海客户" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="起点" required>
                            <el-input v-model="form.origin" placeholder="深圳" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="目的地" required>
                            <el-input v-model="form.destination" placeholder="上海" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="件数" required>
                            <el-input-number v-model="form.pieces" :min="1" :max="999" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="重量(kg)">
                            <el-input-number v-model="form.weight_kg" :min="0" :step="0.1" :precision="2" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="费用">
                            <el-input-number v-model="form.cost" :min="0" :step="1" :precision="2" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="状态">
                            <el-select v-model="form.status" placeholder="选择状态">
                                <el-option v-for="s in statuses" :key="s" :label="statusLabel[s]" :value="s" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="提货日期">
                            <el-date-picker v-model="form.pickup_date" type="date" value-format="YYYY-MM-DD"
                                placeholder="选择日期" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="预计送达">
                            <el-date-picker v-model="form.expected_delivery" type="date" value-format="YYYY-MM-DD"
                                placeholder="选择日期" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="12">
                    <el-col :span="12">
                        <el-form-item label="送达时间">
                            <el-date-picker v-model="form.delivered_at" type="date" value-format="YYYY-MM-DD"
                                placeholder="选择日期" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="备注">
                            <el-input v-model="form.notes" type="textarea" :rows="3" placeholder="可填写特殊要求或异常" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="closeModal">取消</el-button>
                    <el-button type="primary" :loading="saving" :disabled="!canSubmit" @click="handleSubmit">
                        {{ editingId ? "保存修改" : "创建运单" }}
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import axios from "axios";
import type { Shipment, ShipmentPayload, ShipmentStatus, ShipmentList } from "../types";

const api = axios.create({ baseURL: "/api" });
const statuses: ShipmentStatus[] = ["created", "in_transit", "delivered", "canceled"];
const statusLabel: Record<ShipmentStatus, string> = {
    created: "已创建",
    in_transit: "运输中",
    delivered: "已送达",
    canceled: "已取消",
};
const statusType: Record<ShipmentStatus, "info" | "warning" | "success" | "danger"> = {
    created: "info",
    in_transit: "warning",
    delivered: "success",
    canceled: "danger",
};

const shipments = ref<Shipment[]>([]);
const tableHeight = 440;
const loading = ref(false);
const saving = ref(false);
const error = ref<string | null>(null);
const editingId = ref<number | null>(null);
const showModal = ref(false);
const page = ref(1);
const pageSize = ref(10);
const pageSizes = [10, 20, 50];
const total = ref(0);
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)));

const form = reactive<ShipmentPayload>({
    tracking_number: "",
    shipper: "",
    consignee: "",
    origin: "",
    destination: "",
    carrier: "",
    status: "created",
    pieces: 1,
    weight_kg: 0,
    cost: 0,
    pickup_date: "",
    expected_delivery: "",
    delivered_at: "",
    notes: "",
});

const canSubmit = computed(
    () =>
        form.tracking_number.trim().length > 0 &&
        form.shipper.trim().length > 0 &&
        form.consignee.trim().length > 0 &&
        form.origin.trim().length > 0 &&
        form.destination.trim().length > 0 &&
        form.pieces >= 1
);

const fetchShipments = async () => {
    loading.value = true;
    error.value = null;
    try {
        const { data } = await api.get<ShipmentList>("/shipments", {
            params: { limit: pageSize.value, offset: (page.value - 1) * pageSize.value },
        });
        shipments.value = data.items;
        total.value = data.total;
    } catch (err) {
        error.value = "无法加载运单";
    } finally {
        loading.value = false;
    }
};

const normalizeDates = (payload: ShipmentPayload) => {
    const normalized = { ...payload } as Record<string, unknown>;
    ["pickup_date", "expected_delivery", "delivered_at"].forEach((key) => {
        const value = normalized[key];
        if (typeof value === "string" && value.trim() === "") normalized[key] = null;
    });
    return normalized;
};

const handleSubmit = async () => {
    if (!canSubmit.value) return;
    saving.value = true;
    error.value = null;
    const payload = normalizeDates(form);
    try {
        if (editingId.value) {
            await api.put<Shipment>(`/shipments/${editingId.value}`, payload);
        } else {
            await api.post<Shipment>("/shipments", payload);
            page.value = 1;
        }
        await fetchShipments();
        resetForm();
        showModal.value = false;
    } catch (err) {
        error.value = "保存失败";
    } finally {
        saving.value = false;
    }
};

const startEdit = (item: Shipment) => {
    editingId.value = item.id;
    form.tracking_number = item.tracking_number;
    form.shipper = item.shipper;
    form.consignee = item.consignee;
    form.origin = item.origin;
    form.destination = item.destination;
    form.carrier = item.carrier || "";
    form.status = item.status;
    form.pieces = item.pieces;
    form.weight_kg = item.weight_kg;
    form.cost = item.cost;
    form.pickup_date = item.pickup_date || "";
    form.expected_delivery = item.expected_delivery || "";
    form.delivered_at = item.delivered_at ? item.delivered_at.slice(0, 10) : "";
    form.notes = item.notes || "";
    showModal.value = true;
};

const resetForm = () => {
    editingId.value = null;
    form.tracking_number = "";
    form.shipper = "";
    form.consignee = "";
    form.origin = "";
    form.destination = "";
    form.carrier = "";
    form.status = "created";
    form.pieces = 1;
    form.weight_kg = 0;
    form.cost = 0;
    form.pickup_date = "";
    form.expected_delivery = "";
    form.delivered_at = "";
    form.notes = "";
};

const openCreate = () => {
    resetForm();
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    if (!editingId.value) resetForm();
};

const remove = async (id: number) => {
    saving.value = true;
    error.value = null;
    try {
        await api.delete(`/shipments/${id}`);
        const isLastItemOnPage = shipments.value.length === 1 && page.value > 1;
        if (isLastItemOnPage) page.value -= 1;
        await fetchShipments();
        if (editingId.value === id) resetForm();
    } catch (err) {
        error.value = "删除失败";
    } finally {
        saving.value = false;
    }
};

const handleSizeChange = async (size: number) => {
    pageSize.value = size;
    page.value = 1;
    await fetchShipments();
};

const handleCurrentChange = async (current: number) => {
    page.value = current;
    await fetchShipments();
};

onMounted(fetchShipments);
</script>

<style scoped>
.table-shell {
    display: flex;
    flex-direction: column;
    gap: 12px;
    height: 100%;
    overflow: hidden;
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    padding: 10px;
    border-radius: 12px;
}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 4px 4px 0;
}

.label {
    margin: 0;
    color: #475569;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
}

h2 {
    margin: 4px 0 0;
    font-size: 20px;
    font-weight: 800;
}

.header-actions {
    display: flex;
    gap: 8px;
}

.table-card {
    flex: 1;
    overflow: hidden;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.table-header {
    background: #f8fafc;
    color: #475569;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.04em;
}

.pagination {
    display: flex;
    justify-content: flex-end;
    padding: 4px 8px 8px;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}

/* subtle hover for rows */
:deep(.el-table__body tr:hover > td) {
    background: #f1f5f9 !important;
}

/* tighten table header + cells */
:deep(.el-table .cell) {
    padding: 10px 12px;
}

:deep(.el-card__body) {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

:deep(.el-table) {
    flex: 1;
}

/* dialog spacing */
:deep(.el-dialog__body) {
    padding-top: 4px;
}
</style>
