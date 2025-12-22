<template>
  <div class="relative" ref="datePickerRef">
    <div class="relative group">
      <input
        ref="dateInput"
        :value="formattedDate"
        @focus="showPicker = true"
        @blur="handleBlur"
        @click="showPicker = true"
        class="auth-input peer cursor-pointer"
        :placeholder="placeholder"
        readonly
        required
      />
      <div class="input-border"></div>
      <button
        type="button"
        @click="togglePicker"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-emerald-600 hover:text-emerald-700 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <!-- Custom Date Picker Dropdown -->
    <div
      v-if="showPicker"
      class="absolute z-50 mt-2 bg-white rounded-xl shadow-2xl border-2 border-emerald-100 p-4 w-full max-w-sm"
      @click.stop
    >
      <div class="flex items-center justify-between mb-4">
        <button
          type="button"
          @click="previousMonth"
          class="p-2 hover:bg-emerald-50 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="text-center">
          <div class="font-bold text-gray-800">{{ monthNames[currentMonth] }} {{ currentYear }}</div>
        </div>
        <button
          type="button"
          @click="nextMonth"
          class="p-2 hover:bg-emerald-50 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Year Selector -->
      <div class="mb-4 flex items-center justify-center gap-2">
        <button
          type="button"
          @click="previousYear"
          class="p-1 hover:bg-emerald-50 rounded transition-colors"
        >
          <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <select
          v-model.number="currentYear"
          class="px-3 py-1 border border-gray-300 rounded-lg text-sm font-semibold text-gray-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
        <button
          type="button"
          @click="nextYear"
          class="p-1 hover:bg-emerald-50 rounded transition-colors"
        >
          <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Calendar Grid -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div
          v-for="day in dayNames"
          :key="day"
          class="text-center text-xs font-semibold text-gray-500 py-2"
        >
          {{ day }}
        </div>
      </div>
      <div class="grid grid-cols-7 gap-1">
        <div
          v-for="day in daysInMonth"
          :key="day"
          class="text-center"
        >
          <button
            type="button"
            v-if="day"
            @click="selectDate(day)"
            :class="[
              'w-10 h-10 rounded-lg text-sm font-medium transition-all',
              isSelected(day) 
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg' 
                : 'hover:bg-emerald-50 text-gray-700',
              isToday(day) ? 'ring-2 ring-emerald-400' : ''
            ]"
          >
            {{ day }}
          </button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-4 pt-4 border-t border-gray-200 flex gap-2">
        <button
          type="button"
          @click="setToday"
          class="flex-1 px-3 py-2 text-sm font-medium text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
        >
          Today
        </button>
        <button
          type="button"
          @click="clearDate"
          class="flex-1 px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
        >
          Clear
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'

const props = defineProps<{
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const showPicker = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const selectedDate = ref<Date | null>(null)
const datePickerRef = ref<HTMLElement | null>(null)

const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const years = computed(() => {
  const current = new Date().getFullYear()
  const start = current - 100
  const end = current - 13 // Minimum age 13
  return Array.from({ length: end - start + 1 }, (_, i) => start + i).reverse()
})

const formattedDate = computed(() => {
  if (!selectedDate.value) return ''
  const date = selectedDate.value
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const year = date.getFullYear()
  return `${month}/${day}/${year}`
})

const daysInMonth = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  const days = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  const daysArray: (number | null)[] = []
  
  // Add empty cells for days before the first day of the month
  for (let i = 0; i < firstDay; i++) {
    daysArray.push(null)
  }
  
  // Add all days of the month
  for (let i = 1; i <= days; i++) {
    daysArray.push(i)
  }
  
  return daysArray
})

onMounted(() => {
  if (props.modelValue) {
    const date = new Date(props.modelValue)
    if (!isNaN(date.getTime())) {
      selectedDate.value = date
      currentMonth.value = date.getMonth()
      currentYear.value = date.getFullYear()
    }
  }
})

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    const date = new Date(newValue)
    if (!isNaN(date.getTime())) {
      selectedDate.value = date
      currentMonth.value = date.getMonth()
      currentYear.value = date.getFullYear()
    }
  } else {
    selectedDate.value = null
  }
})

function selectDate(day: number) {
  const date = new Date(currentYear.value, currentMonth.value, day)
  selectedDate.value = date
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const dayStr = String(date.getDate()).padStart(2, '0')
  emit('update:modelValue', `${year}-${month}-${dayStr}`)
  showPicker.value = false
}

function isSelected(day: number | null): boolean {
  if (!day || !selectedDate.value) return false
  return (
    selectedDate.value.getDate() === day &&
    selectedDate.value.getMonth() === currentMonth.value &&
    selectedDate.value.getFullYear() === currentYear.value
  )
}

function isToday(day: number | null): boolean {
  if (!day) return false
  const today = new Date()
  return (
    day === today.getDate() &&
    currentMonth.value === today.getMonth() &&
    currentYear.value === today.getFullYear()
  )
}

function previousMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function previousYear() {
  if (currentYear.value > years.value[years.value.length - 1]) {
    currentYear.value--
  }
}

function nextYear() {
  if (currentYear.value < years.value[0]) {
    currentYear.value++
  }
}

function setToday() {
  const today = new Date()
  selectDate(today.getDate())
  currentMonth.value = today.getMonth()
  currentYear.value = today.getFullYear()
}

function clearDate() {
  selectedDate.value = null
  emit('update:modelValue', '')
  showPicker.value = false
}

function togglePicker() {
  showPicker.value = !showPicker.value
}

function handleBlur() {
  // Delay hiding to allow button clicks
  setTimeout(() => {
    showPicker.value = false
  }, 200)
}

function handleClickOutside(event: MouseEvent) {
  if (showPicker.value && datePickerRef.value && !datePickerRef.value.contains(event.target as Node)) {
    showPicker.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.auth-input {
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-transparent focus:outline-none transition-all duration-300 text-gray-900 placeholder:text-gray-400;
}

.input-border {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 transition-all duration-300 rounded-full;
}

.auth-input:focus ~ .input-border {
  @apply w-full h-1;
}
</style>

