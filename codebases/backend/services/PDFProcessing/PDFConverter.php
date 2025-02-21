<?php
require_once Env::get('BACKEND_CONSTANTS_PATH') . '/path/PDFParserPathManager.php';

// 정규식 상수 정의


class PDFConverter {
    private $textData;
    private $hexData;
    private const OBJECT_REGEX = '/(\d+\s+\d+\s+obj\b[\s\S]+?endobj)/';
    private const HEX_OBJECT_REGEX = '/([0-9A-Fa-f]{2}(?:20|0A|0D0A)+[0-9A-Fa-f]{2}(?:20|0A|0D0A)+6F626A(?:20|0A|0D0A)+(?:[0-9A-Fa-f]{2})+?(?:20|0A|0D0A)+656E646F626A)/i';
    private const FILTER_REGEX = '/\/Filter\s*\/([A-Za-z0-9]+)/';
    // /Filter\s+(?:\[\s*([\s\S]+?)\s*\]|\s*([/\w\d]+))(?=\s|>>|$)
    private const HEX_FILTER_REGEX = '/2f46696c746572(?:20|0A|0D0A)+2f([0-9A-Fa-f]+?)(?=20|0A|0D0A|3E)/i';
    private const LENGTH_REGEX = '/\/Length\s+(\d+|\d+\s+\d+\s+R)/';


    private const HEX_LENGTH_REGEX = '/2F4C656E677468(?:20|0A|0D0A)+((?:[0-9A-Fa-f]{2}(?:20|0A|0D0A)*)+?(?=:52(?:20|0A|0D0A)*)?|(?:[0-9A-Fa-f]{2})+?)(?=20|0A|0D0A|3E)/i';
    // private const HEX_LENGTH_REGEX = 
    // '/2F4C656E677468(?:20|0A|0D0A)+
    // (

    //     (

    //     ?:[0-9A-Fa-f]{2}
    //     (?:20|0A|0D0A)*

    //     )
    
    //     +(?:20|0A|0D0A)+52|

    //     (
        
    //     ?:[0-9A-Fa-f]{2}
        
        
    //     )+
    
    // )
    
    // )

    // (?=20|0A|0D0A|3E)
    
    // /i';
    private const STREAM_REGEX = '/stream\s*(.*?)\s*endstream/s';
    private const HEX_STREAM_REGEX = '/73747265616d(?:20|0A|0D0A)+(.*?)(?:20|0A|0D0A)+*656e6473747265616d/s';

    public function __construct($hexPath) {
        $this->hexData = $this->extractTextFromHex($hexPath);
    }

    public function extractTextFromPDF($pdfPath) {
        return file_get_contents($pdfPath);
    }
    
    public function extractTextFromHex($hexPath) {
        $textData = file_get_contents($hexPath);
        return $textData;
    }

    private function filterEmptyMatches($matches) {
        
        return array_filter($matches, function($match) {
            logGeneralError("match contents: " . json_encode($match));
            
            // 각 요소를 개별적으로 확인
            foreach ($match as $key => $value) {
                logGeneralError("Key: $key, Value: " . var_export($value, true));
            }
            
            $containsNull = in_array(null, $match, true);
            logGeneralError("in_array(null, true): " . ($containsNull ? 'true' : 'false'));
            
            // $match 배열에 null이 하나라도 있으면 false를 반환하여 제거
            return !$containsNull;
        });
    }

    public function handleConvertHexToText() {
        logGeneralError("handleConvertHexToText: ");
        preg_match_all(self::HEX_OBJECT_REGEX, $this->hexData, $hexObjectMatches, PREG_SET_ORDER);
        logGeneralError("hexObjectMatches: " . json_encode($hexObjectMatches));

        foreach ($hexObjectMatches as $hexObjectMatch) {
            $objectContent = $hexObjectMatch[1];
            // logGeneralError("!!!!!!!!!!!!!!!!!!!!!!!!objectContent: \n" . $objectContent);

            if (!preg_match(self::HEX_FILTER_REGEX, $objectContent, $filterMatch)) {
            logGeneralError("++++++++++++objectContent: " . $objectContent);
                logGeneralError("filterMatch: 난 압축 안되는 놈");
                continue;
            }
            $filter = $filterMatch[1];


            if (!preg_match(self::HEX_LENGTH_REGEX, $objectContent, $lengthMatch)) {
                logGeneralError("lengthMatch: lengthMatch 못찾음");
                continue;

            }
            // logGeneralError("lengthMatch: " . json_encode($lengthMatch));
            $length = (int)$lengthMatch[1];

            // if (!preg_match(self::HEX_STREAM_REGEX, $objectContent, $streamMatch)) {
            //     continue;
            // }
            // $streamData = substr($streamMatch[1], 0, $length);

            // $decodedData = $this->decodeStreamData($streamData, $filter);
            // logGeneralError("Decoded Data: " . $decodedData);
        }

    }

    public function convertToAnalyzableFormat($pdfPath) {
        // 객체를 찾기 위한 정규식
        preg_match_all(self::OBJECT_REGEX, $this->textData, $objectMatches, PREG_SET_ORDER);
        // 빈 문자열이나 null 값을 포함하는 항목 제거
        $filteredMatches = $this->filterEmptyMatches($objectMatches);
        logGeneralError("Filtered objectMatches: " . json_encode($filteredMatches, JSON_PARTIAL_OUTPUT_ON_ERROR));

        foreach ($filteredMatches as $objectMatch) {
            $objectContent = $objectMatch[2];

            if (!preg_match(self::FILTER_REGEX, $objectContent, $filterMatch)) {
                continue;
            }
            $filter = $filterMatch[1];

            if (!preg_match(self::LENGTH_REGEX, $objectContent, $lengthMatch)) {
                continue;
            }
            $length = (int)$lengthMatch[1];

            if (!preg_match(self::STREAM_REGEX, $objectContent, $streamMatch)) {
                continue;
            }
            $streamData = substr($streamMatch[1], 0, $length);

            $decodedData = $this->decodeStreamData($streamData, $filter);
            logGeneralError("Decoded Data: " . $decodedData);
        }
    }

    private function decodeStreamData($data, $filter) {
        switch ($filter) {
            case 'ASCIIHexDecode':
                return $this->decodeASCIIHex($data);
            case 'FlateDecode':
                return $this->decodeFlate($data);
            default:
                return "decodeStreamData 실패";
        }
    }

    private function convertHexToUtf8($hexData) {
        $binaryData = '';
        for ($i = 0; $i < strlen($hexData); $i += 2) {
            $binaryData .= chr(hexdec(substr($hexData, $i, 2)));
        }
        return mb_convert_encoding($binaryData, 'BASE64', 'ISO-8859-1');
    }

    private function decodeFlate($data) {
        $decompressed = @zlib_decode($data);
        if ($decompressed === false) {
            logGeneralError("FlateDecode 압축 해제 실패");
            return "압축 해제 실패";
        }
        return $decompressed;
    }

    private function decodeASCIIHex($data) {
        return pack('H*', preg_replace('/[^0-9A-Fa-f]/', '', $data));
    }
}
