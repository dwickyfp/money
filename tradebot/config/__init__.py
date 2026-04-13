"""Compatibility facade for the refactored tradebot engine.

The behavior-preserving implementation currently lives in tradebot.engine; this
module provides the planned package boundary for imports while keeping runtime
semantics identical during the modular migration.
"""

from tradebot.engine import *  # noqa: F401,F403
