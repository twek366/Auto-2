Java.perform(function() {
 
    send("Скрипт начал работу");

    const LocationManager = Java.use('android.location.LocationManager');
    const Location = Java.use('android.location.Location');


    LocationManager.getLastKnownLocation.overload('java.lang.String').implementation = function(provider) {
        const location = this.getLastKnownLocation(provider);
        
        if (location) {
            send(`
📍 Получена локация от ${provider}
├ Широта: ${location.getLatitude()}
├ Долгота: ${location.getLongitude()}
├ Точность: ${location.getAccuracy()} м
├ Время: ${new Date(location.getTime())}
├ Высота: ${location.getAltitude()} м
└ Скорость: ${location.getSpeed()} м/с
`);
        } else {
            send(`Нет данных локации от ${provider}`);
        }
        
        return location;
    };


    LocationManager.requestLocationUpdates.overload(
        'java.lang.String', 'long', 'float', 'android.location.LocationListener'
    ).implementation = function(provider, minTime, minDistance, listener) {
        send(`Приложение запросило обновления локации:
├ Источник: ${provider}
├ Интервал: ${minTime} мс
└ Минимальная дистанция: ${minDistance} м`);


        const ProxyListener = Java.registerClass({
            name: 'com.example.ProxyLocationListener',
            implements: [Java.use('android.location.LocationListener')],
            methods: {
                onLocationChanged: function(location) {
                    send(`
Получено обновление локации:
├ Широта: ${location.getLatitude()}
├ Долгота: ${location.getLongitude()}
├ Точность: ${location.getAccuracy()} м
└ Время: ${new Date(location.getTime())}
`);
                    listener.onLocationChanged(location);
                },
                onStatusChanged: function(provider, status, extras) {
                    listener.onStatusChanged(provider, status, extras);
                },
                onProviderEnabled: function(provider) {
                    send(`Источник ${provider} стал доступен`);
                    listener.onProviderEnabled(provider);
                },
                onProviderDisabled: function(provider) {
                    send(`Источник ${provider} стал недоступен`);
                    listener.onProviderDisabled(provider);
                }
            }
        });

        const proxyListener = ProxyListener.$new();
        return this.requestLocationUpdates(provider, minTime, minDistance, proxyListener);
    };


    const methodsToHook = [
        'requestSingleUpdate',
        'getProviders',
        'isProviderEnabled'
    ];

    methodsToHook.forEach(method => {
        if (LocationManager[method] && LocationManager[method].overloads) {
            LocationManager[method].overloads.forEach(overload => {
                overload.implementation = function() {
                    const args = Array.prototype.slice.call(arguments);
                    send(`Вызван ${method} с аргументами: ${JSON.stringify(args)}`);
                    return this[method].apply(this, arguments);
                };
            });
        }
    });
});