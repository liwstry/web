document.addEventListener('DOMContentLoaded', function() {
    const socket = io();

    socket.on('server_update', function(data) {
        // Обновляем процессор
        document.getElementById('cpu-value').textContent = data.cpu;
        document.getElementById('cpu-progress').style.width = data.cpu + '%';

        // Обновляем ОЗУ
        document.getElementById('memory-value').textContent = data.ram;
        document.getElementById('memory-progress').style.width = data.ram + '%';

        // Обновляем диск
        document.getElementById('disk-c-value').textContent = data.disk_percent;
        document.getElementById('disk-c-used').textContent = data.disk_used;
        document.getElementById('disk-c-total').textContent = data.disk_total;
        // document.getElementById('disk-c-progress').style.width = data.disk_percent + '%';

        // Время работы
        document.getElementById('uptime-value').textContent = data.time_work + ' часов';

        // Сетевой трафик
        document.getElementById('bytes-sent').textContent = data.bytes_sent;
        document.getElementById('bytes-recv').textContent = data.bytes_recv;
    });

    socket.emit('get_server_stats');
});