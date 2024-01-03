function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var videoPreview = document.getElementById('videoPreview');
            videoPreview.style.backgroundColor = 'black';
            videoPreview.style.display = 'none';

            var videoElement = document.createElement('video');
            videoElement.src = e.target.result;
            videoElement.width = 200;
            videoElement.height = 200; 
            videoElement.controls = true;
            videoElement.autoplay = true;
            videoElement.loop = true;
            videoElement.controls = false;

            // Crear un contenedor div para aplicar la máscara circular
            var circularMaskContainer = document.createElement('div');
            circularMaskContainer.style.width = '192px'; // Ajusta el ancho del contenedor según tus necesidades
            circularMaskContainer.style.height = '192px'; // Ajusta la altura del contenedor según tus necesidades
            circularMaskContainer.style.overflow = 'hidden';
            circularMaskContainer.style.borderRadius = '50%';
            circularMaskContainer.style.position = 'relative';

            // Agregar el video al contenedor de máscara circular
            circularMaskContainer.appendChild(videoElement);

            // Agregar el contenedor de máscara circular al contenedor de vista previa
            videoPreview.innerHTML = '';
            videoPreview.appendChild(circularMaskContainer);

            // Transición de opacidad
            videoPreview.style.transition = 'opacity 0.65s';
            videoPreview.style.opacity = '0';
            videoPreview.style.display = 'block';

            setTimeout(function () {
                videoPreview.style.opacity = '1';
            }, 0);
        };

        reader.readAsDataURL(input.files[0]);
    }
}


document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const videoUpload = document.getElementById("videoUpload");
    const formData = new FormData();

    formData.append("archivo", videoUpload.files[0]);

    fetch("http://localhost:8080/upload", {
        method: "POST",
        body: formData,
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        document.getElementById("apiResponse").innerText = data;
    })
    .catch(error => {
        console.error("Error al enviar la solicitud a la API:", error);
    });
});


document.getElementById('videoUpload').addEventListener('change', function() {
    if (videoUpload.files.length === 0) {
        console.log("Selecciona un archivo de video antes de enviar el formulario.");
    } else{
        console.log('archivo subido');
    }
    readURL(this);
});