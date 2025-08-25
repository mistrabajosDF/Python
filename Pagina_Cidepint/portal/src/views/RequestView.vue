<script setup>
  	import AppHeader from "@/components/AppHeader.vue";
  	import AppFooter from "@/components/AppFooter.vue";
	import RequestNotes from "@/components/RequestNotes.vue";
	import { ref, onMounted, computed } from 'vue';
	import { apiService } from '@/api.js';
	import { format } from 'date-fns';
	
	const orderForm = ref({
  		sort: '',
  		order: ''
	});

	const requests = ref([]);

	const formatDate = (dateStr) => {
		return format(new Date(dateStr), 'dd/MM/yyyy HH:mm');
	};

	const filterForm = ref({
  		tipo: '',
  		estado: ''
	});

	const submitOrderForm = async() => {
  		await getRequests(orderForm.value.sort, orderForm.value.order);
	}

	const getRequests = async (sort, order) => {
		try {
			const token = localStorage.getItem('jwt');
			const res = await apiService.get(`/api/me/requests?sort=${sort}&order=${order}`, {
				params: {
					'page': 1,
					'per_page': 10,
				},
				headers: { 
					'Authorization': `${token}`,
					'Content-Type': 'application/json', 
				} });
			requests.value = res.data.map(
				request => {
					return { 
						id: request.id,
						nombre: request.nombre,
						tipo: request.tipo,
						status: request.status,
						observation: request.observation,
						request_date: formatDate(request.request_date),
						obs_est_act: request.obs_est_act,
					};
				}
			);
		} catch (err) {
			console.log(err);
		}
	};

	const requestsFiltered = computed(() => {
    	const filtered = requests.value.filter(req => {
      	return (
        	(!filterForm.value.tipo || req.tipo === filterForm.value.tipo) &&
        	(!filterForm.value.estado || req.status === filterForm.value.estado)
      	);
    	});
    	return filtered;
  	});

	onMounted(() => {
  		getRequests();
	});

</script>

<template>
    <AppHeader />
    <div class="container_rq">
		<h1>Mis solicitudes</h1>

		<form id="ordenar-form" @submit.prevent="submitOrderForm">
			<label for="sort">Ordenar por... Criterio:</label>
        	<select v-model="orderForm.sort" name="sort">
            	<option selected value="">Ninguno</option>
            	<option value="fecha">Fecha</option>
            	<option value="status">Estado</option>
        	</select>
			<label for="order">Orden:</label>
        	<select v-model="orderForm.order" name="order">
            	<option selected value="asc">Ascendente</option>
            	<option value="desc">Descendente</option>
        	</select>
        	<input type="submit" value="Ordenar">
    	</form>

		<form id="filtrar-form">
			<label for="tipo">Filtrar por... Tipo servicio:</label>
        	<select v-model="filterForm.tipo" name="tipo">
            	<option selected value="">Todos</option>
            	<option value="Analisis">Análisis</option>
            	<option value="Consultoria">Consultoría</option>
            	<option value="Desarrollo">Desarrollo</option>
        	</select>
			
			<label for="estado">Estado:</label>
        	<select v-model="filterForm.estado" name="estado">
            	<option selected value="">Todos</option>
				<option value="Pendiente">Pendiente</option>
            	<option value="Aceptada">Aceptada</option>
            	<option value="Rechazada">Rechazada</option>
            	<option value="En proceso">En proceso</option>
            	<option value="Finalizada">Finalizada</option>
            	<option value="Cancelada">Cancelada</option>
        	</select>
    	</form>

		<table class="table table-striped">
			<thead>
				<tr>
                	<th scope="col" colspan="2">Servicio</th>
					<th scope="col" colspan="1">Tipo</th>
					<th scope="col" colspan="4">Resumen</th>
                	<th scope="col" colspan="1">Estado</th>
                	<th scope="col" colspan="2">Observaciones estado</th>
					<th scope="col" colspan="1">Notas</th>
					<th scope="col" colspan="1">Fecha</th>
            	</tr>
			</thead>
			<tbody>
				<template v-for="req in requestsFiltered" :key="req.id">
					<tr>
						<td colspan="2">{{ req.nombre }}</td>
						<td colspan="1">{{ req.tipo }}</td>
						<td colspan="4" class="text-break">{{ req.observation }}</td>
						<td colspan="1">{{ req.status }}</td>
						<td colspan="2" class="text-break">{{ req.obs_est_act }}</td>
						<td scope="col" colspan="1">
							<button 
								class="btn btn-primary" 
								data-bs-toggle="collapse" 
								:href="'#collapseNotes' + req.id" 
								role="button" 
								:aria-expanded="false" 
								:aria-controls="'collapseNotes' + req.id">Notas
							</button>
						</td>
						<td colspan="1">{{ req.request_date }}</td>
					</tr>
					<tr>
						<td colspan="12">
						<div class="collapse" :id="'collapseNotes' + req.id">
							<div class="card card-body mt-3">
								<RequestNotes :requestId="req.id" />
								<form action="" method="POST" @submit.prevent="handleSubmit">
									<div class="mb-3">
										<textarea
											name="nota"
											class="form-control" 
											id="notaText" 
											placeholder="" 
											v-model="formData.contenido_nota"
											maxlength="250"
											minlength="1">
										</textarea>
									</div>
									<div v-if="longText" class="alert alert-danger mt-2" role="alert">
										La nota no puede contener más de 250 caracteres ni puede estar vacía.
									</div>
									<button  @click="sendNote(req.id)" type="submit" class="btn btn-primary">Enviar</button>
								</form>
								<div v-if="successMessage" class="alert alert-success mt-3" role="alert">
									{{ successMessage }}
								</div>
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
  	export default {
    	name: "RequestView",
    	components: {
      		AppHeader,
      		AppFooter,
			RequestNotes,
    	},

		data() {
            return{
                formData: {
                    contenido_nota: '',
                },
                successMessage: '',
				longText: false,
            }
        },

		methods: {
			handleSubmit() {
                console.log("fdjfhjksd");
            },
			
			async sendNote(id) {
                try {
                    if ( this.formData.contenido_nota.length > 249 || this.formData.contenido_nota.length < 1) {
                        this.longText = true;
                        return;
                    };
                    const token = localStorage.getItem('jwt');
                    const dataToSend = {
                        'text': this.formData.contenido_nota,
                    };
                    await apiService.post(`/api/me/requests/${id}/notes`, dataToSend, {
                        headers: { 
                            'Authorization': `${token}`,
                            'Content-Type': 'application/json', 
                        } 
                    });

                    this.successMessage = 'Nota enviada con éxito';
                    this.formData.contenido_nota = '';
                    this.longText = false;

                } catch (err) {
                    console.log(err);
                }
            },
		}
  	};
</script>

<style>
	.container_rq {
		margin-top: 6rem;
	}
</style>