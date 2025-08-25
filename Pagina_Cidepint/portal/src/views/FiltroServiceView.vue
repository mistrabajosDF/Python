<script setup>
  	import AppHeader from "@/components/AppHeader.vue";
  	import AppFooter from "@/components/AppFooter.vue";

</script>

<template>
	<AppHeader />
  <div class="container_sv">
	  <h1>Resultados de tu búsqueda</h1>
	  <br/>
	  <router-link class="btn btn-primary" to="/services">Quitar filtro de búsqueda</router-link>
	  <br/>
	  <br/>
	  <table class="table table-striped">
		  <thead>
			   <tr>
				  <th scope="col">Nombre</th>
				  <th scope="col">Descripción</th>
				  <th scope="col">Tipo</th>
				  <th scope="col">Instituciones</th>
				  <th scope="col">Palabra</th>
				  <th scope="col"></th>
			  </tr>
		  </thead>
		  <tbody>
			  <tr v-for="serv in services" :key="serv.id">
				  <td data-label="Nombre">{{ serv.nombre }}</td>
				  <td data-label="Descripción">{{ serv.descripcion }}</td>
				  <td data-label="Tipo">{{ serv.tipo }}</td>
				  <td data-label="Instituciones">
					  <ul v-for="centro in serv.centrosACargo" :key="centro.id">
						  <a> {{ centro.nombre }} </a>
					  </ul>
				  </td>
				  <td data-label="Palabra">
					  <ul v-for="palabra in serv.palabras_clave" :key="palabra.id">
						  <a> {{ palabra.name }} </a>
					  </ul>
				  </td>
				  <td>
					  <router-link class="btn btn-primary" :to="{ name: 'servicedetalle', params: { 'id': serv.id } }" >Ver detalle</router-link>
				  </td>
			  </tr>
		  </tbody>
	  </table>
	  <br/>
	  <br/>
  </div>
	<AppFooter />
</template>

<script>
	import { apiService } from '@/api.js';

  	export default {
    	name: "FiltroServiceView",
    	
		components: {
      		AppHeader,
      		AppFooter,
    	},

		data() {
			return {
				services: {},
			};
		},

		methods: {
			async getParams(){
				const insti = this.$route.params.i;
				const palabra = this.$route.params.p;
				const nombre = this.$route.params.n;
				const descripcion = this.$route.params.d;
				const tipo = this.$route.params.t;	
				try {									
					const res = await apiService.get(`/api/filtrar_serv?i=${insti}&n=${nombre}&p=${palabra}&d=${descripcion}&t=${tipo}`);
					this.services = res.data;
				} catch (err) {
					console.log(err);
				}
			},
		},

		mounted(){
			this.getParams();
		},
	};
</script>

<style scoped>

.table {
    width: 100%; /*TOMA TODA LA PANTALLA*/
    border: 1px solid #ccc; /*COLOR DEL BORDE*/
    border-collapse: collapse; /*NO TOMA ESPACIO AL PEDO*/
    margin: 0;
    padding: 0;
    table-layout: fixed; /*ATRIBUTOS DE TABLA, MISMO ANCHO... NO SE*/
}


.table tr { /*BORDES DE TABLA*/
    background-color: #f8f8f8;
    border: 2px solid #00bfbf ;
}

.table th, .table td {
    font-size: 16px;
    padding: 8px;
    text-align: center;
}

.table thead th{ /*ENCABEZADO EN MAYUSCuLA Y CON OTRO COLOR*/
    text-transform: uppercase;
    background-color: #00bfbf;
}

.table tbody td:hover { /*PONE MAS OSCURO EL CAMPO AL PASAR ENCIMA*/
    background-color: #7cd5d5;
}

@media screen and (max-width: 768px) { /*TAMAÑO MAXIMO*/
    .table {
        border: 0px;
    }
    .table thead {
        display: none; /*OCULTA ENCABEZADOS*/
    }
    .table tr {
        margin-bottom: 8px;
        border-bottom: 4px solid  #00bfbf ;
        display: block;
    }
    .table th, .table td { /*Tamaño fuente*/
        font-size: 16px;
    }
    .table td {
        display: block; /*Datos en horizontal*/
        border-bottom: 2px solid #00bfbf;
        text-align: right; /*Alinea datos a la derecha*/
    }
    .table  td:last-child {
        border-bottom: 0px;
    }
    .table td::before { /*PONE LOS ENCABEZADOS DE LA TABLA*/
        content: attr(data-label);
        font-weight: bold;          /*negrita*/
        text-transform: uppercase;  /*mayusculas*/
        float: left;                /*a la izq*/
    }
}
</style>