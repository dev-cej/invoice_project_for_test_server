// src/config/configManager.js
import configPromise from "./config.js";

let config = null; // 전역에서 사용 가능하도록 선언

(async function initializeConfig() {
  console.log("🌍 환경 설정을 불러옵니다...");
  config = (await configPromise).default; // 🚀 최초 한 번만 실행
  console.log("✅ 설정 로드 완료:", config.API_URL);
})();

export function getConfig() {
  if (!config) {
    throw new Error("🚨 config가 아직 로드되지 않았습니다!");
  }
  return config;
}
