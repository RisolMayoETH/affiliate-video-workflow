"""Autonomous execution engine for product analysis, strategy selection, and affiliate copy generation."""

from hce.execution.audience_analyzer import AudienceAnalysis, AudienceAnalyzer
from hce.execution.content_generator import (
    AffiliateContentGenerator,
    GeneratedAffiliateContent,
    VideoScene,
)
from hce.execution.product_analyzer import ProductAnalysis, ProductAnalyzer, ProductInput
from hce.execution.strategy_selector import (
    SUPPORTED_PLATFORMS,
    STRATEGIES,
    CreativeStrategy,
    StrategySelector,
)

__all__ = [
    "AffiliateContentGenerator",
    "AudienceAnalysis",
    "AudienceAnalyzer",
    "CreativeStrategy",
    "GeneratedAffiliateContent",
    "ProductAnalysis",
    "ProductAnalyzer",
    "ProductInput",
    "SUPPORTED_PLATFORMS",
    "STRATEGIES",
    "StrategySelector",
    "VideoScene",
]
