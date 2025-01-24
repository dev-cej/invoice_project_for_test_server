// src/config/config.js
let configPromise = null; // 한 번만 실행되도록 캐싱

if (!configPromise) {
  if (window.location.hostname === "test.ktainvoice.o-r.kr") {
    console.log("🌍 개발 환경 설정 로드");
    configPromise = import("./config.development.js");
  } else {
    console.log("🚀 프로덕션 환경 설정 로드");
    configPromise = import("./config.production.js");
  }
}

export default configPromise;
