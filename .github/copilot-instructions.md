# Purpose:
This document defines the structured, tool-integrated AI project workflow within VSCode for maximizing automation, reliability, and traceability across conversations and executions. It is optimized for environments using MCP and supporting plugins like Sequential Thinking, REPL, Fetch, Puppeteer, GitHub, and others.

## Automatic Activation
- All instructions and tool integrations listed here are automatically active in all conversations for this project.
- Tools should be utilized proactively and contextually without needing explicit user prompts.

## Default Auto-Active Tools:
- kite, github, context7, playwright, excel, git, memory, sequential-thinking, puppeteer, filesystem, fetch, desktop-commander, zoom, notion, tavily, duckduckgo, everything-search.

## Default Conversation Workflow
- Retrieve and review the last 10 minutes of conversation history, if available, to establish context.
- Start with Sequential Thinking – Automatically trigger it to break down the user's request.
- Terminal Monitoring – Read and interpret command output for successful execution before proceeding.
- Use PowerShell – Prefer PowerShell over Command Prompt for scripting and system tasks.

## Mandatory Tool Usage
- The following tools must be used based on the specific requirements of each task.
- Additionally, verify which tools are available for a particular MCP to ensure efficient and appropriate usage:
- Ensure that the required MCP is in a running state before use. If it is currently stopped, start the MCP before proceeding with any tool operations.

- Sequential Thinking: Core for breaking down multi-step problems
- Kite: Trading and stock market data
- Git / GitHub: Version control, repository integration
- Context7: Enhanced contextual reasoning and memory management
- Fetch: HTTP content and API access
- Excel: Spreadsheet data handling and formula computation
- Memory: Persistent storage of conversations
- Playwright / Puppeteer: Web scraping, browser testing, automation
- Filesystem: Local file and directory operations
- Desktop Commander: Advanced desktop/system file interactions
- Artifacts: For code, visualizations, or documents requiring export
- Zoom: Meeting scheduling and interaction
- DuckDuckgo: Privacy-focused web search engine for general web information retrieval
- Notion: Document management and collaboration platform integration
- Tavily: AI-powered search engine for comprehensive web information retrieval
- Everything-search: Fast local file search tool

## Source Documentation Standards
- All retrieved or referenced external content must be fully traceable:
- Full URL, title, and timestamp for web search results and screenshots
- Cite access dates for all external data or references
- Maintain links in knowledge graphs and summaries
- Use Fetch or DuckDuckgo to retain metadata
- External quotes must include direct source links

## Core Workflow Phases
### 1. Initial Analysis – Sequential Thinking
- Deconstruct the problem into core components
- Identify concepts, relationships, and dependencies
- Select tools accordingly
- Plan for parallelization where applicable

### 2. Search Phase – Fetch / DuckDuckgo
- Begin with broad semantic or contextual queries
- Narrow down using refined filters and offsets
- Include query logs and metadata in output
- Document exact search string, result count, and time of access

### 3. Deep Verification – Puppeteer or Playwright
-Visit top-ranked sites from search
- Take annotated screenshots
- Log all navigation actions
- Fill forms and extract structured data as needed
- Validate output before continuing (e.g., verify expected content appears)

### 4. Data Processing – REPL / Excel / Scripts
- Handle structured data like CSV/JSON
- Perform computations and generate insights
- Create tables, charts, or analysis reports
- Optionally link to memory or knowledge graph

### 5. Synthesis & Output – Artifacts / Markdown / Presentation
- Combine data, insights, code, and visuals into a cohesive output
- Create well-documented artifacts (.md, .ipynb, .py, .csv, etc.)
- Highlight the final insights, traceability, and decision logic

###6. Memory: Check if new entities are required for persistent memory storage to maintain context across conversations.

## Tool-Specific Best Practices
### Tavily
- Use for comprehensive web information retrieval

### Fetch / DuckDuckgo
- Use count, offset, and query scoping
- Document each query string and output summary
- Include metadata: title, URL, snippet, accessed date/time

### Puppeteer / Playwright
- Always verify navigation success
- Extract data using precise selectors
- Document screenshot evidence and URL history
- Gracefully handle page errors and retries

### Sequential Thinking
- Explicitly document step-by-step logic
- Branch alternatives when ambiguous
- Allow for mid-task reevaluation

### REPL / Analysis Tools
- Prefer scripting logic for repeatable computations
- Show all formulas or code used for transparency
- Annotate results for easy review

### Artifacts
- Use when output exceeds reasonable message length or includes files
- Annotate content purpose and structure
- Link back to original conversation or dataset if applicable

## Implementation & Execution Notes
- Proactive Use: Tools should activate based on task type, not just by prompt.
- Parallel Execution: Multiple tools can run simultaneously for efficiency.
- Documentation-First: Each major step should be logged or cited.
- Knowledge Retention: Long-term insights stored via memory/knowledge graph.
- Workflow Triggering: Multi-step prompts should auto-trigger full pipeline.