<template>
    <ol-map
        :loadTilesWhileAnimating="true"
        :loadTilesWhileInteracting="true"
        style="height: 400px; width: 400px;"
    >
        <ol-view
            ref="view"
            :center="center"
            :zoom="zoom"
            :rotation="rotation"
            :projection="projection"
        />
        <ol-tile-layer>
            <ol-source-osm />
        </ol-tile-layer>

        <ol-vector-layer>
            <ol-source-vector>
                <ol-feature>
                    <ol-geom-point :coordinates="coordinate"></ol-geom-point>
                    <ol-style>
                        <ol-style-icon :src="markerIcon" :scale="0.4"/>
                    </ol-style>
                </ol-feature>
            </ol-source-vector>
        </ol-vector-layer>
    </ol-map>
</template>

<script setup>
    import { ref, onMounted, defineProps } from "vue";
    import markerIcon from "@/assets/images/map_pin.ico";

    const props = defineProps(["coordinates"]);

    const center = ref([-57.95, -34.92]);
    const projection = ref("EPSG:4326");
    const rotation = ref(0);
    const zoom = ref(12);
    const coordinate = ref([0, 0]); // valor predeterminado
    

    onMounted(() => {
        updateCoordinates();
    });

    const updateCoordinates = () => {
        center.value = props.coordinates;
        coordinate.value = props.coordinates;
    };

</script>
