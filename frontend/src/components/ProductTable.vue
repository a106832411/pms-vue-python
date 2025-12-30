<template>
  <div class="layout">
    <form class="panel" @submit.prevent="handleSubmit">
      <div class="panel-header">
        <div>
          <p class="label">Form</p>
          <h2>{{ editingId ? "Update product" : "Add product" }}</h2>
        </div>
        <div class="status" v-if="saving">Saving…</div>
      </div>

      <div class="grid">
        <label class="field">
          <span>Name</span>
          <input v-model="form.name" placeholder="SaaS Plan" required />
        </label>
        <label class="field">
          <span>Price</span>
          <input v-model.number="form.price" type="number" min="0" step="0.01" required />
        </label>
        <label class="field">
          <span>Stock</span>
          <input v-model.number="form.stock" type="number" min="0" step="1" required />
        </label>
      </div>

      <label class="field">
        <span>Description</span>
        <textarea v-model="form.description" rows="2" placeholder="Optional" />
      </label>

      <div class="actions">
        <button type="submit" :disabled="saving || !canSubmit" class="primary">
          {{ editingId ? "Save changes" : "Create product" }}
        </button>
        <button type="button" v-if="editingId" @click="resetForm" class="ghost">Cancel edit</button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <div class="panel table-panel">
      <div class="panel-header">
        <div>
          <p class="label">Inventory</p>
          <h2>Products</h2>
        </div>
        <button class="ghost" @click="fetchProducts" :disabled="loading">Refresh</button>
      </div>

      <div v-if="loading" class="state">Loading…</div>
      <div v-else-if="!products.length" class="state">No products yet</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.name }}</td>
            <td>${{ product.price.toFixed(2) }}</td>
            <td>{{ product.stock }}</td>
            <td class="muted">{{ product.description || "—" }}</td>
            <td class="actions-cell">
              <button class="ghost" @click="startEdit(product)">Edit</button>
              <button class="danger" @click="remove(product.id)" :disabled="saving">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, computed } from "vue";
import axios from "axios";
import type { Product, ProductPayload } from "../types";

const api = axios.create({ baseURL: "/api" });

const products = ref<Product[]>([]);
const loading = ref(false);
const saving = ref(false);
const error = ref<string | null>(null);
const editingId = ref<number | null>(null);

const form = reactive<ProductPayload>({
  name: "",
  price: 0,
  stock: 0,
  description: "",
});

const canSubmit = computed(() => form.name.trim().length > 0 && form.price >= 0 && form.stock >= 0);

const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  try {
    const { data } = await api.get<Product[]>("/products");
    products.value = data;
  } catch (err) {
    error.value = "Unable to load products";
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  if (!canSubmit.value) return;
  saving.value = true;
  error.value = null;
  try {
    if (editingId.value) {
      const { data } = await api.put<Product>(`/products/${editingId.value}`, form);
      products.value = products.value.map((p) => (p.id === data.id ? data : p));
    } else {
      const { data } = await api.post<Product>("/products", form);
      products.value = [...products.value, data];
    }
    resetForm();
  } catch (err) {
    error.value = "Save failed";
  } finally {
    saving.value = false;
  }
};

const startEdit = (product: Product) => {
  editingId.value = product.id;
  form.name = product.name;
  form.price = product.price;
  form.stock = product.stock;
  form.description = product.description || "";
};

const resetForm = () => {
  editingId.value = null;
  form.name = "";
  form.price = 0;
  form.stock = 0;
  form.description = "";
};

const remove = async (id: number) => {
  saving.value = true;
  error.value = null;
  try {
    await api.delete(`/products/${id}`);
    products.value = products.value.filter((p) => p.id !== id);
    if (editingId.value === id) resetForm();
  } catch (err) {
    error.value = "Delete failed";
  } finally {
    saving.value = false;
  }
};

onMounted(fetchProducts);
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 20px;
}

@media (max-width: 960px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

.panel {
  background: #f8fafc;
  border-radius: 14px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}

.table-panel {
  background: #fff;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
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
  margin: 2px 0 0;
  font-size: 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #0f172a;
  font-weight: 600;
}

input,
textarea {
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  padding: 10px 12px;
  font-size: 14px;
  font-family: inherit;
  background: #fff;
}

textarea {
  resize: vertical;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

button {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.primary {
  background: linear-gradient(120deg, #2563eb, #0ea5e9);
  color: #fff;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
}

.ghost {
  background: #e2e8f0;
  color: #0f172a;
}

.danger {
  background: #fee2e2;
  color: #b91c1c;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid #e2e8f0;
}

th {
  color: #475569;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.muted {
  color: #475569;
}

.actions-cell {
  display: flex;
  gap: 8px;
}

.state {
  padding: 20px;
  color: #475569;
}

.error {
  margin-top: 10px;
  color: #b91c1c;
  font-weight: 600;
}

.status {
  color: #475569;
  font-weight: 600;
}
</style>
