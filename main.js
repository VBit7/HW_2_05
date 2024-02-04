console.log('Hello world!')

const ws = new WebSocket('ws://localhost:8080')

function sendCommand() {
    const inputField = document.getElementById('textField');
    ws.send(inputField.value)
    inputField.value = null
}

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

ws.onmessage = (e) => {
    const response = e.data;
    const elMsg = document.createElement('div');
    elMsg.textContent = response;
    subscribe.appendChild(elMsg);
}

ws.onclose = (e) => {
    console.log('WebSocket closed');
}

ws.onerror = (e) => {
    console.error('WebSocket error:', e);
}
