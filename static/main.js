function scrollProductos(direccion) {
    const contenedor = document.getElementById("scrollProductos");
    const ancho = contenedor.offsetWidth;
    contenedor.scrollBy({ left: direccion * ancho / 2, behavior: 'smooth' });
}