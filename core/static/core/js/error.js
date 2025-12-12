<script>
document.addEventListener('DOMContentLoaded', function () { const overlay = document.getElementById('overlay-alert');
    if (!overlay) return;  // no hay error, no hacemos nada

    const alertBox = overlay.querySelector('.custom-alert');
    if (!alertBox) return;

    const closeBtn = document.getElementById('overlay-alert-close');

    // Aseguramos que el fade-in se aplique después de pintar el DOM
    requestAnimationFrame(function () {
        alertBox.classList.add('fade-in');
    });

    function hideOverlay() {
        // Evitamos re-aplicar si ya se está ocultando
        if (alertBox.classList.contains('fade-out')) return;

        alertBox.classList.remove('fade-in');
        alertBox.classList.add('fade-out');

        // Cuando termina la animación, removemos el overlay
        alertBox.addEventListener('animationend', function () {
            if (overlay && overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, { once: true });
    }

    // Cerrar con la X
    if (closeBtn) {
        closeBtn.addEventListener('click', function (e) {
            e.preventDefault();
            hideOverlay();
        });
    }

    // (Opcional) Autocerrar después de 5s
    // setTimeout(hideOverlay, 5000);
});
</script>