---
inclusion: manual
---

# vja MCP server

The guidance for the `vja` MCP server (install, registration, available tools,
and practical notes on date filtering and large tool output) is maintained in a
vendor-neutral file at the repository root:

#[[file:AGENTS.md]]

This steering file exists so the content can be pulled into a Kiro session with
`#vja-mcp`. Kiro's own MCP server config lives in `.kiro/settings/mcp.json`
(it supports the client-specific `disabled` and `autoApprove` keys); the
portable equivalent is `.mcp.json` in the repository root.
