<template>
    <nav class="navbar navbar-expand-lg custom-navbar fixed-top">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">
                <img class="logo" src="@/assets/images/logo_cuadrado.png" alt="logo" width="50" height="50"/>
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarText">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/" class="nav-link">Inicio</router-link>
                    </li>

                    <li  class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false" >Servicios</a>
                        <ul class="dropdown-menu">
                            <li>
                                <router-link to="/services" class="dropdown-item">Ver todos</router-link>
                            </li>
                            <li v-if="isUserInLocalStorage">
                                <router-link to="/service_requests" class="dropdown-item ">Solicitudes</router-link>
                            </li>
                        </ul>
                    </li>
                    <li class="nav-item" v-if="isUserInLocalStorage">
                        <router-link to="/statistics" class="nav-link">Estadisticas</router-link>
                    </li>
                    
                    <li class="nav-item">
                        <button @click="redirigirRegistro" class="btn active btn-custom" v-if="!isUserInLocalStorage">Registrarme</button>
                    </li>
                    <li class="nav-item">
                        <router-link to="/login" class="btn active btn-custom" v-if="!isUserInLocalStorage">Iniciar sesión</router-link>
                    </li>
                    <li class="nav-item">
                        <button @click="cerrarSesion" class="btn active btn-custom" v-if="isUserInLocalStorage">Cerrar sesión</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: 'AppHeader',

        computed: {
            isUserInLocalStorage() {
                return localStorage.getItem('user') !== null;
            }   
        },

        data() {
            return {
                isLogged: false,
                userEmail: null,
            };
        },

        methods: {
            redirigirRegistro() {
                window.location.href = 'https://admin-grupo22.proyecto2023.linti.unlp.edu.ar/register?source=app-vue';
                //window.location.href = 'http://localhost:5000/register?source=app-vue';
            },
            cerrarSesion(){
                //remuevo del local storage el jwt y mail
                localStorage.removeItem('jwt');
                localStorage.removeItem('user');

                this.$router.push({ name: 'login' });
            }
        },

    };
</script>