import {
  addCompanyOption,
  loadAndSetupFilter,
} from "../../component/upload/filter/filter.js";
import { getTranslation } from "../../utils/functions/set_language.js";
import { translationKeys } from "../../constants/Transitions.js";

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await loadUploadResult();
    await loadAndSetupFilter();
    setupUploadResultInteractions();
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

async function loadUploadResult() {
  try {
    const response = await fetch("/page/upload_file/upload.html");
    if (!response.ok) {
      throw new Error(`Failed to load sidebar: ${response.statusText}`);
    }
    const data = await response.text();
    document
      .querySelector(".upload-result-container")
      .insertAdjacentHTML("afterbegin", data);
  } catch (error) {
    console.error("Error loading sidebar:", error);
    throw error;
  }
}

function setupUploadResultInteractions() {
  const resultTableBody = document.getElementById("resultTableBody");
  const downloadButton = document.getElementById("downloadCsvButton");

  const tabs = document.querySelectorAll(".tab-button");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      showTab(tab.id);
    });
  });

  if (downloadButton) {
    downloadButton.addEventListener("click", downloadCSV);
  }
}

function formatDateToYYYYMMDD(dateString) {
  // 날짜 형식이 'DD/MM/YYYY'인 경우 처리
  const [day, month, year] = dateString.split("/");
  const date = new Date(`${year}-${month}-${day}`);

  const formattedYear = date.getFullYear();
  const formattedMonth = String(date.getMonth() + 1).padStart(2, "0");
  const formattedDay = String(date.getDate()).padStart(2, "0");

  return `${formattedYear}-${formattedMonth}-${formattedDay}`;
}

export function createDynamicRows(file) {
  const originalDate = file.getInvoiceDate().getSelectedCandidate();
  const formattedDate = formatDateToYYYYMMDD(originalDate);

  const rows = [
    {
      label: getTranslation(translationKeys.tableFileName),
      data_translate: translationKeys.tableFileName,
      value: file.getFileName(),
      editable: false,
      className: "file-link",
    },
    {
      label: getTranslation(translationKeys.tableStatus),
      data_translate: translationKeys.tableStatus,
      value: file.getStatus(),
      editable: false,
    },
    {
      label: getTranslation(translationKeys.tableFileType),
      data_translate: translationKeys.tableFileType,
      value: file.getFileType(),
      editable: false,
    },
    {
      label: getTranslation(translationKeys.tableCaseNumber),
      data_translate: translationKeys.tableCaseNumber,
      value: file.getCaseNumber().getSelectedCandidate(),
      editable: true,
    },
    {
      label: getTranslation(translationKeys.tableMasterNameCode),
      data_translate: translationKeys.tableMasterNameCode,
      value: getPayerCompanyInfo(file),
      editable: true,
    },
    {
      label: getTranslation(translationKeys.tableInvoiceDate),
      data_translate: translationKeys.tableInvoiceDate,
      value: originalDate,
      editable: true,
      inputType: "date",
      inputValue: formattedDate,
    },
    {
      label: getTranslation(translationKeys.tableInvoiceNumber),
      data_translate: translationKeys.tableInvoiceNumber,
      value: file.getInvoiceNumber().getSelectedCandidate(),
      editable: true,
    },
    {
      label: getTranslation(translationKeys.tableAmountBilled),
      data_translate: translationKeys.tableAmountBilled,
      value: getAmountBilledInfo(file),
      editable: true,
    },
  ];

  return rows
    .map((row) => {
      if (row.editable) {
        const inputType = row.inputType || "text";
        const inputValue = row.inputValue || row.value;
        return `
            <tr>
              <td data-translate="${row.data_translate}">${row.label}</td>
              <td>${row.value}</td>
              <td><input type="${inputType}" value="${inputValue}" class="editable-input" /></td>
            </tr>
          `;
      } else {
        return `
            <tr>
              <td data-translate="${row.data_translate}">${row.label}</td>
              <td class="${row.className}">${row.value}</td>
              <td>${row.value}</td>
            </tr>
          `;
      }
    })
    .join("");
}

export function handleAddTable(file) {
  const resultTableBody = document.getElementById("resultTableBody");
  const tableHTML = createDynamicTable(file);
  resultTableBody.insertAdjacentHTML("afterbegin", tableHTML);
  const newFileLink = resultTableBody.querySelector(
    `tr:first-child .file-link`
  );

  addFileLinkClickListener(newFileLink, file.getFileName());

  // 회사 정보 가져오기
  const matchedCandidate = file.getPayerCompany().getMatchedCandidate();
  if (matchedCandidate) {
    const masterData = matchedCandidate.getMatchedMasterData();
    const code = masterData.getCode();
    const shortName = masterData.getShortName();
    addCompanyOption(code, shortName); // 필터 옵션 추가
  }
}

export function createDynamicTable(file) {
  const matchedCandidate = file.getPayerCompany().getMatchedCandidate();
  const companyCode = matchedCandidate
    ? matchedCandidate.getMatchedMasterData().getCode()
    : "other"; // 회사 코드가 없으면 "기타"로 설정
  return `
      <table class="file-table" data-company-code="${companyCode}">
        <thead>
          <tr>
            <th data-translate="${translationKeys.tableField}">${getTranslation(
    translationKeys.tableField
  )}</th>
            <th data-translate="${
              translationKeys.tableExtracted
            }">${getTranslation(translationKeys.tableExtracted)}</th>
            <th data-translate="${
              translationKeys.tableReviewed
            }">${getTranslation(translationKeys.tableReviewed)}</th>
          </tr>
        </thead>
        <tbody>
          ${createDynamicRows(file)}
        </tbody>
      </table>
    `;
}

function getAmountBilledInfo(file) {
  try {
    const selectedCandidate = file.getAmountBilled().getSelectedCandidate();
    if (!selectedCandidate || selectedCandidate.length === 0) {
      console.warn("No selected candidate found for amount billed.");
      return "-"; // 기본값 반환
    }
    return selectedCandidate[0].getAmount();
  } catch (error) {
    console.error("Error retrieving amount billed info:", error);
    return "-"; // 기본값 반환
  }
}

function getPayerCompanyInfo(file) {
  const matchedCandidate = file.getPayerCompany().getMatchedCandidate();
  if (!matchedCandidate) return "N/A";

  const masterData = matchedCandidate.getMatchedMasterData();
  // (${masterData.getName()}, ${masterData.getCurrency()})
  // ( ${matchedCandidate.getMatchedPhrase()})
  return `${masterData.getShortName()} : ${masterData.getCode()} `;
}

function addFileLinkClickListener(linkElement, fileName) {
  if (linkElement) {
    linkElement.addEventListener("click", (event) => {
      event.preventDefault(); // 기본 동작 방지
      console.log("Clicked file link:", fileName); // 디버깅 로그
      openPdfInViewer(fileName); // PDF 뷰어 열기
    });
  }
}

async function openPdfInViewer(fileName) {
  const pdfViewer = document.getElementById("pdfViewer");
  const dragBar = document.getElementById("dragBar");

  // 기본 이름 준비
  const baseName = fileName.replace(/\.pdf$/i, "");
  const highlightedFileName = `${baseName}_highlighted.pdf`;

  // 경로 목록 정의
  const paths = [
    `/uploads/highlight/${encodeURIComponent(highlightedFileName)}`,
    `/uploads/pdfs/${encodeURIComponent(fileName)}`,
  ];

  // 순차적으로 파일 존재 여부 확인
  for (const path of paths) {
    try {
      const response = await fetch(path, { method: "HEAD" });
      if (response.ok) {
        pdfViewer.src = path;
        pdfViewer.style.display = "block";
        dragBar.style.display = "block";
        return;
      }
    } catch (error) {
      console.log(`경로 확인 중 에러 발생: ${path}`, error);
    }
  }

  // 모든 경로가 실패한 경우
  console.error("PDF 파일을 찾을 수 없습니다.");
  alert("PDF 파일을 찾을 수 없습니다.");
}

function downloadCSV() {
  const downloadButton = document.getElementById("downloadCsvButton");

  // 버튼 비활성화 및 로딩 인디케이터 표시
  downloadButton.disabled = true;

  const resultTableBody = document.getElementById("resultTableBody");
  const tables = resultTableBody.querySelectorAll(".file-table");
  let csvContent = "\uFEFF"; // UTF-8 BOM 추가

  // CSV 헤더 정의
  const headers = [
    getTranslation(translationKeys.tableFileName),
    getTranslation(translationKeys.tableCaseNumber),
    getTranslation(translationKeys.tableMasterNameCode),
    getTranslation(translationKeys.tableInvoiceDate),
    getTranslation(translationKeys.tableInvoiceNumber),
    getTranslation(translationKeys.tableAmountBilled),
  ];
  csvContent += headers.join(",") + "\r\n";

  tables.forEach((table) => {
    const rowData = extractTableData(table);
    csvContent += formatCSVRow(rowData, headers);
  });

  // CSV 파일 다운로드
  const encodedUri = encodeURI("data:text/csv;charset=utf-8," + csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "INVOICE必要項目データ(company).csv");
  document.body.appendChild(link);

  // 다운로드 링크 클릭
  link.click();

  // 일정 시간 후 버튼 활성화
  setTimeout(() => {
    enableDownloadButton(downloadButton);
  }, 1000); // 3초 후에 버튼을 활성화
}

function enableDownloadButton(downloadButton) {
  downloadButton.disabled = false;
}

function extractTableData(table) {
  const rows = table.querySelectorAll("tbody tr");
  const rowData = {};

  rows.forEach((row) => {
    const cols = row.querySelectorAll("td");
    if (cols.length > 0) {
      const fieldName = cols[0].innerText.trim();
      const value = extractValue(cols[2]);
      rowData[fieldName] = value;
    }
  });

  return rowData;
}

function extractValue(column) {
  const inputElement = column.querySelector("input");
  return inputElement ? inputElement.value.trim() : column.innerText.trim();
}

function formatCSVRow(rowData, headers) {
  return (
    headers
      .map((header) => {
        const value = rowData[header] || "";
        return `"${value.replace(/"/g, '""')}"`;
      })
      .join(",") + "\r\n"
  );
}
