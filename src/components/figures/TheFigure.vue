<template>
  <div :id="figureName">
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: ['figureName'],
};
</script>
