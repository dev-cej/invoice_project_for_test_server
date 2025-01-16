<?php
header('Content-Type: application/json');
require_once('/var/www/html/invoiceProject/codebases/backend/config/config.php');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if ($data === null || !isset($data['fileName']) || !isset($data['phrases'])) {
        echo json_encode(['status' => 'error', 'message' => '잘못된 입력 데이터']);
        exit;
    }

    $fileName = $data['fileName'];
    $phrases = $data['phrases'];
    $pdfFilePath = "/var/www/html/invoiceProject/uploads/pdfs/" . $fileName;
    $highlightScriptPath = "/var/www/html/invoiceProject/codebases/backend/api/extract/highlight_text.py";

    try {
        // 하이라이트 스크립트 실행
        $highlightCommand = escapeshellcmd("$pythonPath $highlightScriptPath $pdfFilePath " . escapeshellarg(json_encode($phrases)) . " 2>&1");
        $highlightOutput = shell_exec($highlightCommand);
        logGeneralError("하이라이트 스크립트 실행 결과: " . $highlightOutput);

        echo json_encode(['status' => 'success', 'message' => '하이라이트 완료']);
    } catch (Exception $e) {
        logGeneralError("하이라이트 처리 중 예외 발생: " . $e->getMessage());
        echo json_encode(['status' => 'error', 'message' => '하이라이트 처리 중 오류 발생: ' . $e->getMessage()]);
    }
}
?>