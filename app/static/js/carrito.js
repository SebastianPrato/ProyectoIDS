const cantidadCarritoElements = document.querySelectorAll(".cantidad-carrito");

function actualizarNumeroCarrito() {
	fetch("http://127.0.0.1:5001/api/compras/carrito",
		{
			method: "GET",
			credentials: "include"
		}
	)
		.then(response => response.json())
		.then(data => {
			cantidad = data.length;
			cantidadCarritoElements.forEach(element => {
				element.textContent = cantidad;
			});
		});
}

function eliminarProducto(id_detalle_compra) {
        fetch('http://127.0.0.1:5001/api/compras/carrito', {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_detalle_compra: id_detalle_compra
            })
        }).then(response => {
            alert("Producto eliminado del carrito");
            window.location.reload();
        });
    }

document.addEventListener("DOMContentLoaded", () => {
	actualizarNumeroCarrito();
});