<template>
    <div>
        <button @click="GetSections">Get sections</button>
        <div v-if="sectionsPoints">
            <h2>Sections:</h2>
            <ul>
                <li v-for="(point, index) in sectionsPoints" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                    <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
                </li>
            </ul>
            <button @click="makeShoppingList">make list</button>
        </div>
    </div>
</template>


<script>
import axios from 'axios';


export default {
    data() {
        return {
            sectionsPoints: null,
            shoppingListIds: [],
            shoppingList: null,
        }
    },
    methods: {
        async postList() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/list', this.shoppingList)
            } catch (error) {
                console.error(error);
            }
        },

        async GetSections() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/sections')
                this.sectionsPoints = response.data;
            } catch (error) {
                console.error(error);
            }
        },

        makeShoppingList() {
            const rawIds = [...this.shoppingListIds];
            this.shoppingList = this.sectionsPoints.filter(point => rawIds.includes(point[0]));
            this.postList();
            this.sectionsPoints = null;
            this.shoppingList = null;

        }
    },
}
</script>