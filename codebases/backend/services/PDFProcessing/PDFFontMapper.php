class QDFParser {
    private $uploadDir;
    private $qdfOutputDir;
    private $textData;
    private $fontObjectIds;
    private $pageFontMappings;
    // 정규식 상수 정의
    private const PAGE_OBJECT_REGEX = '/%% Page (\d+).*?(<<.*?\s*\/Type \/Page\s*>>)/s';
    
    private const FONT_BLOCK_REGEX = '/\/Font\s*<<\s*(.*?)\s*>>/s';
    private const FONT_REF_REGEX = '/\/(.+?)\s+(\d+)\s+(\d+)\s+R/';
    private const OBJECT_BLOCK_REGEX_TEMPLATE = '/%d %d obj(.*?)endobj/s';
    private const PAGE_CONTENTS_REGEX = '/%% Contents for page (\d+)(.*?)endobj/s';
    private const STREAM_REGEX = '/stream(.*?)endstream/s';
    private const TEXT_BLOCK_REGEX = '/BT([\s\S]*?)ET/s';
    private const UNICODE_RANGE_REGEX = '/1 begincodespacerange\s*<([0-9A-F]+)>\s*<([0-9A-F]+)>/i';
    private const UNICODE_BFCHAR_REGEX = '/beginbfrange(.*?)endbfrange/s';
    private const UNICODE_TOUNICODE_REGEX = '/ToUnicode\s+(\d+)\s+(\d+)\s+R/';
    private const FONT_OPERATOR_REGEX = '/\/([A-Za-z0-9]+)\s+\d+(?:\.\d+)?+\s+Tf/';
    private const UNICODE_BFCHAR_MATCH_REGEX = '/<([0-9A-F]{2,4})>\s*<([0-9A-F]{4})>/i';
    private $fontMappings = [];


  /**
     * PDF 페이지별로 텍스트를 추출하는 함수
     */
    public function extractTextByPage() {
        $pages = [];  // 페이지별 데이터를 저장할 배열

        // `%% Contents for page {n}` 패턴을 찾아 페이지별 분리
        preg_match_all(self::PAGE_CONTENTS_REGEX, $this->textData, $pageMatches);


            // 각 페이지의 시작 위치를 기준으로 페이지별 데이터 추출
            for ($i = 0; $i < count($pageMatches[1]); $i++) {
                $pageNumber = $pageMatches[1][$i];  // 페이지 번호
                $pageContent = $pageMatches[2][$i];  // 해당 페이지의 내용 추출

                // 스트림 데이터 추출
                if (preg_match(self::STREAM_REGEX, $pageContent, $streamMatch)) {
                    $streamData = $streamMatch[1] ?? '';  // stream 내부 데이터 추출
                    // 텍스트 블록 추출
                    if (preg_match_all(self::TEXT_BLOCK_REGEX, $streamData, $textBlocks)) {
                           // 텍스트 블록의 처음 5개만 추출
                            $firstFiveTextBlocks = $textBlocks[1];
                            // 텍스트 블록을 분석하여 페이지별 저장
                            $pages[$pageNumber] = $this->parseTextBlocks($firstFiveTextBlocks, $pageNumber);
                    }
                }
            }

        return $pages;  // 페이지별 추출된 텍스트 데이터 반환
    }

    /**
     * 개별 텍스트 블록을 분석하는 함수
     */
    function parseTextBlocks($blocks, $pageNumber) {
        $parsedTexts = [];
        $currentFont = null;
    
        foreach ($blocks as $block) {
            
            // 🔹 블록을 한 줄씩 나누기
            $lines = explode("\n", $block);

            foreach ($lines as $line) {
                $line = trim($line); // 앞뒤 공백 제거
                // 🔹 폰트(Tf) 찾기
                if (preg_match('/\/([A-Za-z0-9]+)\s+\d+(?:\.\d+)?\s+Tf/', $line, $fontMatch)) {
                    $currentFont = $fontMatch[1]; // 현재 폰트 업데이트
                    continue; // 다음 줄로 이동
                }
    
                // 🔹 Tj 찾기 (같은 줄에서 앞에 있는 데이터 추출)
                if (preg_match('/(?:<([0-9A-Fa-f]+)>|\((.*?)\))\s*Tj/', $line, $tjMatch)) {
                    $text = $this->extractValidText($tjMatch, $currentFont, $pageNumber);
                    
                    $parsedTexts[] = [
                        'font' => $currentFont,
                        'type' => 'Tj',
                        'text' => $text
                    ];

                }
    
                // 🔹 TJ 찾기 (여러 문자열)
                if (preg_match('/\[(.*?)\]\s*TJ/', $line, $tjArrayMatch)) {
                    $text = $this->processTJText($tjArrayMatch[1], $currentFont, $pageNumber);

                    $parsedTexts[] = [
                        'font' => $currentFont,
                        'type' => 'TJ',
                        'text' => $text
                    ];
                }
            }
        }

        logGeneralError("parsedTexts: " . json_encode($parsedTexts));
    
        return $parsedTexts;

    }
    

/**
 * 🔹 HEX 값을 사람이 읽을 수 있는 유니코드 문자로 변환
 */
function convertHexToUnicode($hexString, $currentFont, $pageNumber) {
    
    if (!$currentFont || !isset($this->fontMappings[$pageNumber]['fonts'][$currentFont])) {

        
        return $hexString; // 폰트 매핑이 없으면 원래 문자열 반환
    }

    $fontDetails = json_decode($this->fontMappings[$pageNumber]['fonts'][$currentFont]['details'], true);
    $unicode_content = $fontDetails['unicode_content'] ?? [];
    $unicodeMap = $unicode_content['unicode_content'] ?? [];
    
        $isSingleByte = $unicode_content['is_single_byte'] ?? true;
        $convertedText = '';

  // 🔹 HEX 값을 2자리 또는 4자리씩 분리하여 변환
  $hexValues = str_split($hexString, $isSingleByte ? 2 : 4);
  

  foreach ($hexValues as $hexCode) {
      

      if (isset($unicodeMap[$hexCode])) {
          $convertedText .= $unicodeMap[$hexCode];
          
      } else {
          $convertedText .= '?'; // 매핑이 없으면 '?' 출력
      }
      
  }

  
  return $convertedText;
}


/**
 * 🔹 `TJ`의 여러 텍스트 블록을 처리
 */
function processTJText($tjBlock, $currentFont, $pageNumber) {
    $outputText = '';
    // 🔹 `<HEX>` 또는 `(TEXT)`만 추출
    preg_match_all('/<([0-9A-Fa-f]+)>|\((.*?)\)/', $tjBlock, $matches, PREG_SET_ORDER);
    logGeneralError("matches: " . json_encode($matches));

    foreach ($matches as $match) {
        $text = $this->extractValidText($match, $currentFont, $pageNumber);
        $outputText .= $text;

        
    }

    return $outputText;
}
/**
 * 🔹 `<HEX>` 또는 `(TEXT)`에서 유효한 문자만 추출
 */
function extractValidText($matches, $currentFont, $pageNumber) {

    if (!empty($matches[1])) { 
        // 🔹 `<HEX>` 값 변환
        return $this->convertHexToUnicode($matches[1], $currentFont, $pageNumber);
    }
    
    if (!empty($matches[2])) { 
        // 🔹 `(TEXT)` 값 그대로 반환
        return $matches[2];
    }
    
    return '';
}


    private function extractPageObject() {
        preg_match_all(self::PAGE_OBJECT_REGEX, $this->textData, $pageObjects);
        return $pageObjects;
    }

    private function extractFontMappings() {
        $pageObjects = $this->extractPageObject();
        $pageFontMappings = [];

        foreach ($pageObjects[1] as $index => $pageNumber) {
            $pageObject = $pageObjects[2][$index];
            $fonts = $this->extractFontsFromPageObject($pageObject);
            $pageFontMappings[$pageNumber] = ['fonts' => $fonts];
        }

        $this->pageFontMappings = $pageFontMappings;
        return $pageFontMappings;
    }

    private function extractFontsFromPageObject($pageObject) {
        preg_match(self::FONT_BLOCK_REGEX, $pageObject, $fontMatch);

        $fonts = [];
        if (!empty($fontMatch[1])) {
            preg_match_all(self::FONT_REF_REGEX, $fontMatch[1], $fontRefs);
            

            foreach ($fontRefs[1] as $fontIndex => $fontName) {
                $fonts[$fontName] = [
                    'object_id' => $fontRefs[2][$fontIndex],
                    'index' => $fontRefs[3][$fontIndex],
                    'details' => $this->processObject($fontRefs[2][$fontIndex], $fontRefs[3][$fontIndex])
                ];
                

            }
        }
        return $fonts;
    }

    private function findObjectInPDF($objectId, $index) {
        $objectContent = $this->getObjectContent($objectId, $index);
        return $objectContent;
    }

    private function getObjectContent($objectId, $index) {
        $objectPattern = sprintf('/%d %d obj(.*?)endobj/s', $objectId, $index);
        if (preg_match($objectPattern, $this->textData, $matches)) {
            return $matches[1];
        } else {
            return null;
        }
    }

    private function processObject($objectId, $index) {
        $objectContent = $this->findObjectInPDF($objectId, $index);
        if ($objectContent === null) {
            return null;
        }

        $filteredContent = $this->filterObjectContent($objectContent);
        $unicodeContent = $this->processUnicodeContent($filteredContent);

        $jsonContent = json_encode([
            'object_content' => $filteredContent,
            'unicode_content' => $unicodeContent
        ], JSON_UNESCAPED_UNICODE);

        return $jsonContent;
    }

    private function filterObjectContent($objectContent) {
        $filteredContent = preg_replace('/\/Widths\s*\[.*?\]/s', '', $objectContent);
        return $filteredContent;
    }

    private function processUnicodeContent($filteredContent) {
        if (preg_match(self::UNICODE_TOUNICODE_REGEX, $filteredContent, $unicodeMatch)) {
            
            $unicodeObjectId = $unicodeMatch[1];
            $unicodeIndex = $unicodeMatch[2];
            $unicodeContent = $this->findObjectInPDF($unicodeObjectId, $unicodeIndex);
            return $this->extractUnicodeMappings($unicodeContent);
        }
        return null;
    }

    private function extractUnicodeMappings($content) {
        $unicodeMappings = [];
        $isSingleByte = true; // 기본값: 싱글 바이트 (1바이트 문자)
        if (preg_match(self::UNICODE_RANGE_REGEX, $content, $rangeMatch)) {
            $startRange = hexdec($rangeMatch[1]);
            $endRange = hexdec($rangeMatch[2]);

            // 단일 바이트인지 다중 바이트인지 판단
            $isSingleByte = ($endRange <= 0xFF);

            if (preg_match(self::UNICODE_BFCHAR_REGEX, $content, $bfcharMatch)) {
                $bfcharContent = $bfcharMatch[1];
                preg_match_all(self::UNICODE_BFCHAR_MATCH_REGEX, $bfcharContent, $matches, PREG_SET_ORDER);
                foreach ($matches as $match) {
                    $code = $match[1];
                    $value = hexdec($match[2]);
                    if ($isSingleByte) {
                        // 단일 바이트 처리 (ANSI / WinAnsiEncoding 대응)
                        $encodedValue = mb_convert_encoding(pack('n', $value), 'UTF-8', 'Windows-1252');
                        $unicodeMappings[sprintf($code)] = $encodedValue;
                    } else {
                        // 다중 바이트 처리 (UTF-16BE 기반 변환)
                        if ($value <= 0xFFFF) {
                            // 2바이트 유니코드 변환 (기본)
                            $unicodeMappings[sprintf($code)] = mb_convert_encoding(pack('n', $value), 'UTF-8', 'UTF-16BE');
                        } else {
                            // 3바이트 이상 유니코드 (예: 이모지)
                            $unicodeMappings[sprintf($code)] = mb_convert_encoding(pack('N', $value), 'UTF-8', 'UTF-32BE');
                        }
                    }
                    
                }
            }
        }

        return [
            'unicode_content' => $unicodeMappings,
            'is_single_byte' => $isSingleByte //  싱글 바이트 여부를 저장!
        ];
    }


}