from dataclasses import dataclass

@dataclass
class PyPositConfig:
    n_bits: int
    es: int


class PyPosit:
    cfg: PyPositConfig
    value: str

    def __init__(self, cfg: PyPositConfig, bit_str: str):
        self.cfg = cfg
        if len(bit_str) != cfg.n_bits:
            raise ValueError(
                f"Bit string of length {len(bit_str)} does not match "
                f"provided configuration value of {cfg.n_bits}.")
        self.value = bit_str

    @classmethod
    def from_float(cls, cfg: PyPositConfig, val: float):
        """Factory method to create bit string from float."""
        return cls(cfg, "")
    
    def __repr__(self) -> str:
        return (f"{self.cfg.n_bits}-bit posit with {self.cfg.es} "
                f"exponent bits, value: {self.value}")
    
    def __str__(self) -> str:
        return self.value
