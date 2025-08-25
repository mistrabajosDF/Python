<template>
  <br>
  <br>
  <br>
    <section class="section_cidepint">
        <img id="cidepint_logo" src="@/assets/images/cidepint.jpg" alt="logo cidepint"/>
    </section>
    <center>
    <section class="section_cidep1">
        <img id="cidepint_logo" src="@/assets/images/cidep1.jpg" alt="logo cidepint"/>
    </section>

    <section class="section_cidep1">
        <img id="cidepint_logo" src="@/assets/images/cidep2.jpg" alt="logo cidepint"/>
    </section>
    </center>
    <section class="section_cidepint_lab">
        <div class="info">
            <p>Ingresando a tu cuenta, desde la sección Servicios, podrás:</p>
            <ul>
                <li>Buscar servicios</li>
                <li>Lista servicios prestados por instituciones</li>
                <li>Iniciar solicitudes de servicios</li>
            </ul>
            <p>Para más información contactanos al mail {{ info_contacto }} </p>
        </div>       
        <img class= "cidepint_lab" id="cidepint_lab" src="@/assets/images/cidepint_lab.jpg" alt="logo cidepint"/>
    </section>
</template>

<script>
import { ref, onMounted } from 'vue';
import { apiService } from '@/api.js';

export default {
  name: 'HomeContent',

  setup() {
    const info_contacto = ref('');

    const getContactInfo = async () => {
      try {
        const res = await apiService.get(`/api/contact`, { withCredentials: true });
        console.log(res);
        info_contacto.value = res.data.info_contacto;
      } catch (err) {
        console.error('Error al obtener la información de contacto:', err);
      }
    };

    onMounted(() => {
      getContactInfo();
    });

    return {
      info_contacto,
    };
  },
};
</script>

<style scoped>

.container {
    width: 1000px;
    height: 100px;
    margin: auto; /*CENTRA*/
}
.section_cidep1 {
    display: none; /*OCULTA ENCABEZADOS*/
  }


@media screen and (max-width: 768px) { /*TAMAÑO MAXIMO*/

p, li {
    font-size: 17px;
    margin: 3px 25px;
  }
  .cidepint_lab {
    display: none; /*OCULTA ENCABEZADOS*/
  }

  .section_cidepint {
    display: none; /*OCULTA ENCABEZADOS*/
  }

  .section_cidep1 {
    display: block; /*OCULTA ENCABEZADOS*/
  }
  
  
  }
</style>