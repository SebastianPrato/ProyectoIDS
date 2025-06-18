function eliminarProducto(id) {
    const id= parseIntint(id)
    fetch('http://127.0.0.1:5000/admin/borrar/{id}', {method:'POST'})
    .then(response=>{
        if (response.ok){
            alert("Producto eliminado")
            window.location.href = "/admin";
        } else {
            alert("Error al eliminar Producto")
        }
    })
        .catch(error => console.error("Error:", error))
    
}