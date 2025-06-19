document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('formularioPago').addEventListener('submit', async function(e) {
        e.preventDefault();

        const datos = {
            numero: document.getElementById('numero').value,
            nombre: document.getElementById('nombre').value,
            vencimiento: document.getElementById('vencimiento').value,
            cvv: document.getElementById('cvv').value
        };

        const respuesta = await fetch('/api/confirmar_pago', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();
        const mensaje = document.getElementById('mensaje');
        if (respuesta.ok) {
            mensaje.innerHTML = `<div class="alert alert-success">${resultado.mensaje}</div>`;
        } else {
            mensaje.innerHTML = `<div class="alert alert-danger">${resultado.error}</div>`;
        }
    });
});