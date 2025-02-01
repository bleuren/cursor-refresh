from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import json
import uuid
import random
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """配置類，從環境變數加載參數"""
    STORAGE_PATH: Path = Path.home() / os.getenv('CURSOR_STORAGE_PATH', "Library/Application Support/Cursor/User/globalStorage/storage.json")
    MS_DEVICEID_PATH: Path = Path.home() / os.getenv('MS_DEVICEID_PATH', "Library/Application Support/Microsoft/DeveloperTools/deviceid")
    ADDY_API_KEY: str = os.getenv('ADDY_API_KEY', '')
    ADDY_API_URL: str = os.getenv('ADDY_API_URL', 'https://app.addy.io/api/v1/aliases')
    ALIAS_DESCRIPTION: str = os.getenv('ALIAS_DESCRIPTION', 'cursor')
    ALIAS_DOMAIN: str = os.getenv('ALIAS_DOMAIN', 'anonaddy.me')
    ALIAS_FORMAT: str = os.getenv('ALIAS_FORMAT', 'uuid')
    RECIPIENT_IDS: Optional[List[str]] = None

    def __post_init__(self):
        if not self.ADDY_API_KEY:
            raise ValueError("ADDY_API_KEY environment variable is required")

        recipient_ids = os.getenv('RECIPIENT_IDS')
        if recipient_ids:
            self.RECIPIENT_IDS = [id.strip() for id in recipient_ids.split(',')]

class CursorResetter:
    def __init__(self, config: Config):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.ADDY_API_KEY}",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }

    @staticmethod
    def generate_hex_id(length: int = 64) -> str:
        """生成指定長度的隨機十六進位字串"""
        return ''.join(random.choices('0123456789abcdef', k=length))

    def _handle_ms_deviceid(self) -> str:
        """處理 Microsoft DeviceID，返回新的 device ID"""
        new_device_id = str(uuid.uuid4())
        
        if self.config.MS_DEVICEID_PATH.exists():
            self.config.MS_DEVICEID_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.config.MS_DEVICEID_PATH.write_text(new_device_id)
            logger.info(f"Updated Microsoft DeviceID: {new_device_id}")
            
        return new_device_id

    def update_storage_ids(self) -> None:
        """更新存儲文件中的各種ID"""
        if not self.config.STORAGE_PATH.exists():
            raise FileNotFoundError(f"Storage file not found: {self.config.STORAGE_PATH}")

        data = json.loads(self.config.STORAGE_PATH.read_text())
        required_fields = [
            "telemetry.macMachineId",
            "telemetry.machineId",
            "telemetry.devDeviceId"
        ]

        if not all(field in data for field in required_fields):
            logger.warning("Missing required fields in storage.json")
            return

        logger.info("Original values:")
        for field in required_fields:
            logger.info(f"{field}: {data[field]}")

        data["telemetry.macMachineId"] = self.generate_hex_id()
        data["telemetry.machineId"] = self.generate_hex_id()
        data["telemetry.devDeviceId"] = self._handle_ms_deviceid()

        logger.info("\nUpdated values:")
        for field in required_fields:
            logger.info(f"{field}: {data[field]}")

        self.config.STORAGE_PATH.write_text(json.dumps(data, indent=4))
        logger.info("Storage file updated successfully")

    def manage_addy_aliases(self) -> None:
        """管理 Addy.io 別名"""
        params = {"filter[search]": self.config.ALIAS_DESCRIPTION, "page[size]": 100}
        response = requests.get(self.config.ADDY_API_URL, headers=self.headers, params=params)
        response.raise_for_status()

        aliases = [
            alias for alias in response.json().get("data", [])
            if alias.get("description", "").startswith(self.config.ALIAS_DESCRIPTION)
        ]

        for alias in aliases:
            del_url = f"{self.config.ADDY_API_URL}/{alias['id']}"
            requests.delete(del_url, headers=self.headers).raise_for_status()
            logger.info(f"Deleted alias: {alias.get('email')}")

        payload = {
            "domain": self.config.ALIAS_DOMAIN,
            "description": self.config.ALIAS_DESCRIPTION,
            "format": self.config.ALIAS_FORMAT
        }
        if self.config.RECIPIENT_IDS:
            payload["recipient_ids"] = self.config.RECIPIENT_IDS

        response = requests.post(self.config.ADDY_API_URL, headers=self.headers, json=payload)
        response.raise_for_status()
        
        new_alias = response.json().get("data", {})
        logger.info(f"Created new alias: {new_alias.get('email')}")

def main():
    import os
    os.system("pkill -9 Cursor")
    logger.info("Cursor has been terminated")

    try:
        config = Config()
        resetter = CursorResetter(config)
        resetter.update_storage_ids()
        resetter.manage_addy_aliases()
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()