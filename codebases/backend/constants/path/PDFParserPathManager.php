<?php

class PDFParserPathManager {

    public static function getPDFUploadPath() {
        return Env::get('UPLOAD_PATH') . '/pdf/';
    }

    public static function getDecompressedPath() {
        return Env::get('UPLOAD_PATH') . '/decompressed/';
    }

    public static function getHexPath() {
        return Env::get('UPLOAD_PATH') . '/hex/';
    }

}


