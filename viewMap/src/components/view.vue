<template>
    <div>
        <h2>Live Supermarket Map</h2>
        <div id="map" style="width: 600px; height: 400px;"></div>
    </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    data() {
        return {
            map: null,
            personMarker: null,
        };
    },
    mounted() {
        this.initMap();
        this.startLocationUpdates();
    },
    methods: {
        initMap() {
            this.map = L.map('map').setView([3, 3], 19);
            L.tileLayer('', { attribution: 'Supermarket Map' }).addTo(this.map);

            // Define supermarket layout
            const supermarketBounds = [
                [2, 2], [4, 2], [4, 0], [2, 0]
            ];
            L.polygon(supermarketBounds, { color: 'red' })
                .addTo(this.map)
                .bindPopup('Entrance');

            // Add person marker
            this.personMarker = L.marker([3, 3]).addTo(this.map);
        },
        updateLocation() {
            fetch('http://127.0.0.1:5000/location')
                .then(response => response.json())
                .then(data => {
                    this.personMarker.setLatLng([data.lat, data.lng]);
                })
                .catch(error => console.error('Error fetching location:', error));
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