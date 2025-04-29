document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");
  
    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });
  
    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        const files = inputElement.files;
        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const extension = file.name.split(".").pop().toLowerCase();
          if (extension === "pdf" || extension === "jpg" || extension === "png") {
            if (extension === "pdf") {
              displayPdfThumbnail(dropZoneElement, file);
            } else {
              addThumbnail(dropZoneElement, file);
            }
            uploadFile(file); // Subir el archivo al modelo de Django
          }
        }
        inputElement.value = ""; // Limpiar el valor del input para permitir subir los mismos archivos varias veces
      }
    });
  
    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });
  
    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });
  
    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
  
      if (e.dataTransfer.files.length) {
        const files = e.dataTransfer.files;
        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const extension = file.name.split(".").pop().toLowerCase();
          if (extension === "pdf" || extension === "jpg" || extension === "png") {
            if (extension === "pdf") {
              displayPdfThumbnail(dropZoneElement, file);
            } else {
              addThumbnail(dropZoneElement, file);
            }
            uploadFile(file); // Subir el archivo al modelo de Django
          }
        }
      }
  
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  
  /**
   * Displays a thumbnail of a PDF file.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function displayPdfThumbnail(dropZoneElement, file) {
    const thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    thumbnailElement.dataset.label = file.name;
    dropZoneElement.appendChild(thumbnailElement);
  
    // Use PDF.js to generate a thumbnail from the PDF file
    const fileReader = new FileReader();
    fileReader.onload = function () {
      const arrayBuffer = this.result;
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      loadingTask.promise.then(function (pdf) {
        pdf.getPage(1).then(function (page) {
          const viewport = page.getViewport({ scale: 0.5 });
          const canvas = document.createElement("canvas");
          const context = canvas.getContext("2d");
          canvas.width = viewport.width;
          canvas.height = viewport.height;
          thumbnailElement.appendChild(canvas);
  
          const renderContext = {
            canvasContext: context,
            viewport: viewport,
          };
          page.render(renderContext).promise.then(function () {
            // Convert the canvas content to a data URL
            const dataUrl = canvas.toDataURL();
            thumbnailElement.style.backgroundImage = `url('${dataUrl}')`;
          });
        });
      });
    };
    fileReader.readAsArrayBuffer(file);
  }
  
  /**
   * Adds a thumbnail for an image file.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function addThumbnail(dropZoneElement, file) {
    const thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    thumbnailElement.dataset.label = file.name;
    dropZoneElement.appendChild(thumbnailElement);
  
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  }
  

  // Función auxiliar para obtener el valor de la cookie CSRF
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Busca la cookie que coincide con el nombre especificado
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  /**
   * Sube un archivo al modelo de Django.
   *
   * @param {File} file
   */
  function uploadFile(file) {
    const url = ""; // Reemplaza con la URL de tu vista de Django
    const formData = new FormData();
    formData.append("files", file);

    const csrftoken = getCookie("csrftoken");
  
    fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrftoken
      }
    })
      .then((response) => response.json())
      .then((data) => {
        // Aquí puedes manejar la respuesta del servidor
        console.log(data);
        file = null;
        File = [];
        const newFormData = new FormData();
      })
      .catch((error) => {
        // Aquí puedes manejar errores en la solicitud
        //console.error("Error al subir el archivo:", error);
        file = null;
        File = [];
        const newFormData = new FormData();        
      });
  }
