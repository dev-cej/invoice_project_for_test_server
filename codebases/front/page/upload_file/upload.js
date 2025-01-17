import {
  addCompanyOption,
  loadAndSetupFilter,
} from "../../component/upload/filter/filter.js";
import { getTranslation } from "../../utils/functions/set_language.js";
import { translationKeys } from "../../constants/Transitions.js";
import { FileType } from "../../constants/FileType.js";

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await loadUploadResult();
    await loadAndSetupFilter();
    setupUploadResultInteractions();
  } catch (error) {
    console.error("Initialization error:", error);
  }
});

const UPLOAD_HTML_PATH = "/page/upload_file/upload.html";
const EXTRACTED_DATA_HTML_PATH = "/template/upload/extracted_data_table.html";

async function loadUploadResult() {
  try {
    const [data, data2] = await Promise.all([
      fetchHTML(UPLOAD_HTML_PATH),
      fetchHTML(EXTRACTED_DATA_HTML_PATH),
    ]);

    insertHTMLToContainer(".upload-result-container", data, data2);
  } catch (error) {
    console.error("Error loading upload result:", error);
  }
}

async function fetchHTML(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Failed to load HTML from ${path}: ${response.statusText}`);
  }
  return response.text();
}

function insertHTMLToContainer(containerSelector, ...htmlContents) {
  const container = document.querySelector(containerSelector);
  htmlContents.forEach((html) => {
    container.insertAdjacentHTML("afterbegin", html);
  });
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
  const rows = getRowData(file);
  const fragment = document.createDocumentFragment();
  const template = document.getElementById("row-template");

  rows.forEach((row) => {
    const clone = template.content.cloneNode(true);
    populateRow(clone, row);
    fragment.appendChild(clone);
  });

  return fragment;
}

function getRowData(file) {
  const originalDate = file.getInvoiceDate().getSelectedCandidate();
  const formattedDate = formatDateToYYYYMMDD(originalDate);

  return [
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
}

function populateRow(clone, row) {
  const tds = clone.querySelectorAll("td");
  tds[0].setAttribute("data-translate", row.data_translate);
  tds[0].textContent = row.label;
  tds[1].textContent = row.value;

  if (row.editable) {
    const input = tds[2].querySelector("input");
    input.type = row.inputType || "text";
    input.value = row.inputValue || row.value;
  } else {
    tds[2].textContent = row.value;
  }
}

export function handleAddTable(file) {
  const resultTableBody = document.getElementById("resultTableBody");
  const tableElement = createDynamicTable(file);
  resultTableBody.insertBefore(tableElement, resultTableBody.firstChild);
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

function getFileTypeIcon(fileType) {
  switch (fileType) {
    case FileType.FILE_TYPE_UNKNOWN:
      return "file_type_unknown ";
    case FileType.FILE_TYPE_IMAGE:
      return "file_type_image";
    case FileType.FILE_TYPE_TEXT:
      return "file_type_text";
    default:
      return "file_type_unknown";
  }
}

export function createDynamicTable(file) {
  // 파일의 회사 코드 가져오기
  const matchedCandidate = file.getPayerCompany().getMatchedCandidate();
  const companyCode = matchedCandidate
    ? matchedCandidate.getMatchedMasterData().getCode()
    : "other"; // 회사 코드가 없으면 "기타"로 설정

  // 테이블 템플릿 복제
  const template = document.getElementById("table-template");
  const clone = template.content.cloneNode(true);
  const table = clone.querySelector(".file-table-container");
  table.setAttribute("data-company-code", companyCode);

  // 파일 링크 설정
  const fileLink = clone.querySelector(".file-link");
  fileLink.classList.add(getFileTypeIcon(file.getFileType()));
  fileLink.textContent = file.getFileName();

  // 테이블 헤더 설정
  const ths = clone.querySelectorAll("th");
  ths[0].setAttribute("data-translate", translationKeys.tableField);
  ths[0].textContent = getTranslation(translationKeys.tableField);
  ths[1].setAttribute("data-translate", translationKeys.tableExtracted);
  ths[1].textContent = getTranslation(translationKeys.tableExtracted);
  ths[2].setAttribute("data-translate", translationKeys.tableReviewed);
  ths[2].textContent = getTranslation(translationKeys.tableReviewed);

  // 테이블 본문에 동적으로 생성된 행 추가
  const tbody = clone.querySelector("tbody");
  tbody.appendChild(createDynamicRows(file));

  // Alternative data 추가
  const alternativeDataContent = clone.querySelector(
    ".alternative-data-content"
  );
  const alternativeData = createAlternativeData(file);
  alternativeDataContent.appendChild(alternativeData);

  return table;
}

function createAlternativeData(file) {
  const fragment = document.createDocumentFragment();

  const alternativeItems = [
    {
      title: "CASE NUMBER",
      data: file.getCaseNumber().getAlternativeOptions(),
    },
    {
      title: "PAYER NAME",
      data: file
        .getPayerCompany()
        .getAlternativeOptions()
        .map((option) => option.getMatchedPhrase()),
    },
    {
      title: "INVOICE DATE",
      data: file.getInvoiceDate().getAlternativeOptions(),
    },
    {
      title: "INVOICE NUMBER",
      data: file.getInvoiceNumber().getAlternativeOptions(),
    },
    {
      title: "AMOUNT",
      data: file
        .getAmountBilled()
        .getAlternativeOptions()
        .map((option) => `${option.getAmount()} ${option.getCurrency()}`),
    },
  ];

  alternativeItems.forEach((item) => {
    if (!Array.isArray(item.data)) {
      console.error(`Data for ${item.title} is not an array:`, item.data);
      return;
    }

    const itemBox = document.createElement("div");
    itemBox.classList.add("alternative-item-box");

    const itemTitle = document.createElement("span");
    itemTitle.classList.add("alternative-title");
    itemTitle.textContent = item.title;
    itemBox.appendChild(itemTitle);

    const contentBox = document.createElement("div");
    contentBox.classList.add("alternative-content-box");

    item.data.forEach((data) => {
      const dataSpan = document.createElement("span");
      dataSpan.classList.add(
        `alternative-data`,
        `alternative-${item.title.toLowerCase().replace(" ", "-")}`
      );
      dataSpan.textContent = data;
      contentBox.appendChild(dataSpan);
    });

    itemBox.appendChild(contentBox);
    fragment.appendChild(itemBox);
  });

  return fragment;
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

  rowData[getTranslation(translationKeys.tableFileName)] = table
    .querySelector(".file-link")
    .textContent.trim();

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
