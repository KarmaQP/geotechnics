<template>
  <div class="generated-table material">
    <div class="tr">
      <div class="td">{{ materialName }}</div>
      <div class="td">{{ materialColor }}</div>
      <div class="td">{{ materialComment }}</div>
      <div class="td">
        <textarea
          type="text"
          name=""
          id=""
          placeholder="Введите текст"
          :value="materialNote"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['materialName', 'materialColor', 'materialComment', 'materialNote'],
};
</script>
