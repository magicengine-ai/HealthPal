"""
OCR 识别服务
"""
from typing import Optional, List, Dict, Any
import httpx
from app.core.config import settings


class OCRService:
    """OCR 识别服务类"""
    
    def __init__(self):
        """初始化 OCR 服务"""
        self.provider = settings.OCR_PROVIDER
        self.api_key = settings.OCR_API_KEY
        self.api_secret = settings.OCR_API_SECRET
    
    def recognize(self, image_url: str) -> Optional[Dict[str, Any]]:
        """
        OCR 识别（通用文字识别）
        
        Args:
            image_url: 图片 URL 或 Base64
            
        Returns:
            OCR 识别结果字典
        """
        if self.provider == "baidu":
            return self._baidu_ocr(image_url)
        elif self.provider == "tencent":
            return self._tencent_ocr(image_url)
        else:
            # 模拟识别结果（开发环境）
            return self._mock_ocr(image_url)
    
    def _baidu_ocr(self, image_url: str) -> Optional[Dict[str, Any]]:
        """
        百度 OCR 识别
        
        Args:
            image_url: 图片 URL
            
        Returns:
            OCR 识别结果
        """
        # 获取 Access Token
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        token_params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        
        try:
            response = httpx.post(token_url, params=token_params)
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                return None
            
            # 调用 OCR 接口
            ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"image": image_url}
            
            response = httpx.post(ocr_url, headers=headers, data=data)
            result = response.json()
            
            return result
            
        except Exception as e:
            print(f"百度 OCR 识别失败：{e}")
            return None
    
    def _tencent_ocr(self, image_url: str) -> Optional[Dict[str, Any]]:
        """
        腾讯云 OCR 识别
        
        Args:
            image_url: 图片 URL
            
        Returns:
            OCR 识别结果
        """
        # TODO: 实现腾讯云 OCR
        print("腾讯云 OCR 待实现")
        return None
    
    def _mock_ocr(self, image_url: str) -> Dict[str, Any]:
        """
        模拟 OCR 识别结果（开发环境使用）
        
        Args:
            image_url: 图片 URL
            
        Returns:
            模拟的 OCR 识别结果
        """
        return {
            "words_result": [
                {"words": "体检报告"},
                {"words": "姓名：张三"},
                {"words": "性别：男"},
                {"words": "年龄：35"},
                {"words": "白细胞：5.2 x10^9/L"},
                {"words": "红细胞：4.8 x10^12/L"},
                {"words": "血红蛋白：145 g/L"},
            ],
            "words_result_num": 7,
        }
    
    def parse_ocr_result(self, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析 OCR 结果，提取结构化数据
        
        Args:
            ocr_result: OCR 识别原始结果
            
        Returns:
            结构化数据字典
        """
        if not ocr_result or "words_result" not in ocr_result:
            return {}
        
        words_list = ocr_result.get("words_result", [])
        words_text = [item.get("words", "") for item in words_list]
        
        # 提取基本信息
        structured_data = {
            "title": "",
            "name": "",
            "gender": "",
            "age": "",
            "indicators": [],
        }
        
        # 简单解析（实际项目需要更复杂的 NLP 处理）
        for text in words_text:
            if "体检" in text or "报告" in text:
                structured_data["title"] = text
            elif "姓名" in text:
                structured_data["name"] = text.split(":")[-1].strip() if ":" in text else text
            elif "性别" in text:
                structured_data["gender"] = text.split(":")[-1].strip() if ":" in text else text
            elif "年龄" in text:
                structured_data["age"] = text.split(":")[-1].strip() if ":" in text else text
            elif any(kw in text for kw in ["细胞", "蛋白", "指数", "值"]):
                # 尝试解析指标
                indicator = self._parse_indicator(text)
                if indicator:
                    structured_data["indicators"].append(indicator)
        
        return structured_data
    
    def _parse_indicator(self, text: str) -> Optional[Dict[str, str]]:
        """
        解析单个指标
        
        Args:
            text: 指标文本
            
        Returns:
            指标字典或 None
        """
        import re
        
        # 匹配模式：指标名：值 单位
        pattern = r"([\u4e00-\u9fa5\w]+)[:：]?\s*([0-9.]+)\s*([a-zA-Z^/0-9]+)?"
        match = re.search(pattern, text)
        
        if match:
            return {
                "indicator_name": match.group(1),
                "value": match.group(2),
                "unit": match.group(3) or "",
            }
        
        return None
    
    def recognize_table(self, image_url: str) -> Optional[List[Dict[str, Any]]]:
        """
        表格 OCR 识别
        
        Args:
            image_url: 图片 URL
            
        Returns:
            表格数据列表
        """
        # TODO: 实现表格 OCR
        return self.recognize(image_url)
