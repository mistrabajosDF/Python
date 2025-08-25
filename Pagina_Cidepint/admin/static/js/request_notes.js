$(document).ready(function() {
    $(".btn-primary[data-bs-toggle='modal'][data-bs-target^='#verNotas']").on("click", function() {
        var solicitudId = parseInt($(this).data("bs-id"));
        console.log(solicitudId + " clicked");
        
        var currentURL = window.location.href;
        var ajaxURL = currentURL.replace(/\?.*/, '') + "/notas/" + solicitudId;

        $.ajax({
            url: ajaxURL,  // URL de la función
            type: "GET",
            success: function(data) {
                var notas = data;
                console.log("Notas obtenidas:", notas);
                var modalBody =	$(".modal-body");

                modalBody.empty();

                $.each(notas, function(index, nota) {
                    modalBody.append("<h5>" + nota.description + "</h5>"
                    + "<small>" + nota.inserted_at + "</small>");
                });
            },
            error: function(xhr, status, error) {
                console.log("Error al obtener las notas:", error);
            }
        });
    });
});