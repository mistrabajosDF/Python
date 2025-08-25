<template>
    <Bar :chart-options="charOptions" :chart-data="chartData" :data="chartData"></Bar>
</template>

<script>
	import { apiService } from '@/api.js';
	import { Bar } from 'vue-chartjs'
	import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

	ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  	export default {
    	name: "GraphicTwo",
        components: {Bar},
		props: {
			chartId: {
				type: String,
				default: 'bar-chart'
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
                    responsive: true, indexAxis: 'y'
                }
            }
            },
		async mounted(){
			this.loaded = false
			try{
				const grafico1 = await apiService.get('/api/graphics/2', {headers: {'Content-Type': 'application/json','Authorization': `${localStorage.getItem('jwt')}` },});
				grafico1.data.map((row)=>(
					this.etiquetas.push(row.servicio),
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