
document.addEventListener("DOMContentLoaded", function () {

  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  const themeToggle = document.getElementById("themeToggle");
  const html = document.documentElement;

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    html.setAttribute("data-bs-theme", "dark");
    const icon = themeToggle.querySelector("i");
    if (icon) icon.className = "bi bi-sun-fill";
  }

  function toggleTheme() {
    const icon = themeToggle.querySelector("i");
    if (html.getAttribute("data-bs-theme") === "dark") {
      html.setAttribute("data-bs-theme", "light");
      localStorage.setItem("theme", "light");
      if (icon) icon.className = "bi bi-moon-fill";
    } else {
      html.setAttribute("data-bs-theme", "dark");
      localStorage.setItem("theme", "dark");
      if (icon) icon.className = "bi bi-sun-fill";
    }
  }

  if (themeToggle) themeToggle.addEventListener("click", toggleTheme);

  const fileInput = document.getElementById("fileInput");
  const uploadForm = document.getElementById("uploadForm");
  const uploadBtn = document.getElementById("uploadBtn");
  const uploadSpinner = document.getElementById("uploadSpinner");
  const uploadText = document.getElementById("uploadText");
  const selectFileBtn = document.getElementById("selectFileBtn");
  const dropArea = document.getElementById("dropArea");
  const changeFileBtn = document.getElementById('changeFileBtn');

  if (uploadBtn) {
    uploadBtn.disabled = true;
  }
  if (selectFileBtn) {
    selectFileBtn.addEventListener("click", (e) => {
      e.preventDefault();
      fileInput.click();
    });
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function handleFileSelect(file) {
    if (!file) return;
    
    const emptyState = dropArea.querySelector('.upload-empty-state');
    const selectedState = dropArea.querySelector('.upload-selected-state');
    const fileNameElement = document.getElementById('selectedFileName');
    const fileSizeElement = document.getElementById('selectedFileSize');
    const fileIcon = document.getElementById('fileTypeIcon');
    
    const fileExt = file.name.split('.').pop().toLowerCase();
    let iconClass = 'bi-file-earmark';
    const fileIcons = {
      'pdf': 'bi-file-earmark-pdf',
      'doc': 'bi-file-earmark-word',
      'docx': 'bi-file-earmark-word',
      'xls': 'bi-file-earmark-excel',
      'xlsx': 'bi-file-earmark-excel',
      'ppt': 'bi-file-earmark-ppt',
      'pptx': 'bi-file-earmark-ppt',
      'zip': 'bi-file-earmark-zip',
      'rar': 'bi-file-earmark-zip',
      'txt': 'bi-file-earmark-text',
      'csv': 'bi-file-earmark-spreadsheet',
      'jpg': 'bi-file-earmark-image',
      'jpeg': 'bi-file-earmark-image',
      'png': 'bi-file-earmark-image',
      'gif': 'bi-file-earmark-image',
    };
    
    if (fileIcons[fileExt]) {
      iconClass = fileIcons[fileExt];
    } else if (file.type.startsWith('image/')) {
      iconClass = 'bi-file-earmark-image';
    }
    
    emptyState.classList.add('d-none');
    selectedState.classList.remove('d-none');
    fileNameElement.textContent = file.name;
    fileSizeElement.textContent = formatFileSize(file.size);
    fileIcon.className = `bi ${iconClass} file-type-icon`;
    uploadBtn.disabled = false;
    dropArea.classList.remove('empty');
  }

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        fileInput.files = e.target.files;
        handleFileSelect(e.target.files[0]);
      }
    });
  }
  
  if (changeFileBtn) {
    changeFileBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      fileInput.click();
    });
  }

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  if (dropArea) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
  }

  function highlight(e) {
    dropArea.classList.add('border-primary');
    dropArea.style.borderStyle = 'solid';
  }

  function unhighlight(e) {
    dropArea.classList.remove('border-primary');
    dropArea.style.borderStyle = 'dashed';
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
      fileInput.files = files;
      handleFileSelect(files[0]);
    }
  }

  if (uploadForm) {
    uploadForm.addEventListener("submit", function (e) {
      if (!fileInput.files || fileInput.files.length === 0) {
        e.preventDefault();
        alert("Por favor, selecciona al menos un archivo para subir.");
        return;
      }

      if (uploadBtn) uploadBtn.disabled = true;
      if (uploadSpinner) uploadSpinner.classList.remove("d-none");
      if (uploadText) uploadText.textContent = "Subiendo...";
    });
  }

  function updateFileDates() {
    document.querySelectorAll(".file-date").forEach((element) => {
      const date = new Date();
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      element.textContent = date.toLocaleDateString("es-ES", options);
    });
  }
  
  updateFileDates();
});

function updateFileDates() {
  const dateElements = document.querySelectorAll(".file-date .date-text");
  const options = { year: "numeric", month: "2-digit", day: "2-digit" };
  const today = new Date().toLocaleDateString("es-ES", options);
  dateElements.forEach((el) => {
    el.textContent = today;
  });
}

document.addEventListener("DOMContentLoaded", function () {
  updateFileDates();
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  const darkModeToggle = document.getElementById("darkModeToggle");
  const themeToggle = document.getElementById("themeToggle");
  const html = document.documentElement;
  const icon = darkModeToggle.querySelector("i");

  const currentTheme = localStorage.getItem("theme") || "light";
  if (currentTheme === "dark") {
    html.setAttribute("data-bs-theme", "dark");
    icon.className = "bi bi-sun-fill";
    themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
  } else {
    html.setAttribute("data-bs-theme", "light");
    icon.className = "bi bi-moon-fill";
    themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
  }

  function toggleTheme() {
    if (html.getAttribute("data-bs-theme") === "dark") {
      html.setAttribute("data-bs-theme", "light");
      localStorage.setItem("theme", "light");
      icon.className = "bi bi-moon-fill";
      themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
    } else {
      html.setAttribute("data-bs-theme", "dark");
      localStorage.setItem("theme", "dark");
      icon.className = "bi bi-sun-fill";
      themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }
    document.documentElement.style.setProperty(
      "--bs-body-bg",
      "var(--light-bg)"
    );
    document.documentElement.style.setProperty(
      "--bs-body-color",
      "var(--text-color)"
    );
  }

  darkModeToggle.addEventListener("click", toggleTheme);
  themeToggle.addEventListener("click", toggleTheme);

  const dropArea = document.getElementById("dropArea");
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const uploadForm = document.getElementById("uploadForm");
  const uploadSpinner = document.getElementById("uploadSpinner");
  const uploadText = document.getElementById("uploadText");
  const selectFileBtn = document.getElementById("selectFileBtn");
  const filePreviews = document.getElementById("filePreviews");
  const uploadPreview = document.getElementById("uploadPreview");
  const addMoreBtn = document.getElementById("addMoreFiles");
  const emptyState = document.querySelector(".upload-empty-state");

  let filesToUpload = [];

  selectFileBtn.addEventListener("click", () => fileInput.click());
  addMoreBtn.addEventListener("click", () => fileInput.click());

  function createFilePreview(file, fileId) {
    const isImage = file.type.startsWith("image/");

    const filePreview = document.createElement("div");
    filePreview.className = "file-preview";
    filePreview.dataset.id = fileId;

    let previewContent = "";
    if (isImage) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = filePreview.querySelector("img");
        if (img) img.src = e.target.result;
      };
      reader.readAsDataURL(file);
      previewContent = '<img src="" alt="" class="preview-thumb">';
    } else {
      const fileExt = file.name.split(".").pop().toLowerCase();
      let iconClass = "bi-file-earmark";

      const fileIcons = {
        pdf: "bi-file-earmark-pdf",
        doc: "bi-file-earmark-word",
        docx: "bi-file-earmark-word",
        xls: "bi-file-earmark-excel",
        xlsx: "bi-file-earmark-excel",
        ppt: "bi-file-earmark-ppt",
        pptx: "bi-file-earmark-ppt",
        zip: "bi-file-earmark-zip",
        rar: "bi-file-earmark-zip",
        txt: "bi-file-earmark-text",
        csv: "bi-file-earmark-spreadsheet",
      };

      if (fileIcons[fileExt]) {
        iconClass = fileIcons[fileExt];
      }

      previewContent = `<div class="file-icon"><i class="bi ${iconClass}"></i></div>`;
    }

    const fileName =
      file.name.length > 30 ? file.name.substring(0, 27) + "..." : file.name;

    filePreview.innerHTML = `
                    ${previewContent}
                    <div class="file-info">
                        <div class="file-name">
                            <input type="text" value="${fileName}" class="form-control form-control-sm" data-original="${
      file.name
    }">
                        </div>
                        <div class="text-muted small">${formatFileSize(
                          file.size
                        )} • ${file.type || "Desconocido"}</div>
                    </div>
                    <div class="file-actions-preview">
                        <button type="button" class="btn btn-sm btn-outline-secondary edit-filename" title="Editar nombre">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger remove-file" title="Eliminar">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;

    const removeBtn = filePreview.querySelector(".remove-file");
    const editBtn = filePreview.querySelector(".edit-filename");
    const nameInput = filePreview.querySelector("input");

    removeBtn.addEventListener("click", () => removeFile(fileId));
    editBtn.addEventListener("click", () => nameInput.focus());

    nameInput.addEventListener("change", (e) => {
      updateFileName(fileId, e.target.value);
    });

    return filePreview;
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function updateFileName(fileId, newName) {
    const fileIndex = filesToUpload.findIndex((f) => f.id === fileId);
    if (fileIndex !== -1) {
      filesToUpload[fileIndex].name = newName;
      updateFileInput();
    }
  }

  function removeFile(fileId) {
    filesToUpload = filesToUpload.filter((f) => f.id !== fileId);
    const fileElement = document.querySelector(`[data-id="${fileId}"]`);
    if (fileElement) {
      fileElement.remove();
    }
    updateFileInput();

    if (filesToUpload.length === 0) {
      showEmptyState();
    }
  }

  function showEmptyState() {
    emptyState.classList.remove("d-none");
    uploadPreview.classList.add("d-none");
    uploadBtn.disabled = true;
    fileInput.value = "";
  }

  function showPreview() {
    emptyState.classList.add("d-none");
    uploadPreview.classList.remove("d-none");
    uploadBtn.disabled = filesToUpload.length === 0;

    const fileCount = filesToUpload.length;
    uploadText.textContent = `Subir ${fileCount} archivo${
      fileCount !== 1 ? "s" : ""
    }`;
  }

  function updateFileInput() {
    const dataTransfer = new DataTransfer();
    filesToUpload.forEach((fileData) => {
      let file = fileData.file;
      if (fileData.name !== fileData.originalName) {
        file = new File([fileData.file], fileData.name, {
          type: fileData.file.type,
          lastModified: fileData.file.lastModified,
        });
      }
      dataTransfer.items.add(file);
    });
    fileInput.files = dataTransfer.files;

    uploadBtn.disabled = filesToUpload.length === 0;
  }

  function handleFiles(selectedFiles) {
    if (selectedFiles.length === 0) return;

    Array.from(selectedFiles).forEach((file) => {
      const fileId = "file-" + Math.random().toString(36).substr(2, 9);
      const fileData = {
        id: fileId,
        file: file,
        name: file.name,
        originalName: file.name,
      };

      filesToUpload.push(fileData);
      const preview = createFilePreview(file, fileId);
      filePreviews.appendChild(preview);

      const removeBtn = preview.querySelector(".remove-file");
      const editBtn = preview.querySelector(".edit-filename");
      const nameInput = preview.querySelector("input");

      removeBtn.addEventListener("click", () => removeFile(fileId));
      editBtn.addEventListener("click", () => nameInput.focus());

      nameInput.addEventListener("change", (e) => {
        updateFileName(fileId, e.target.value);
      });
    });

    showPreview();
    updateFileInput();
  }

  fileInput.addEventListener("change", (e) => {
    handleFiles(e.target.files);
    fileInput.value = "";
  });

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    if (eventName === "drop" || eventName === "dragleave") {
      document.body.addEventListener(eventName, preventDefaults, false);
    }
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => {
        dropArea.classList.add("border-primary");
        dropArea.style.borderStyle = "solid";
      },
      false
    );
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => {
        dropArea.classList.remove("border-primary");
        dropArea.style.borderStyle = "dashed";
      },
      false
    );
  });

  dropArea.addEventListener(
    "drop",
    (e) => {
      e.preventDefault();
      dropArea.classList.remove("border-primary");
      dropArea.style.borderStyle = "dashed";

      const dt = e.dataTransfer;
      const files = dt.files;
      handleFiles(files);
    },
    false
  );

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.add("border-primary");
      dropArea.style.borderStyle = "solid";
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.remove("border-primary");
      dropArea.style.borderStyle = "dashed";
    });
  });

  uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (filesToUpload.length === 0) {
      alert("Por favor, selecciona al menos un archivo para subir.");
      return;
    }

    uploadBtn.disabled = true;
    uploadSpinner.classList.remove("d-none");
    uploadText.textContent = "Subiendo...";

    const formData = new FormData();
    filesToUpload.forEach((fileData, index) => {
      let file = fileData.file;
      if (fileData.name !== fileData.originalName) {
        file = new File([fileData.file], fileData.name, {
          type: fileData.file.type,
          lastModified: fileData.file.lastModified,
        });
      }
      formData.append("file", file);
    });

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url;
        } else {
          return response.json();
        }
      })
      .then((data) => {
        if (data && data.success) {
          window.location.reload();
        } else {
          throw new Error("Error al subir los archivos");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert(
          "Ocurrió un error al subir los archivos. Por favor, inténtalo de nuevo."
        );
        uploadBtn.disabled = false;
        uploadSpinner.classList.add("d-none");
        uploadText.textContent = "Subir archivos";
      });
  });

  function init() {
    filesToUpload = [];
    filePreviews.innerHTML = "";
    showEmptyState();

    fileInput.addEventListener("change", (e) => {
      handleFiles(e.target.files);
      fileInput.value = "";
    });

    document.addEventListener("click", (e) => {
      if (
        e.target.closest(".remove-file") ||
        e.target.closest(".remove-file i")
      ) {
        e.preventDefault();
        const fileItem = e.target.closest(".file-preview");
        if (fileItem) {
          const fileId = fileItem.dataset.id;
          removeFile(fileId);
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();
    uploadBtn.disabled = true;
    uploadSpinner.classList.remove("d-none");
    uploadText.textContent = "Subiendo...";
    dropArea.classList.add("upload-success");

    setTimeout(() => {
      this.submit();
    }, 500);
  });

  window.addEventListener("load", () => {
    dropArea.classList.remove("upload-success");
  });
});
