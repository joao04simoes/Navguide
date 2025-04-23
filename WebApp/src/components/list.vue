<template>
    <div>
        <button @click="GetSections">Get sections</button>
        <button @click="makeShoppingList">make list</button>
        <div v-if="sectionsPoints">
            <h2>Sections:</h2>

            <input type="text" v-model="searchQuery" placeholder="Search..." />
            <ul>
                <li v-for="(point, index) in filteredSections" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                    <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
                </li>
            </ul>
            <h2>ALL sections:</h2>

            <ul>
                <li v-for="(point, index) in sectionsPoints" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                    <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
                </li>
            </ul>

        </div>
        <div v-if="shoppingList">
            <router-link to="/route">
                <button>Iniciar a navegação</button>
            </router-link>
            <ul>
                <li v-for="(point, index) in shoppingList" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                </li>
            </ul>

        </div>
    </div>
</template>


<script>
import axios from 'axios';
import { useRoute } from 'vue-router'


export default {
    data() {
        return {
            sectionsPoints: null,
            shoppingListIds: [],
            shoppingList: null,
            searchQuery: '',
        }
    },

    computed: {
        filteredSections() {
            if (!this.searchQuery) {
                return ""
            }
            return this.sectionsPoints.filter(point =>
                point[1].toLowerCase().includes(this.searchQuery.toLowerCase()))
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

        }
    },

    mounted() {
        this.GetSections();
    }
}
</script>

<style scoped>
div {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 600px;
    margin: auto;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-top: 1rem;
    color: #2c3e50;
}

ul {
    padding: 0;
    list-style-type: none;
}

li {
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.3rem 0;
    border-bottom: 1px solid #eee;
    color: #333;
}

button {
    margin-top: 1rem;
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

button:hover {
    background-color: #2ecc71;
}
</style>
