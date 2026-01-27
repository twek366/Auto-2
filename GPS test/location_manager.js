Java.perform(function() {

    const LocationListener = Java.use('android.location.LocationListener');


    const ProxyListener = Java.registerClass({
        name: 'com.example.ProxyLocationListener',
        implements: [LocationListener],
        methods: {
            onLocationChanged: function(location) {

                send({
                    provider: location.getProvider(),
                    latitude: location.getLatitude(),
                    longitude: location.getLongitude(),
                    accuracy: location.getAccuracy() + 'm',
                    time: new Date(location.getTime()).toLocaleString(),
                    speed: location.hasSpeed() ? location.getSpeed() + 'm/s' : 'N/A',
                    altitude: location.hasAltitude() ? location.getAltitude() + 'm' : 'N/A',
                    bearing: location.hasBearing() ? location.getBearing() + '°' : 'N/A'
                });


                this.onLocationChanged(location);
            },
            onStatusChanged: function(provider, status, extras) {

                this.onStatusChanged(provider, status, extras);
            },
            onProviderEnabled: function(provider) {
                this.onProviderEnabled(provider);
            },
            onProviderDisabled: function(provider) {
                this.onProviderDisabled(provider);
            }
        }
    });


    const LocationManager = Java.use('android.location.LocationManager');
    LocationManager.requestLocationUpdates.implementation = function(provider, minTime, minDistance, listener) {

        const proxyListener = ProxyListener.$new();
        return this.requestLocationUpdates(provider, minTime, minDistance, proxyListener);
    };


    LocationManager.getLastKnownLocation.implementation = function(provider) {
        const location = this.getLastKnownLocation(provider);
        if (location) {
            send({
                type: 'last_known',
                provider: provider,
                latitude: location.getLatitude(),
                longitude: location.getLongitude(),
                accuracy: location.getAccuracy() + 'm',
                time: new Date(location.getTime()).toLocaleString()
            });
        }
        return location;
    };

    console.log("Geolocation hook установлен");
});