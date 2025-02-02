"""Device Info DTO"""

from typing import Any

from pydantic import BaseModel


class DeviceInfoDTO(BaseModel):
    """Device info DTO"""
    systemOID: Any
    systemDevice: Any
    deviceModel: Any

    def to_dict(self):
        """Convert to dict"""
        return self.model_dump()
