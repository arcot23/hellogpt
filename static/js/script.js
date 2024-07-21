document.addEventListener('DOMContentLoaded', function () {
    const eventSource = new EventSource('/stream');

    eventSource.onmessage = function (event) {
        const log = document.getElementById('log');

        const message = document.createElement('div');
        const data = JSON.parse(event.data);
        message.innerHTML = `${data.d}`;

//        const message = document.createElement('div');
//        message.innerHTML = event.data;
//        const message = document.createElement('textarea');
//        message.value = event.data;
        log.appendChild(message);
    };

    eventSource.onerror = function () {
        console.error('Error in event source');
        eventSource.close();
    };
});
