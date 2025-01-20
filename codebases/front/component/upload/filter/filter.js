import { getTranslation } from "../../../utils/functions/set_language.js";
import { translationKeys } from "../../../constants/Transitions.js";

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await loadAndSetupFilter();
  } catch (error) {
    console.error("Error loading filter component:", error);
  }
});

export async function loadAndSetupFilter() {
  try {
    const response = await fetch("/component/upload/filter/filter.html");
    if (!response.ok) {
      throw new Error(
        `Failed to load filter component: ${response.statusText}`
      );
    }
    const html = await response.text();
    document.getElementById("filter-container").innerHTML = html;
    setupCompanyFilter();
  } catch (error) {
    console.error("Error loading filter component:", error);
    throw error;
  }
}

function setupCompanyFilter() {
  const companyFilter = document.getElementById("companyFilter");

  //회사 필터 변경 시 이벤트 리스너 설정
  companyFilter.addEventListener("change", () => {
    console.log(companyFilter.value);
    filterResultsByCompany(companyFilter.value);
  });
}

function filterResultsByCompany(code) {
  // 결과 테이블의 모든 테이블 선택
  const tables = document.querySelectorAll(".file-table");
  tables.forEach((table) => {
    // 테이블의 회사 코드 가져오기
    const companyCode = table.dataset.companyCode || "other";
    console.log("companyCode", companyCode);
    console.log("code", code);
    // 선택된 코드와 테이블의 회사 코드가 일치하는지 확인
    if (code === "" || companyCode === code) {
      console.log("일치");
      table.style.display = ""; // 일치하면 테이블을 표시
    } else {
      console.log("불일치");
      table.style.display = "none"; // 일치하지 않으면 테이블을 숨김
    }
  });
}

export function addCompanyOption(code, shortName) {
  const companyFilter = document.getElementById("companyFilter");

  // "미확인 회사" 옵션을 임시로 저장
  const otherOption = companyFilter.querySelector(`option[value="other"]`);
  if (otherOption) {
    companyFilter.removeChild(otherOption);
  }

  // 새로운 옵션 추가
  if (!companyFilter.querySelector(`option[value="${code}"]`)) {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = shortName;
    companyFilter.appendChild(option);
  }

  // "미확인 회사" 옵션을 항상 맨 아래로 추가
  if (otherOption) {
    companyFilter.appendChild(otherOption);
  } else {
    const newOtherOption = document.createElement("option");
    newOtherOption.value = "other";
    newOtherOption.textContent = getTranslation(
      translationKeys.filter.companyFilterOther
    );
    newOtherOption.setAttribute(
      "data-translate",
      translationKeys.filter.companyFilterOther
    );
    companyFilter.appendChild(newOtherOption);
  }
}
