<template>
  <div class="max-w-3xl mx-auto p-6 space-y-4">
    <h1 class="text-2xl font-semibold">Addresses</h1>
    <form class="grid grid-cols-2 gap-2" @submit.prevent="create">
      <input class="input" v-model="f.street" placeholder="Street" />
      <input class="input" v-model="f.city" placeholder="City" />
      <input class="input" v-model="f.state" placeholder="State" />
      <input class="input" v-model="f.postal_code" placeholder="Postal Code" />
      <input class="input" v-model="f.phone_number" placeholder="Phone (+989... or 09...)" />
      <button class="btn col-span-2">Add</button>
    </form>
    <div class="divide-y border rounded">
      <div v-for="a in items" :key="a.id" class="p-3">
        <form v-if="editing === a.id" class="grid grid-cols-2 gap-2" @submit.prevent="update(a.id)">
          <input class="input col-span-2" v-model="editForm.street" placeholder="Street" />
          <input class="input" v-model="editForm.city" placeholder="City" />
          <input class="input" v-model="editForm.state" placeholder="State" />
          <input class="input" v-model="editForm.postal_code" placeholder="Postal Code" />
          <input class="input" v-model="editForm.phone_number" placeholder="Phone" />
          <div class="col-span-2 flex gap-2">
            <button type="submit" class="btn flex-1">Save</button>
            <button type="button" class="btn-cancel flex-1" @click="editing = null">Cancel</button>
          </div>
        </form>
        
        <div v-else class="flex items-center justify-between">
          <div>
            <div class="font-medium">{{ a.street }}, {{ a.city }}</div>
            <div class="text-sm text-gray-600">{{ a.state }} {{ a.postal_code }} • {{ a.phone_number }}</div>
          </div>
          <div class="flex items-center gap-2">
            <button class="text-sm px-2 py-1 border rounded" @click="startEdit(a)">Edit</button>
            <button class="text-sm px-2 py-1 border rounded" @click="setDefault(a.id)" :disabled="a.is_default">
              {{ a.is_default ? 'Default' : 'Set default' }}
            </button>
            <button class="text-sm px-2 py-1 border rounded text-red-600" @click="remove(a.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api from '../utils/http'

const items = ref<any[]>([])
const editing = ref<number | null>(null)
const f = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '' })
const editForm = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '' })

async function load() {
  const { data } = await api.get('/api/addresses/')
  items.value = data.results || data
}
async function create() {
  await api.post('/api/addresses/', f)
  Object.assign(f, { street: '', city: '', state: '', postal_code: '', phone_number: '' })
  await load()
}
async function remove(id: number) {
  await api.delete(`/api/addresses/${id}/`)
  await load()
}
async function setDefault(id: number) {
  await api.post(`/api/addresses/${id}/set-default/`)
  await load()
}

function startEdit(address: any) {
  editing.value = address.id
  editForm.street = address.street
  editForm.city = address.city
  editForm.state = address.state
  editForm.postal_code = address.postal_code
  editForm.phone_number = address.phone_number
}

async function update(id: number) {
  await api.patch(`/api/addresses/${id}/`, editForm)
  editing.value = null
  await load()
}

onMounted(load)
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2; }
.btn { @apply bg-black text-white rounded px-3 py-2; }
.btn-cancel { @apply bg-gray-200 text-gray-800 rounded px-3 py-2 hover:bg-gray-300; }
</style>


