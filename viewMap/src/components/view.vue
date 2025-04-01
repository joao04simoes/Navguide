<template>
    <div>
        <h2>Live Supermarket Map</h2>
        <div id="map"></div>
        <button @click="calculateRoute"> route </button>
    </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    data() {
        return {
            map: null,
            personMarker: null
        };
    },
    mounted() {
        this.initMap();
        this.loadMapData();

    },
    methods: {
        initMap() {
            this.map = L.map('map').setView([3, 1.5], 7);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(this.map);

            // Marcador da pessoa (inicialmente no centro)
            this.personMarker = L.marker([3, 1.5]).addTo(this.map);

        },

        async calculateRoute() {
            try {
                const response = await fetch('http://127.0.0.1:5000/route');
                const data = await response.json();
                for (let i = 0; i < data.length - 1; i++) {
                    L.polyline([data[i], data[i + 1]], { color: 'blue' }).addTo(this.map);
                }

            } catch (error) {
                console.error('Erro ao atualizar localização:', error);
            }
        },
        async loadMapData() {
            try {
                const response = await fetch('http://127.0.0.1:5000/map');
                const data = await response.json();

                // Desenha os limites do supermercado
                L.polygon(data.bounds, { color: 'red' })
                    .addTo(this.map)
                    .bindPopup('Supermercado');

                // Adiciona estações (caixas, seções)
                data.stations.forEach(station => {
                    L.marker(station.coords)
                        .addTo(this.map)
                        .bindPopup(station.name);
                });

                // Desenha os corredores (aisles) como linhas horizontais
                data.aisles.forEach(aisle => {
                    L.polyline([aisle.start, aisle.end], { color: 'blue', weight: 3, dashArray: '5, 5' })
                        .addTo(this.map)
                        .bindPopup(aisle.name);
                });

                // Desenha as prateleiras (shelves) como linhas verticais
                data.shelves.forEach(shelf => {
                    const [x, y] = shelf.coords;
                    L.polyline([[x, y - 0.5], [x, y + 0.5]], { color: 'green', weight: 4 }) // Linha vertical
                        .addTo(this.map)
                        .bindPopup(`Prateleira ${shelf.id}`);
                });



            } catch (error) {
                console.error('Erro ao carregar o mapa:', error);
            }
        },
        async updateLocation() {
            try {
                const response = await fetch('http://127.0.0.1:5000/location');
                const data = await response.json();
                this.personMarker.setLatLng([data.lat, data.lng]);
            } catch (error) {
                console.error('Erro ao atualizar localização:', error);
            }
        },
        startLocationUpdates() {
            setInterval(this.updateLocation, 1000);
        }
    }
};
</script>

<style>
#map {
    width: 100%;
    height: 400px;
}
</style>
