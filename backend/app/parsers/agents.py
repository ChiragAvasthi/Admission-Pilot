from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentAnalysisResult(BaseModel):
    college_profile: str = Field(description="Summary of the college profile.")
    courses_offered: List[str] = Field(description="List of courses extracted from the document.")
    facilities: List[str] = Field(description="List of facilities available.")
    placements: str = Field(description="Information regarding placements.")
    vision: str = Field(description="Vision of the institution.")
    mission: str = Field(description="Mission of the institution.")
    past_campaigns: List[str] = Field(description="Mentions of past campaigns or reports.")
    confidence_score: float = Field(description="Confidence in the extraction accuracy.")

class WebsiteAuditResult(BaseModel):
    strengths: List[str] = Field(description="Strengths of the website.")
    weaknesses: List[str] = Field(description="Weaknesses of the website.")
    improvement_suggestions: List[str] = Field(description="Suggestions for improvement.")
    priority_issues: List[str] = Field(description="High-priority issues to address immediately.")
    mobile_responsiveness: str = Field(description="Assessment of mobile responsiveness.")
    confidence_score: float = Field(description="Confidence score of the analysis.")

class CompetitorAnalysisResult(BaseModel):
    competitor_matrix: Dict[str, Any] = Field(description="Matrix comparing courses, fees, placements, etc.")
    strengths: List[str] = Field(description="Strengths of competitors relative to the client.")
    weaknesses: List[str] = Field(description="Weaknesses of competitors.")
    opportunities: List[str] = Field(description="Market opportunities identified.")
    threats: List[str] = Field(description="Potential market threats.")
    confidence_score: float = Field(description="Confidence score.")

class MarketingStrategyResult(BaseModel):
    admission_strategy: str = Field(description="Overall admission strategy.")
    marketing_channels: List[str] = Field(description="Recommended marketing channels.")
    campaign_ideas: List[str] = Field(description="Ideas for online and offline campaigns.")
    budget_recommendations: str = Field(description="Recommendations for budget allocation.")
    roadmap_90_days: str = Field(description="A 90-day action plan.")
    kpis: List[str] = Field(description="Key Performance Indicators to track.")
    confidence_score: float = Field(description="Confidence score.")

class SEOResult(BaseModel):
    keyword_recommendations: List[str] = Field(description="Recommended SEO keywords.")
    landing_page_ideas: List[str] = Field(description="Ideas for targeted landing pages.")
    blog_strategy: str = Field(description="Strategy for blog content.")
    local_seo_improvements: List[str] = Field(description="Suggestions for local SEO.")
    schema_recommendations: List[str] = Field(description="Recommended schema markups.")
    confidence_score: float = Field(description="Confidence score.")

class ReportResult(BaseModel):
    executive_summary: str = Field(description="High-level executive summary of all analyses.")
    sections: Dict[str, Any] = Field(description="Merged sections from various agent reports.")
    quick_wins: List[str] = Field(description="List of immediate actions to take.")
    long_term_recommendations: List[str] = Field(description="List of long-term strategic recommendations.")
    confidence_score: float = Field(description="Confidence score.")

class QAResult(BaseModel):
    is_consistent: bool = Field(description="Whether the output is consistent and accurate.")
    missing_information: List[str] = Field(description="Information missing from the report.")
    conflicting_recommendations: List[str] = Field(description="Any conflicting advice detected.")
    business_feasibility: str = Field(description="Assessment of how feasible the recommendations are.")
    confidence_score: float = Field(description="Confidence score of the QA evaluation.")
    needs_revision: bool = Field(description="True if the output needs revision from the agents.")
    feedback: str = Field(description="Constructive feedback for revisions.")
