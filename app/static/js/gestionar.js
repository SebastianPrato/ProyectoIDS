function eliminarProducto() {
    const id=parseInt(document.getElementById("producto-id").value)
    if (confirm('¿Estás seguro de que queres eliminar el producto?')) {
        fetch(`http://127.0.0.1:5000/usuario/admin/borrar/${id}`, {
            method: 'DELETE'})
        .then(response => {
            if (response.ok) {
                alert("Producto eliminado con éxito.");
                window.location.href = "/admin";
            } else {
                alert("Error al eliminar el producto.");
            }
        });
    }
}   