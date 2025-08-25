<script setup>
  	import AppHeader from "@/components/AppHeader.vue";
  	import AppFooter from "@/components/AppFooter.vue";
	import { ref, onMounted } from 'vue';
	import { apiService } from '@/api.js';

	const services = ref([]);

	const getServices = async () => {
		try {
			const res = await apiService.get('/api/all_services', { withCredentials: true });
			services.value = res.data;
		} catch (err) {
			console.log(err);
		}
	};

	onMounted(() => {
  		getServices();
	});

</script>

<template>
  	<AppHeader />
	<div class="container_sv">
		
		<h1>Todos los servicios</h1>
		<h3>Ingrese criterios de búsqueda:</h3>
		<form id="filtrar-form" action="" method="POST">
        	<label for="nombre">Nombre:</label>
			<input type="text" name="nombre" id="nombre" v-model="nombre" size="30" maxlength="50">

        	<label for="institucion">Institución:</label>
        	<input type="text" name="institucion" id="institucion" v-model="institucion" size="30" maxlength="50">

			<label for="tipo">Tipo:</label>
        	<select type="text" name="tipo" id="tipo" v-model="tipo">
            	<option selected value="-">Todos</option>
            	<option value="Analisis">Análisis</option>
            	<option value="Consultoria">Consultoría</option>
            	<option value="Desarrollo">Desarrollo</option>
        	</select>

			<br/>

			<label for="palabra">Palabra clave:</label>
        	<input type="text" name="palabra" id="palabra" v-model="palabra" size="30">

			<label for="palabra">Descripcion:</label>
        	<input type="text" name="descripcion" id="descripcion" v-model="descripcion" size="30" maxlength="100">

			<button type="submit" @click.prevent="enviarDatos()">Buscar</button>

			<br/>
			<br/>

    	</form>

		<table class="table table-striped">
			<thead>
				 <tr>
                	<th scope="col">Nombre</th>
                	<th scope="col">Descripción</th>
                	<th scope="col">Tipo</th>
					<th scope="col">Instituciones</th>
					<th scope="col">Palabras Clave</th>
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
					<td data-label="Palabras Clave">
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
  	export default {
    	name: "ServicesView",
    	components: {
      		AppHeader,
      		AppFooter,
    	},
		data() {
    		return {
      			nombre: '',
				institucion: '',
				palabra: '',
      			descripcion: '',
				tipo: '',
    		}
  		},
  
  		methods: {
    		enviarDatos() {
				if(this.institucion === "") {
					this.institucion = "-";
				}
				if(this.nombre === "") {
					this.nombre = "-";
				}
				if(this.descripcion === "") {
					this.descripcion = "-";
				}
				if(this.palabra === "") {
					this.palabra = "-";
				}
				if(this.tipo === "") {
					this.tipo = "-";
				}
				this.$router.push({ name: 'filtroservice', params: { 'i': this.institucion, 'n': this.nombre, 'p': this.palabra, 'd':this.descripcion, 't':this.tipo } });
    			//this.$router.push({ path: `/filtroservice/${this.institucion}` })
			}	
		}
  	};
</script>

<style>
	label {
		padding: 0.5rem;
	}
	input {
		margin-left: 0.5rem;
	}
</style>

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
```