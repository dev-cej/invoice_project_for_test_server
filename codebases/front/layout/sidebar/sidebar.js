import { FileUploadDetail } from "../../DTO/detail/FileUploadDetail.js";
import { FileUploadResponse } from "../../DTO/response/FileUploadResponse.js";
import { FileHandleStatus } from "../../constants/FileHandleStatus.js";
import { FileType } from "../../constants/FileType.js";

import { handleAddTable } from "../../page/upload_file/upload.js";

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await loadSidebar();
    setupSidebarInteractions();
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

async function loadSidebar() {
  try {
    const response = await fetch("/layout/sidebar/sidebar.html");
    if (!response.ok) {
      throw new Error(`Failed to load sidebar: ${response.statusText}`);
    }
    const data = await response.text();
    document.querySelector("aside").insertAdjacentHTML("afterbegin", data);
  } catch (error) {
    console.error("Error loading sidebar:", error);
    throw error;
  }
}

function setupSidebarInteractions() {
  const uploadBox = document.getElementById("upload-box");
  const fileInput = document.getElementById("file-input");
  const beforeUpload = document.getElementById("before-upload");
  const afterUpload = document.getElementById("after-upload");
  const fileCountDisplay = document.getElementById("file-count");
  const uploadButton = document.getElementById("upload-button");
  const fileListBox = document.getElementById("file-list-box");
  const loadingSpinner = document.getElementById("loading-spinner");

  setupUploadBoxClick();
  setupUploadButtonClick();

  function setupUploadBoxClick() {
    if (uploadBox && fileInput) {
      uploadBox.addEventListener("click", (event) => {
        if (!event.target.closest("#upload-button")) {
          fileInput.click();
        }
      });
      fileInput.addEventListener("change", handleFileSelection);
    }
  }

  function handleFileSelection(event) {
    const fileCount = fileInput.files.length;
    if (fileCount > 0) {
      beforeUpload.style.display = "none";
      afterUpload.style.display = "flex";
      fileCountDisplay.textContent = `${fileCount} files selected`;
      uploadButton.disabled = !areAllFilesPdf(fileInput.files);
    } else {
      beforeUpload.style.display = "block";
      afterUpload.style.display = "none";
    }
  }

  function setupUploadButtonClick() {
    uploadButton.addEventListener("click", handleUploadFiles);
  }

  async function handleUploadFiles() {
    const files = fileInput.files;

    if (!validateFiles(files)) return;

    // 업로드 버튼 숨기고 로딩 스피너 표시
    uploadButton.style.display = "none";
    loadingSpinner.style.display = "block";

    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append("files[]", file);

        const response = await fetch(
          "https://api.ktainvoice.o-r.kr/upload/upload_file_handler.php",
          {
            method: "POST",
            body: formData,
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
          console.log("response", response);
        }

        const responseToJson = await response.json();
        const fileUploadResponse = new FileUploadResponse(responseToJson);

        if (
          fileUploadResponse.getStatus() === FileHandleStatus.STATUS_SUCCESS
        ) {
          populateFileList(fileUploadResponse.getExtractResult());
        }
      }
    } catch (error) {
      console.error("파일 업로드 오류:", error);
      alert("파일 업로드 중 오류가 발생했습니다.");
    } finally {
      // 업로드 완료 후 로딩 스피너 숨기고 업로드 버튼 표시
      loadingSpinner.style.display = "none";
      uploadButton.style.display = "block";
    }
  }

  function areAllFilesPdf(files) {
    return Array.from(files).every((file) => file.type === "application/pdf");
  }

  function validateFiles(files) {
    if (files.length === 0) {
      alert("파일을 선택하세요.");
      return false;
    }
    if (files.length > 300) {
      alert("최대 50개의 파일만 업로드할 수 있습니다.");
      return false;
    }
    return true;
  }

  function populateFileList(files) {
    files.forEach((file) => {
      const listItem = createListItem(file);
      fileListBox.insertBefore(listItem, fileListBox.firstChild);
      handleAddTable(file);
    });
  }

  function createListItem(file) {
    const listItem = document.createElement("li");
    const icon = document.createElement("img");
    icon.src = getFileTypeIcon(file.getFileType());
    listItem.appendChild(icon);
    listItem.appendChild(document.createTextNode(file.getFileName()));
    return listItem;
  }

  function getFileTypeIcon(fileType) {
    switch (fileType) {
      case FileType.FILE_TYPE_UNKNOWN:
        return "assets/icon/disable_circle.svg";
      case FileType.FILE_TYPE_IMAGE:
        return "assets/icon/error_circle.svg";
      case FileType.FILE_TYPE_TEXT:
        return "assets/icon/check_circle.svg";
      default:
        return "assets/icon/disable_circle.svg";
    }
  }
}
