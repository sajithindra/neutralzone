<template>
<v-app index>
    <v-app-bar app color="transparent" elevation="0">
        <NuxtLink to="/" class="text-white px-20 m-4 text-2xl font-bold " > Neutral Zone</NuxtLink>
        <v-spacer></v-spacer>
        <NuxtLink to="/services" class="p-4 m-4 text-l text-white font-bold hover:bg-fuchsia-500 rounded ">Services</NuxtLink>
        <NuxtLink to="/about" class="p-4 m-4 text-l text-white font-bold hover:bg-fuchsia-500 rounded ">About</NuxtLink>
        <NuxtLink to="/contact" class="p-4 m-4 text-l text-white font-bold hover:bg-fuchsia-500 rounded ">Contact</NuxtLink>
        <NuxtLink to="/register" class="py-10 m-4 text-l text-white font-bold hover:bg-fuchsia-500 rounded ">Register</NuxtLink>

    </v-app-bar>
    <v-main class="bg-fuchsia-800">
        <slot/>
    </v-main>
 
</v-app>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>