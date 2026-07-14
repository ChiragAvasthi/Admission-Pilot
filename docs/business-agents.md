# Business Agents Architecture

AdmissionPilot uses a suite of specialized Business Agents that plug into the central `MasterAgent` and LangGraph orchestrator. These agents never communicate directly with the user or with each other. All routing, context sharing, and error handling are managed by the macro-architecture.

## Execution Lifecycle
1. **Delegation**: The `ExecutionManager` identifies a pending task and fetches the corresponding Agent from the `AgentRegistry` based on required `Capabilities`.
2. **Context Injection**: The `ContextBuilder` provides the agent with active goal context, conversation history, and RAG knowledge.
3. **Execution**: The agent retrieves its specific markdown prompt from the `PromptManager` and queries the `LocalLLM`.
4. **Validation**: The output is strongly typed via Pydantic (`DocumentAnalysisResult`, `SEOResult`, etc.).
5. **Quality Assurance**: The `QA Agent` reviews generated blocks. If confidence is `< 0.8`, it triggers a revision loop through the `TaskManager`.

## The Agents

### 1. Document Intelligence Agent
- **Capability**: `DOCUMENT_ANALYSIS`
- **Responsibility**: Ingests unstructured files/HTML, extracts structured college profiles, and stores them in the ChromaDB knowledge base.
- **Output**: `DocumentAnalysisResult`

### 2. Website Analysis Agent
- **Capability**: `WEBSITE_ANALYSIS`
- **Responsibility**: Audits target URLs for strengths, weaknesses, and UX/UI metrics.
- **Output**: `WebsiteAuditResult`

### 3. Competitor Intelligence Agent
- **Capability**: `COMPETITOR_INTELLIGENCE`
- **Responsibility**: Runs searches, evaluates local competitors, and generates SWOT matrices.
- **Output**: `CompetitorAnalysisResult`

### 4. Marketing Strategy Agent
- **Capability**: `MARKETING_STRATEGY`
- **Responsibility**: Synthesizes past campaigns and competitor data into a 90-day execution roadmap and budget plan.
- **Output**: `MarketingStrategyResult`

### 5. SEO & Content Strategy Agent
- **Capability**: `SEO_STRATEGY`
- **Responsibility**: Analyzes metadata and structures to recommend keywords, landing pages, and Local SEO improvements.
- **Output**: `SEOResult`

### 6. Report Generation Agent
- **Capability**: `REPORT_GENERATION`
- **Responsibility**: Merges all findings into a comprehensive, cohesive final Markdown/PDF report.
- **Output**: `ReportResult`

### 7. Quality Assurance Agent
- **Capability**: `QUALITY_ASSURANCE`
- **Responsibility**: Reviews all outputs for hallucinations, logic gaps, and business feasibility.
- **Output**: `QAResult`
