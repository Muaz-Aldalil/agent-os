# WebMCP Security & Boundary Architecture

WebMCP introduces programmatic agent access to web applications, crossing traditional trust boundaries. This document outlines the mandatory security posture and threat mitigation strategies defined by the W3C WebMCP specification.

---

## 1. Permissions Policy (`tools`)

Access to `document.modelContext` is controlled by the Permissions Policy feature `"tools"`.

```
Feature Name:     tools
Default Allowlist: 'self'
```

### Delegation Rules
1. **Top-Level Documents**: Granted by default under HTTPS.
2. **Same-Origin Iframes**: Inherit access from parent by default.
3. **Cross-Origin Iframes**: Blocked by default. Must be explicitly delegated:
   ```html
   <iframe src="https://partner-agent.com" allow="tools"></iframe>
   ```
4. **Disabling Feature**: To completely disallow WebMCP across an entire origin or document tree:
   ```http
   Permissions-Policy: tools=()
   ```

---

## 2. Origin Isolation & Cross-Frame Access

### `exposedTo` vs `fromOrigins`
Tools registered by a document are not visible to third-party frames unless explicitly shared:

```javascript
// Registering frame: Expose specifically to trusted partner
await document.modelContext.registerTool({
  name: "share_document",
  description: "Exports current document summary",
  execute() { return { id: 123, status: "draft" }; }
}, {
  exposedTo: ["https://trusted-partner.example.com"]
});
```

```javascript
// Consuming frame: Request tools from specific secure origins
const tools = await document.modelContext.getTools({
  fromOrigins: ["https://trusted-partner.example.com"]
});
```

The browser enforces mutual consent: if `exposedTo` does not include the caller's origin, `executeTool` will reject.

---

## 3. Threat Matrix & Defense-in-Depth

| Threat Vector | Description | Mandatory Defense |
|---|---|---|
| **Prompt Injection / Malicious Input** | An external agent supplies malicious payloads (`<script>`, SQL fragments, shell metacharacters). | Treat all `inputObject` properties as untrusted. Validate via Zod/Valibot schemas before DOM insertion or API forwarding. |
| **Confused Deputy Attack** | Agent is tricked into calling a destructive tool with the user's logged-in session cookies. | Mark high-impact tools with `consequentialHint: true`. For state-mutating actions (checkout, deletion), require human confirmation. |
| **Data Exfiltration** | A compromised third-party script registers tools to read sensitive form fields. | Restrict Permissions Policy; inspect tool registry (`getTools()`) in audits; use Content Security Policy (CSP). |
| **Denial of Service / Loop Lockup** | Agent invokes heavy synchronous computation repeatedly. | Check `signal.aborted` frequently inside async loops. Enforce timeout budgets. |

---

## 4. Architectural Rules for High-Stakes Domains

1. **Financial Operations**:
   - Zero floating-point arithmetic. Represent money strictly as integer subunits (e.g., cents).
   - Require idempotency keys on checkout or charge tool callbacks.
2. **Authentication & Identity**:
   - Derive the active user ID from the authenticated session cookies or JWT—never accept a `userId` parameter blindly from the agent.
3. **Visual Feedback Synchronization**:
   - Whenever a tool mutates data, ensure the visible DOM is synchronously updated so the human user retains full transparency.
