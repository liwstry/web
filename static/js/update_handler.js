document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    function updateWeatherDisplay(weather) {
        const weatherWidget = document.querySelector('.weather-widget');

        let tempClass = weather.temp <= 0 ? 'weather-temp-cold' : 'weather-temp';
        weatherWidget.innerHTML = `
                <div class="weather-info">
                    <span class="weather-city">${weather.city}</span>
                    <span class="${tempClass}">${weather.temp}°C</span>
                </div>
            `;
    }

    socket.on('connect', function () {
        socket.emit('get_weather');
    });

    socket.on('weather_update', function (weather_data) {
        updateWeatherDisplay(weather_data);
    });

    setInterval(() => {
        socket.emit('get_weather');
    }, 300000);
});