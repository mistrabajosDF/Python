<template>
    <div class="container_form">
        <div class="volver">
            <router-link to="/"><img src="../assets/images/logo_cuadrado.png" alt="logo" width="60"></router-link>
        </div>
        <div class="formulario">
            <div class="titulo">Iniciar sesión</div>
            <form action="" method="POST" @submit.prevent="handleSubmit">

                <div class="mb-3 input_form">
                    <label for="emailAddress" class="form-label">Email</label>
                    <input type="email" name="user" class="form-control" id="emailAddress" placeholder="Ingresar dirección de mail" v-model="formData.user">
                </div>

                <div class="mb-3 input_form">
                    <label for="password" class="form-label">Contraseña</label>
                    <input type="password" name="password" class="form-control" id="password" placeholder="Ingresar contraseña" v-model="formData.password">
                </div>

                <button @click="sendData" type="submit" class="btn btn-primary button mb-5">Ingresar</button>
            </form>
        </div>
    </div>
</template>

<script>
    import { apiService } from '@/api.js';

    export default {
        name: "LoginView",

        data() {
            return { 
                formData: {
                    user: '',
                    password: ''
                }
            };
        },

        methods: {
            handleSubmit() {
                console.log("Iniciando sesión...");
            },
            
            async sendData() {
                try {
                    const dataToSend = {
                        user: this.formData.user,
                        password: this.formData.password    
                    };
                const response = await apiService.post('/api/auth', dataToSend, {
                headers: { 'Content-Type': 'application/json' },});
                
                //guardo jwt y mail en local storage
                localStorage.setItem('jwt', response.data.token)
                localStorage.setItem('user', this.formData.user)

                alert('Se inició sesión correctamente')
                if(this.formData.user!='')
                    this.$router.push({ name: 'home' });
                } catch (error) {
                    console.error('Error al enviar datos:', error);
                    if(this.formData.user!='')
                        alert('Los datos de inicio de sesión son erróneos')
                }
            },

        },

    }
</script>

<style scoped>
    @media (max-width: 768px) {
        .container_form {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .volver {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
            width: 100%;
        }

        .formulario {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .titulo {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }

        .input_form {
            width: 100%;
            margin-bottom: 1.5rem;
        }

        .button {
            width: 100%;
        }

        img{
            height: 1.8rem !important;
            width: 1.8rem !important;
        }
    }
</style>
