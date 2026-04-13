"""Legacy compatibility module for the refactored tradebot package."""

from __future__ import annotations

import sys
import types

from tradebot import engine as _engine


class _TradeFullProxy(types.ModuleType):
    """Compatibility proxy that forwards attribute writes to the engine."""

    def __getattr__(self, name: str):
        """Function : __getattr__
        Descriptions : Resolve legacy module attributes from the refactored engine.
        Param :
            Param <name> : Attribute name requested from the legacy module.
        """
        return getattr(_engine, name)

    def __setattr__(self, name: str, value) -> None:
        """Function : __setattr__
        Descriptions : Mirror legacy module attribute writes into the engine module.
        Param :
            Param <name> : Attribute name to set.
            Param <value> : Attribute value to assign.
        """
        setattr(_engine, name, value)
        super().__setattr__(name, value)


if __name__ == "__main__":
    _engine.main()
else:
    _module = sys.modules[__name__]
    _module.__class__ = _TradeFullProxy
    globals().update(_engine.__dict__)
