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

    // 페이지별로 텍스트 데이터를 처리
    for (const page in data.text_data) {
      const textItems = data.text_data[page];

      // 페이지별 컨테이너 생성
      var pageContainer = document.createElement("div");
      pageContainer.className = "pdf-page"; // 페이지 컨테이너 클래스 설정
      pageContainer.style.marginBottom = "20px"; // 페이지 간격 설정

      // 각 텍스트 객체에서 텍스트를 추출하여 한 줄씩 추가
      textItems.forEach((item) => {
        var textElement = document.createElement("div");
        textElement.className = "pdf-text";
        textElement.style.fontSize = item.font_size + "px"; // 폰트 크기 설정
        textElement.style.whiteSpace = "pre-wrap"; // 줄바꿈 허용
        textElement.style.display = "block"; // 블록 요소로 설정하여 한 줄씩 배치
        textElement.innerText = item.text; // 텍스트 설정

        pageContainer.appendChild(textElement); // 페이지 컨테이너에 추가
      });

      container.appendChild(pageContainer); // 메인 컨테이너에 페이지 컨테이너 추가
    }
  }
}
