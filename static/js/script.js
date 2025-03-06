function calculate() {
    const volume = parseFloat(document.getElementById('volume').value);
    const abv = parseFloat(document.getElementById('abv').value);
    const price = parseFloat(document.getElementById('price').value);

    if (volume && abv && price) {
        const coefficient = (volume * abv) / price;
        document.getElementById('result').textContent =
            `Коэффициент выгодности: ${coefficient.toFixed(2)}`;
    } else {
        alert('Заполните все поля числами!');
    }
}

document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        name: document.getElementById('name').value,
        message: document.getElementById('message').value
    };

    fetch('/log_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert('Сообщение отправлено в вечные архивы лоховства!');
            document.getElementById('messageForm').reset();
        }
    })
    .catch(error => console.error('Error:', error));
});