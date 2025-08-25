<script setup>
  	import AppHeader from "@/components/AppHeader.vue";
  	import AppFooter from "@/components/AppFooter.vue";
	import InstitutionMap from '@/components/InstitutionMap.vue';

</script>

<template>
  	<AppHeader/>
	<div class="container_sv">
		<h1>Detalle del servicio {{ servicio.nombre }}</h1>
		<router-link class="btn btn-primary mx-2" to="/services">Volver a servicios</router-link>
		<br/>
	  	<br/>
		
		<table class="table table-striped">
			<thead>
				 <tr>
                	<th scope="col">Nombre</th>
                	<th scope="col">Descripción</th>
                	<th scope="col">Tipo</th>
					<th scope="col">Palabras Clave</th>
            	</tr>
			</thead>
			<tbody>
				<tr>                    
					<td data-label="Nombre">{{ servicio.nombre }}</td>
					<td data-label="Descripción">{{ servicio.descripcion }}</td>
					<td data-label="Tipo">{{ servicio.tipo }}</td>
					<td data-label="Palabras">
						<ul v-for="palabra in servicio.palabras_clave" :key="palabra.key">
                			<a> {{ palabra.name }} </a>
						</ul>
            		</td>
                </tr>
			</tbody>
		</table>

        <h1>Instituciones a cargo</h1>
		<table class="table table-striped">
			<thead>
            	<tr>
                	<th scope="col" colspan="2">Nombre</th>
                	<th scope="col" colspan="2">Información</th>
                	<th scope="col" colspan="2">Direccion</th>
                	<th scope="col" colspan="2">Pagina web</th>
                	<th scope="col" colspan="2">Días y horarios</th>
                	<th scope="col" colspan="2">Contacto</th>
            	</tr>
        	</thead>
			<tbody>
				<template v-for="centro in servicio.centrosACargo" :key="centro.id">
					<tr>
						<td colspan="2">{{ centro.nombre }}</td>
						<td colspan="2">{{ centro.informacion }}</td>
						<td colspan="2">{{ centro.direccion }}</td>
						<td colspan="2">{{ centro.paginaweb }}</td>
						<td colspan="2">{{ centro.diasyhorarios }}</td>
						<td colspan="2">{{ centro.contacto }}</td>
					</tr>

					<tr>
						<td colspan="12">
							<div class="d-flex justify-content-around align-items-center">
								<button 
									class="btn btn-primary" 
									data-bs-toggle="collapse" 
									:href="'#collapseForm' + centro.id" 
									role="button" 
									:aria-expanded="false" 
									:aria-controls="'collapseForm' + centro.id" @click="handleSolicitar">Solicitar
								</button>
								<button 
									class="btn btn-primary" 
									data-bs-toggle="collapse" 
									:href="'#collapseMap' + centro.id" 
									role="button" 
									:aria-expanded="false" 
									:aria-controls="'collapseMap' + centro.id">Mapa
								</button>
							</div>
							<div class="collapse" :id="'collapseForm' + centro.id">
								<div class="card card-body mt-3">
									<form action="" method="POST" @submit.prevent="handleSubmit">
										<div class="mb-3">
											<textarea 
												name="observacion"
												class="form-control" 
												id="observacionText" 
												placeholder="Ingresa un resumen del trabajo a solicitar" 
												v-model="formData.observacion"
												maxlength="250"
												minlength="1">
											</textarea>
										</div>
										<div v-if="longText" class="alert alert-danger mt-2" role="alert">
											El resumen no puede contener más de 250 caracteres ni puede estar vacío.
										</div>
										<button  @click="sendData(centro.id)" type="submit" class="btn btn-primary">Enviar</button>
									</form>
								</div>
								<div v-if="successMessage" class="alert alert-success mt-3" role="alert">
									{{ successMessage }}
								</div>
							</div>
							<div class="collapse" :id="'collapseMap' + centro.id">
								<div class="card card-body mt-3">
									<InstitutionMap :coordinates="convertToCoord(centro.localizacion)" />
								</div>
							</div>
						</td>
					</tr>
				</template>
            </tbody>
        </table>
	</div>
  	<AppFooter />
</template>

<script>
	import { apiService } from '@/api.js';
	import { format } from 'date-fns';

	const convertToCoord = (coordinatesString) => {
  		const [latitud, longitud] = coordinatesString.split(',').map(coord => parseFloat(coord.trim()));
  		return [longitud, latitud];
	};

  	export default {
    	name: "DetalleServiceView",
    	
		components: {
      		AppHeader,
      		AppFooter,
			InstitutionMap,
    	},

		data() {
			return {
				servicio: {},
				formData: {
      				observacion: '',
    			},
				successMessage: '',
				longText: false,
			};
		},

		computed: {
            isUserInLocalStorage() {
                return localStorage.getItem('user') !== null;
            }   
        },

		methods: {
			async getId(){
				const serviceId = this.$route.params.id;
				try {
					const res = await apiService.get(`/api/services/${serviceId}`, { withCredentials: true });
					this.servicio = res.data;
				} catch (err) {
					console.log(err);
				}
			},

			handleSubmit() {
                console.log("fdjfhjksd");
            },

			async handleSolicitar(){
				if (this.isUserInLocalStorage) {
					return;
				}
				else {
					this.$router.push({ name: 'login' });
				}
			},
			
			async sendData(centro) {
				try {
					if ( this.formData.observacion.length > 249 || this.formData.observacion.length < 1) {
						this.longText = true;
						return;
					};
					const token = localStorage.getItem('jwt');
					const currentDateTime = new Date();
					const formattedDate = format(currentDateTime, "yyyy-MM-dd HH:mm:ss.SSSSSS");

					const dataToSend = {
  						service_id: this.servicio.id,
						institution_id: centro,
						request_date: formattedDate,
						status: "Pendiente",
						change_status_date: null,
						observation: this.formData.observacion,
					};

					await apiService.post('/api/me/requests', dataToSend,{
						headers: { 
							'Authorization': `${token}`,
							'Content-Type': 'application/json', 
						} 
					});

					this.successMessage = 'Solicitud enviada con éxito';
					this.longText = false;
					this.formData.observacion = '';

				} catch (error) {
					console.error('Error al enviar datos:', error);
				}
			}
		},
		
		mounted(){
			this.getId();
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