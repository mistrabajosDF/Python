<template>
    <p>Notas</p>
    <ul>
        <li v-for="a_note in all_notes" :key="a_note.id">
            {{ a_note.description }} - {{a_note.inserted_at }}
        </li>
    </ul>

</template>

<script setup>
    import { ref, onMounted, defineProps } from "vue";
    import { apiService } from '@/api.js';
    import { format } from 'date-fns';

    const props = defineProps(["requestId"]);
    const all_notes = ref([]);

    const formatDate = (dateStr) => {
        return format(new Date(dateStr), 'dd/MM/yyyy HH:mm');
    };

    const getNotes = async () => {
        try {
            const token = localStorage.getItem('jwt');
            const res = await apiService.get(`/api/me/requests/${props.requestId}/notes`, {
                headers: { 
                    'Authorization': `${token}`,
                    'Content-Type': 'application/json', 
                } });

            all_notes.value = res.data.map(
                a_note => {
                    const formattedDate = formatDate(a_note.inserted_at);
                    return { 
                        id: a_note.id,
                        description: a_note.description,
                        inserted_at: formattedDate,
                    };
                }
            );
        } catch (err) {
            console.log(err);
        }
    };

    onMounted(() => {
  		getNotes();
	});
</script>

<script>
    export default {
        name: 'RequestNotes',
    }
</script>