<?php

class DirectoryHelper {
    /**
     * 디렉토리가 존재하지 않으면 생성하는 함수
     */
    public static function createDirectoryIfNotExists($dir) {
        logGeneralError("createDirectoryIfNotExists");
        if (!file_exists($dir)) {
            // 디렉토리를 생성합니다.
            mkdir($dir, 0777, true);
        }
    }
}