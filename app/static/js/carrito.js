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

document.addEventListener("DOMContentLoaded", () => {
	actualizarNumeroCarrito();
});