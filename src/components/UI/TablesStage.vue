<template>
  <the-stage stage-name="Фаза инициализации"></the-stage>
  <!-- <the-stage stage-name="Фаза 1"></the-stage> -->
</template>

<script>
import TheStage from './Table/TableStages/TheStage.vue';

export default {
  components: {
    TheStage,
  },
};
</script>

<style scoped>
#fig01 {
  transform: translateX(-13%);
}

select,
option {
  font-family: inherit;
}
</style>
