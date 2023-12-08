<template>
  <teleport to="body">
    <div @click="$emit('close')"></div>
    <dialog open>
      <header>
        <h2>{{ title }}</h2>
      </header>
      <section>
        <slot></slot>
      </section>
      <menu>
        <slot name="action">
          <button type="button" @click="$emit('close')">Закрыть</button>
        </slot>
      </menu>
    </dialog>
  </teleport>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: false,
    },
  },
  emits: ['close'],
};
</script>

<style scoped>
div {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
}

dialog {
  position: fixed;
  top: 10vh;
  min-width: 120rem;
  transform: translateX(-45rem);
  z-index: 100;
  border-radius: 12px;
  border: none;
}

header {
  background-color: var(--blue-bg-color);
  border-radius: 12px 12px 0 0;
  color: white;
  width: 100%;
  padding: 1rem;
}

header h2 {
  margin: 0;
}

section {
  padding: 1rem;
}

menu {
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
  margin: 0;
}

@media (min-width: 768px) {
  dialog {
    left: calc(50% - 20rem);
    width: 40rem;
  }
}
</style>
