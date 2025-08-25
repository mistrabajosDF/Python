<template>
    <Doughnut :chart-options="charOptions" :chart-data="chartData" :data="chartData"></Doughnut>
</template>

<script>
	import { apiService } from '@/api.js';
	import { Doughnut } from 'vue-chartjs'
	import { Chart as ChartJS, Tooltip, Legend, ArcElement } from 'chart.js'

	ChartJS.register( Tooltip, ArcElement, Legend)
  	export default {
    	name: "GraphicOne",
        components: {Doughnut},
		props: {
			chartId: {
				type: String,
				default: 'doughnut'
			},
  		},
        data() {
            return {
                loaded: false,
                etiquetas: [],
                valores: [],
                chartData: {
                labels: [],
                datasets: [
                    { label: 'Solicitudes', data: [], backgroundColor: ['#9B59B6', '#28B463', '#DAF7A6', '#FFC300', '#FF5733', '#C70039'] }
                ]
                },
                charOptions: {
                    responsive: true
                }
            }
            },
		async mounted(){
			this.loaded = false
			try{
				const grafico1 = await apiService.get('/api/graphics/1', {headers: {'Content-Type': 'application/json','Authorization': `${localStorage.getItem('jwt')}` },});
				grafico1.data.map((row)=>(
					this.etiquetas.push(row.status),
					this.valores.push(row.cantidad)
				))
				this.chartData = {
					labels: this.etiquetas,
					datasets:[
						{label:'Solicitudes', data:this.valores, backgroundColor: ['#9B59B6','#28B463','#DAF7A6','#FFC300','#FF5733','#C70039']}
					]
				}
				this.loaded=true
			} catch (e) {
      			console.error(e)
    		}

			
		}

	}
</script>