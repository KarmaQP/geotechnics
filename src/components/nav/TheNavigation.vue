<template>
  <header>
    <nav>
      <ul>
        <li>
          <router-link to="/page1">Расчетная схема</router-link>
        </li>
        <li>
          <router-link :class="disabledLink" to="/page2"
            >Расчетные свойства</router-link
          >
        </li>
        <li>
          <router-link :class="disabledLink" to="/page3"
            >Характеристики материалов</router-link
          >
        </li>
        <li>
          <router-link :class="disabledLink" to="/page4"
            >Расчетные этапы</router-link
          >
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['gmshData']),
    disabledLink() {
      if (!this.gmshData) return 'disabled-link';
      else return '';
    },
  },
};
</script>

<style scoped>
header {
  width: 100%;
  height: 5rem;
  background-color: #11005c;
}

nav {
  height: 100%;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

li {
  margin: 0 2rem;
}

a {
  text-decoration: none;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  color: white;
  padding: 0.5rem 1.5rem;
  display: inline-block;
}

a:hover,
a:active,
a.active {
  color: #f1a80a;
  border-color: #f1a80a;
  background-color: #1a037e;
}

.disabled-link {
  pointer-events: none;
  color: var(--grey-text-color);
}
</style>
