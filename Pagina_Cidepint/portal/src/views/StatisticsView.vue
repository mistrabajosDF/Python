<script setup>
  	import AppHeader from "@/components/AppHeader.vue";
  	import AppFooter from "@/components/AppFooter.vue";
	import GraphicOne from "@/components/GraphicOne.vue"
	import GraphicTwo from "@/components/GraphicTwo.vue"
	import GraphicThree from "@/components/GraphicThree.vue"

</script>

<template>
  	<AppHeader />
	<br><br><br>
	<div class="row mt-3">
		<div class="col-md-6 offset-md-3">
			<div class="card border border-dark">
				<div class="card-header bg-dark text-white">Cantidad de solicitudes por estado</div>
				<div class="card-body">
					<GraphicOne/>
				</div>
			</div>
			<br>
			<div class="card border border-dark">
				<div class="card-header bg-dark text-white">Ranking de los servicios más solicitados</div>
				<div class="card-body">
					<GraphicTwo/>
				</div>
			</div>
			<br>
			<div class="card border border-dark">
				<div class="card-header bg-dark text-white">Top 10 instituciones con más solicitudes</div>
				<div class="card-body">
					<GraphicThree/>
				</div>
			</div>
		</div>
	</div>
	<br><br><br>
  	<AppFooter />
</template>

<script>

  	export default {
    	name: "StatisticsView",
    	components: {
      		AppHeader,
			GraphicOne,
			GraphicTwo,
			GraphicThree,
      		AppFooter,
    	},
	}
</script>
