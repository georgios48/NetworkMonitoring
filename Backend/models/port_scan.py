"""Port Scan DTO"""

from typing import Any

from pydantic import BaseModel


class PortScanDTO(BaseModel):
    """Port Scan DTO"""
    number: Any
    port: Any
    ifAlias: Any
    vlan: Any
    In: Any
    Out: Any
    inError: Any
    outError: Any

    def to_dict(self):
        """Convert to dict"""
        return self.model_dump()
