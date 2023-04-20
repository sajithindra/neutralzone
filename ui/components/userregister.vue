<template>
        <v-container style="width: 40%; padding-top: 5% ;">
                <h1 class="text-center text-white p-3 font-bold text-2xl">User Registration</h1>
                <v-form>
                    <v-text-field label="Name" v-model="name" :rules="[rules.required,rules.name]" variant="underlined"></v-text-field>
                    <v-text-field label="Email" v-model="email" :rules="[rules.required,rules.email]" variant="underlined"></v-text-field>
                    <v-text-field label="Password" v-model="password" type="password" :rules="[rules.required,rules.password]" variant="underlined"></v-text-field>
                    <v-container style="width: 50%;" class="text-center">
                        <v-btn @click="signin()" text  class="w-40 h-20">Register</v-btn>
                    </v-container>
                </v-form>
        </v-container>
</template>

<script setup>
const router = useRouter()
const name = ref("")
const email = ref("")
const password= ref("")
let rules = {
    required : v => !!v || "required",
    name : v => (v.match(/^[a-zA-Z\. ]+$/)) || "Please check name",
    email : v => (v.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)) || "Please use proper format for email",
    password:v => (v.length>=8) || "Minimun 8 charectors required"
}
async function signin() {
    let url = "http://127.0.0.1:8000/user"
    let udata = { 
        name: name.value,
        email: email.value,
        password: password.value
    }
    const {data,pending,error, refresh}=await useAsyncData ( 'userregistration',() =>  $fetch(url,{
        method:'POST',body: udata
    }))
    if (data.value.status == 200){
        router.push({path:'/'})
    }

}

</script>

<style lang="scss" scoped>

</style>