const cuentaCarritoElement = document.getElementById("cuenta-carrito");
actualizarNumeroCarrito();

function agregarAlCarrito(juego) {
  const productos=localStorage.getItem("juegos") || []
  if (!productos| memoria.length === 0) {
    const producto = addproduct(juego);
    localStorage.setItem("juegos", JSON.stringify([producto]));
    actualizarNumeroCarrito();
    return 1;
  }

  let items = JSON.parse(localStorage.getItem("juegos"));
  const indice = items.findIndex(producto => producto.id === juego.id);

  if (indice === -1) {
    const producto = addproduct(juego);
    items.push(producto);
  } else {
    items[indice].cantidad++;
  }

  localStorage.setItem("juegos", JSON.stringify(items));
  actualizarNumeroCarrito();
  return items[indice]?.cantidad || 1;
}

function addproduct(juego) {
  return {
    nombre: juego.nombre,
    cantidad: 1,
    precio: juego.precio,
    imagen: juego.imagen,
  };
}

function actualizarNumeroCarrito() {
  let cuenta = 0;
  const items = JSON.parse(localStorage.getItem("juegos"));
  if (items && items.length > 0) {
    cuenta = items.reduce((acum, current) => acum + current.cantidad, 0);
  }
  cuentaCarritoElement.innerText = cuenta;
}

function reiniciarCarrito() {
  localStorage.removeItem("juegos");
  localStorage.setItem("cantidad", 0);
}

function procesarJuego() {
  let imagen = document.getElementById("imagen-juego")?.src;
  let nombre = document.getElementById("nombre-juego")?.innerText;
  let precioTexto = document.getElementById("precio-juego")?.innerText;
  let precio = parseFloat(precioTexto.replace("$", ""));

  // Usamos el nombre como ID única para este ejemplo
  return {
    imagen,
    nombre,
    precio
  };
}

const boton = document.getElementById("boton-agregar-carrito");
if (boton) {
  boton.addEventListener("click", function () {
    const juego = procesarJuego();
    agregarAlCarrito(juego);
  });
}
