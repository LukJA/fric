"""Posits in Python. What more can I say?"""

from dataclasses import dataclass
from .operations.arithmetic import bin_add_s, bin_sub_s
from .operations.logic import twoc

@dataclass
class PyPositConfig:
    """Configuration of Posit value: numbers of total and exponent bits."""
    n_bits: int
    es: int  # pylint: disable=C0103

    def __eq__(self, other):
        return self.n_bits == other.n_bits and self.es == other.es


class PyPosit:
    """Python Posit impementation."""

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
    
    @property
    def float_approximation(self) -> float:
        """Return the closest float approximation."""
        return 0.0  # FIXME

    def __setattr__(self, name, value):
        if self.__dict__.get("_locked", False):
            if name == "value" and len(value) != self.cfg.n_bits:
                raise ValueError(
                    f"Bit string of length {len(value)} does not match "
                    f"provided configuration value of {self.cfg.n_bits}.")
            if name == "cfg":
                raise AttributeError("Posit configuration cannot be changed")

        self.__dict__[name] = value

    def __repr__(self) -> str:
        return (f"{self.cfg.n_bits}-bit posit with {self.cfg.es} "
                f"exponent bits, value: {self.value}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        return self.cfg == other.cfg and self.value == other.value
        # FIXME: this doesn't account for any duplicate representations

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")

        return self.__class__(
            cfg=self.cfg,
            bit_str=bin_add_s(self.value, other.value)
        )
    
    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")
        
        self.value = bin_add_s(self.value, other.value)
        return self

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")

        return self.__class__(
            cfg=self.cfg,
            bit_str=bin_sub_s(self.value, other.value)
        )
    
    def __isub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")
        
        self.value = bin_sub_s(self.value, other.value)
        return self

    @property
    def complement(self):
        """Get 2's complement of value as a string."""
        return twoc(self.value, self.cfg.n_bits)

    @property
    def sign(self):
        """Return sign of value."""
        return 1 if self.value[0] == '0' else -1
