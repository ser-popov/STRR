<script setup lang="ts">

const props = defineProps<{ label: string }>()

</script>

<template>
  <div class="flex py-4 text-sm">
    <div class="flex w-1/5 items-start justify-start">
      <span class="text-sm font-bold">{{ props.label }}</span>
    </div>
    <div class="flex-auto">
      <slot />
    </div>
  </div>
</template>

<style scoped></style>
