function scrollProductos(direccion) {
    const contenedor = document.getElementById("scrollProductos");

    contenedor.scrollBy({
        left: direccion * 300,
        behavior: "smooth"
    });
}
