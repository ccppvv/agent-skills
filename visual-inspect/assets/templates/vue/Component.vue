<template>
  <div :class="['container', variant]">
    <h2 class="title">{{ title }}</h2>
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  variant: {
    type: String,
    default: 'default'
  }
});
</script>

<style scoped>
.container {
  --padding: var(--spacing-md);
  --radius: var(--radius-md);

  padding: var(--padding);
  border-radius: var(--radius);
  background: var(--color-surface);
}

.title {
  font: var(--font-heading);
  color: var(--color-text);
  margin-bottom: var(--spacing-sm);
}

@media (max-width: 640px) {
  .container {
    --padding: var(--spacing-sm);
  }
}
</style>
