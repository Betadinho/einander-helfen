<!-- Button to scroll to the top of the page. -->

<template>
  <v-btn
    v-scroll="onScroll"
    v-show="fab"
    fab
    dark
    fixed
    bottom
    right
    color="primary"
    @click="toTop"
  >
    <v-icon x-large>keyboard_arrow_up</v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "ScrollTopButton",
  data: function () {
    return {
      fab: false,
    };
  },
  methods: {
    /**
     * Allows fab to be shown if the user has scrolled down at least 20px.
     */
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
  },
});
</script>
