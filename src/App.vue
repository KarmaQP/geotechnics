<template>
  <the-navigation></the-navigation>
  <main>
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component"></component>
      </keep-alive>
    </router-view>
  </main>
</template>

<script>
import TheNavigation from './components/nav/TheNavigation.vue';

/* global toastr */

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
  /* overflow-x: hidden; */
}

/*
- Font sizes (px)
10 / 12 / 14 / 16 / 18 / 20 / 24 / 30 / 36 / 44 / 52 / 62 / 74 / 86 / 98

- Spacing system (px)
2 / 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 80 / 96 / 128
*/

/*-------------------------------------------------------*/

:root {
  --bg-color: #fff;
  --blue-bg-color: #3c74d3;
  --hover-blue-bg-color: #3e69b4;
  --active-blue-bg-color: #31548f;
  --light-blue-bg-color: #cfd5ea;
  --very-light-blue-bg-color: #e9ebf5;
  --text-color: #fff;
  --dark-text-color: #000;
  --grey-text-color: #aaa;
  --disabled-color: #8b8b8b;
}

@font-face {
  font-family: 'Century Gothic';
  src: url('./assets/fonts/centurygothic.ttf');
}

@font-face {
  font-family: 'GOST type B';
  src: url('./assets/fonts/gost_type_b.ttf');
}

body {
  font-family: 'GOST type B';
}

section {
  padding: 6.4rem 0;
  max-width: 70rem;
  margin: 0 auto;
}

h1 {
  margin: 0 auto 3.2rem auto;
  max-width: 36rem;
  font-size: 2.4rem !important;
  text-align: center;
  line-height: 1.4;
}

.bubble,
a.bubble:link,
a.bubble:visited {
  background-color: var(--blue-bg-color);
  padding: 0.8rem;
  color: var(--text-color);
  border-radius: 8px;
  border: 1px solid #000;
  transition: all 0.3s ease;
}

a.bubble:hover,
a.bubble:active,
.bubble.btn:hover {
  background-color: var(--hover-blue-bg-color);
}

option,
select {
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

.tr .td .tr .td {
  border: none;
}

.tr .td .tr .td:first-child {
  border-right: 1px solid #000;
}

.tr .td .tr {
  grid-template-columns: 2fr 1fr;
}

.table {
  min-width: 100%;
  background-color: #ccc;
}

.th,
.td {
  padding: 0.4rem;
  line-height: 1.2;
  border: 1px solid #fff;
}

.th {
  background-color: var(--blue-bg-color);
  color: var(--text-color);
  font-size: 1.6rem;
}

.td--h {
  background-color: var(--blue-bg-color);
  color: var(--text-color);
}

.generated-table:nth-child(even),
.tr--multi-row .td:nth-child(odd) {
  background-color: var(--light-blue-bg-color);
}

.generated-table:nth-child(odd),
.tr--multi-row .td:nth-child(even) {
  background-color: var(--very-light-blue-bg-color);
}

.tr .td .tr:nth-child(odd) {
  background-color: var(--light-blue-bg-color);
}

.tr .td .tr:nth-child(even) {
  background-color: var(--very-light-blue-bg-color);
}

input[type='text'],
input[type='number'],
select {
  min-width: 100%;
  background-color: transparent;
}

input[type='text'],
input[type='number'] {
  min-height: 100%;
}

input[type='checkbox'] {
  cursor: pointer;
}

textarea {
  min-width: 100%;
  min-height: 100%;
  background-color: transparent;
  resize: none;
}

#step-num,
#phase-name {
  border: 1px solid #000;
  font-size: 1.6rem;
  border-radius: 8px;
  font-family: inherit;
  margin-right: 1.6rem;
  min-width: 18rem;
  padding: 0.3rem;
}

option {
  font-family: inherit;
}

.disabled__btn {
  cursor: not-allowed;
  pointer-events: none;
  background-color: var(--disabled-color);
}

.two-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.table {
  margin-top: 3.2rem;
}
</style>
