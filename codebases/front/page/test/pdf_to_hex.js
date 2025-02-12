import { getConfig } from "../../config/configManager.js";

// DOM이 로드되면 이벤트 리스너 설정
document.addEventListener("DOMContentLoaded", function () {
  setupUploadButtonClick();
});

function setupUploadButtonClick() {
  const uploadButton = document.getElementById("upload-button");
  uploadButton.addEventListener("click", uploadPDF);

  // PDF 업로드 함수

  async function uploadPDF() {
    const fileInput = document.getElementById("pdf-upload");
    const file = fileInput.files[0];

    if (!file) {
      alert("PDF 파일을 선택해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf_file", file);

    try {
      const CONFIG = getConfig();
      const response = await fetch(CONFIG.API_URL + "test/pdf_to_hex", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("업로드 실패");
      }

      const data = await response.json();
      renderPDFText(data);
    } catch (error) {
      alert("파일 업로드 중 오류가 발생했습니다: " + error.message);
    }
  }

  // PDF 텍스트 렌더링 함수
  function renderPDFText(data) {
    var container = document.getElementById("pdf-viewer");
    container.innerHTML = ""; // 기존 내용 초기화

    data.forEach((item) => {
      var textElement = document.createElement("div");
      textElement.className = "pdf-text";
      textElement.style.left = item.x + "px";
      textElement.style.top = 1000 - item.y + "px";
      textElement.style.fontSize = item.font_size + "px";
      textElement.innerText = item.text;

      container.appendChild(textElement);
    });
  }
}
