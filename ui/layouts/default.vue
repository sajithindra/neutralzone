<template>
<v-app index>
    <v-app-bar app color="purple darken-4">
        <NuxtLink to="/" class="text-white p-4 text-2xl font-bold"> Neutral Zone</NuxtLink>
        <v-spacer></v-spacer>
        <NuxtLink to="/services" class="p-2 text-l font-bold hover:bg-fuchsia-500 rounded h-10">Services</NuxtLink>
        <NuxtLink to="/about" class="p-2 text-l font-bold hover:bg-fuchsia-500 rounded h-10">About</NuxtLink>
        <NuxtLink to="/contact" class="p-2 text-l font-bold hover:bg-fuchsia-500 rounded h-10">Contact</NuxtLink>
        <NuxtLink to="/register" class="p-2 text-l font-bold hover:bg-fuchsia-500 rounded h-10">Register</NuxtLink>
    </v-app-bar>
    <v-main>
        <slot/>
    </v-main>
    <v-footer padless>
    <v-col
      class="text-center bg-fuchsia-800 text-white px-10 py-2 text-l"
      cols="12">
      {{ new Date().getFullYear() }} : <strong>Copyright (c) Securekloud Technologies, Ltd. All rights reserved.</strong>
    </v-col>
  </v-footer>
</v-app>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>