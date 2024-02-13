console.log('Homework 5')

const ws = new WebSocket('ws://localhost:8080')

formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

ws.onmessage = (e) => {
    console.log(e.data)
    const messages = e.data.split('\n'); // розділяємо повідомлення за символами нового рядка
    messages.forEach(message => {
        const elMsg = document.createElement('div');
        elMsg.textContent = message;
        subscribe.appendChild(elMsg);
    });
}
