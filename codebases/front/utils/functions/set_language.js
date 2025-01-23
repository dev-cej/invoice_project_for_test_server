import { TRANSLATIONS } from "../../constants/Transitions.js";
// 언어를 설정하는 함수
function setLanguage(language) {
  console.log(`Setting language to: ${language}`);
  const elements = document.querySelectorAll("[data-translate]");

  // 각 요소에 대해 번역된 텍스트를 설정
  elements.forEach((element) => {
    const key = element.getAttribute("data-translate");
    element.textContent = TRANSLATIONS[language][key] || key;
  });

  // 언어에 따라 폰트 변경
  if (language === "ja") {
    document.documentElement.style.setProperty(
      "--font-family",
      '"NotoSansJP", sans-serif'
    );
  } else {
    document.documentElement.style.setProperty(
      "--font-family",
      '"Pretendard", sans-serif'
    );
  }
}

export function getLanguage() {
  const languageSelector = document.getElementById("languageSelector");
  const selectedLanguage = languageSelector.value;
  return selectedLanguage;
}

// 특정 번역 키에 대한 값을 가져오는 함수
export function getTranslation(key, defaultValue = "") {
  const languageSelector = document.getElementById("languageSelector");
  const selectedLanguage = languageSelector.value || "en";
  return TRANSLATIONS[selectedLanguage]?.[key] ?? defaultValue;
}

// 언어 선택 드롭다운에 이벤트 리스너 추가
document
  .getElementById("languageSelector")
  .addEventListener("change", function () {
    const selectedLanguage = this.value;
    setLanguage(selectedLanguage);
  });

// 페이지의 모든 리소스가 로드된 후 초기 언어 설정
window.onload = function () {
  setLanguage("ja");
};
