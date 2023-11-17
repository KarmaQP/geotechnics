<template>
  <the-navigation></the-navigation>
  <main>
    <router-view></router-view>
  </main>
</template>

<script>
import TheNavigation from './components/nav/TheNavigation.vue';

export default {
  components: {
    TheNavigation,
  },
};
</script>

<style>
* {
  padding: 0;
  margin: 0;
  border: 0;
}
*,
*:before,
*:after {
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
}
:focus,
:active {
  outline: none;
}
a:focus,
a:active {
  outline: none;
}

nav,
footer,
header,
aside {
  display: block;
}

html,
body {
  height: 100%;
  width: 100%;
  font-size: 100%;
  line-height: 1;
  font-size: 1.4rem;
  -ms-text-size-adjust: 100%;
  -moz-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
}
input,
button,
textarea {
  font-family: inherit;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input::-ms-clear {
  display: none;
}
button {
  cursor: pointer;
}
button::-moz-focus-inner {
  padding: 0;
  border: 0;
}
a,
a:visited {
  text-decoration: none;
}
a:hover {
  text-decoration: none;
}
ul li,
ol li,
li {
  list-style: none;
}
img {
  vertical-align: top;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-size: inherit;
  font-weight: 400;
}

html {
  font-size: 62.5%;
  overflow-x: hidden;
}

/*
- Font sizes (px)
10 / 12 / 14 / 16 / 18 / 20 / 24 / 30 / 36 / 44 / 52 / 62 / 74 / 86 / 98

- Spacing system (px)
2 / 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 80 / 96 / 128
*/

/*-------------------------------------------------------*/

@font-face {
  font-family: 'Century Gothic';
  src: url('./assets/fonts/centurygothic.ttf');
}

body {
  font-family: 'Century Gothic';
}

.tooltip {
  font-family: 'helvetica neue', helvetica, arial, sans-serif;
  position: absolute;

  width: auto;
  height: auto;
  background: none repeat scroll 0 0 lightblue;
  border: 0 none;
  border-radius: 8px 8px 8px 8px;
  box-shadow: -3px 3px 15px #888888;
  color: blue;
  font: 12px sans-serif;
  padding: 5px;
  text-align: center;
}

table {
  border-collapse: collapse;
}
th {
  color: #ffffff;
  background-color: #000000;
  margin-right: 10px;
}
td {
  background-color: #cccccc;
}
thead {
  display: none;
}
tr {
  display: flex;
  gap: 0.8rem;
  background-color: #000000;
}
table,
th,
td {
  font-family: Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
</style>
