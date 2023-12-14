<template>
  <div class="generated-table material">
    <div class="tr">
      <div class="td">
        <input
          type="text"
          name=""
          id=""
          placeholder="Введите наименование..."
        />
      </div>
      <div class="td">
        <input type="text" name="" id="" placeholder="Введите цвет..." />
      </div>
      <div class="td">
        <input type="text" name="" id="" placeholder="Введите комментарий..." />
      </div>
      <div class="td list-geometry" @click="$emit('toggle-modal', id)">
        {{ primitives }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  emits: ['toggle-modal'],
  props: ['id', 'selectedPrimitives'],
  computed: {
    primitives() {
      let str = '';
      const lastEl = this.selectedPrimitives.at(-1);

      this.selectedPrimitives.forEach((primitive, i) => {
        if (primitive !== lastEl) str += primitive + ', ';
        else str += primitive;
      });
      return str;
    },
  },
};
</script>

<style scoped>
.list-geometry {
  cursor: pointer;
}
</style>
