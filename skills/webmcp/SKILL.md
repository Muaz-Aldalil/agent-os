---
name: webmcp
description: >-
  Standardized protocol and developer guide for WebMCP (Web Model Context Protocol),
  the W3C browser standard exposing in-page JavaScript tools and declarative forms to AI agents via
  document.modelContext. Use when designing, authoring, registering, testing, or debugging
  in-browser WebMCP tools (document.modelContext.registerTool, getTools, executeTool),
  managing permissions policy ("tools"), securing cross-origin iframe exposures (exposedTo/fromOrigins),
  or enabling agentic web application actuation.
compatibility: W3C Web Machine Learning Community Group Specification Draft. Chrome 149+ (Origin Trial / about:flags#enable-webmcp-testing), Edge 150+, npm package webmcp-types.
---

# WebMCP: In-Browser Model Context Protocol (SKILL.md)

## 1. Overview & Purpose

**WebMCP (Web Model Context Protocol)** is an emerging W3C web standard incubated by the **W3C Web Machine Learning Community Group** (`webmachinelearning/webmcp`). It allows web applications to expose client-side JavaScript functions and semantic HTML forms directly to AI agents as structured, callable tools under `document.modelContext`.

### Why WebMCP Over Traditional Web Actuation?
- **Traditional Actuation (Brittle)**: Relies on DOM scraping, screen readers, OCR screenshots, synthetic clicks, and CSS selector guessing. Fragile, slow, and prone to breaking on minor UI adjustments.
- **Backend MCP / Remote API (UI Disintermediation)**: Bypasses the active browser session, losing user session cookies, client-side state, form validation, and reactive UI feedback.
- **WebMCP (Client-Native & Synchronized)**: Web applications register tools directly in the browser document execution context. AI agents call structured tools via JSON schemas, and web application code updates the DOM and reactive state in real time for both the user and the agent.

---

## 2. Core Architecture & Interfaces

WebMCP extends the browser's `Document` interface with the `modelContext` property in secure contexts (`https://`):

```webidl
partial interface Document {
  [SecureContext, SameObject] readonly attribute ModelContext modelContext;
};
```

### The `ModelContext` Interface
```webidl
[Exposed=Window, SecureContext]
interface ModelContext : EventTarget {
  Promise<undefined> registerTool(ModelContextTool tool, optional ModelContextRegisterToolOptions options = {});
  Promise<sequence<RegisteredTool>> getTools(optional ModelContextGetToolOptions options = {});
  Promise<DOMString> executeTool(RegisteredTool tool, optional object inputObject, optional ModelContextExecuteToolOptions options = {});

  attribute EventHandler ontoolchange;
  attribute EventHandler ontoolactivated;
  attribute EventHandler ontoolcancel;
};
```

---

## 3. Imperative Tool Authoring & Lifecycle

### 3.1 Registering a Tool (`registerTool`)

Web developers register tools by invoking `document.modelContext.registerTool(tool, options)`.

```typescript
// Import official TypeScript definitions if using npm
// npm install --save-dev webmcp-types

const controller = new AbortController();

await document.modelContext.registerTool({
  name: "filter_products",
  title: "Filter Store Products",
  description: "Filters visible catalog items by category, maximum price, and in-stock status.",
  inputSchema: {
    type: "object",
    properties: {
      category: {
        type: "string",
        enum: ["electronics", "apparel", "home", "books"],
        description: "The product category to display."
      },
      maxPrice: {
        type: "number",
        description: "Maximum budget filter in integer cents (e.g. 5000 for $50.00)."
      },
      inStockOnly: {
        type: "boolean",
        description: "Whether to hide out-of-stock items."
      }
    },
    required: ["category"]
  },
  annotations: {
    readOnlyHint: true,           // Indicates tool does not mutate server/session state
    untrustedContentHint: false,  // Return value does not contain raw untrusted user input
    consequentialHint: false      // No financial, destructive, or permanent side-effect
  },
  async execute(input, { signal }) {
    // 1. Check for cancellation
    if (signal.aborted) {
      throw new DOMException("Tool execution aborted", "AbortError");
    }

    // 2. Perform client-side filtering and update visual UI
    const matchingCount = await applyCatalogFilters(input, signal);

    // 3. Return JSON-serializable structured result
    return {
      success: true,
      category: input.category,
      matchedCount: matchingCount,
      message: `Updated catalog view: ${matchingCount} items matching criteria displayed.`
    };
  }
}, {
  signal: controller.signal // Unregister tool by calling controller.abort()
});
```

### 3.2 Dynamic Tool Lifecycle & Token Budget Management
- **Context Window Conservation**: AI agents have finite prompt budgets. Do NOT statically register dozens of dormant tools on initial page load.
- **State-Dependent Registration**: Dynamically register tools relevant to the active user workflow (e.g., checkout tools only during checkout).
- **Graceful Teardown**: Pass an `AbortSignal` in `ModelContextRegisterToolOptions.signal`. When the user navigates away or closes a modal, call `controller.abort()` to unregister the tool cleanly and trigger `toolchange`.

### 3.3 Discovering & Executing Tools (`getTools` & `executeTool`)
Author-provided agents or browser extensions discover and invoke registered tools safely:

```typescript
// 1. Discover registered tools in same-origin frames
const tools = await document.modelContext.getTools();
const filterTool = tools.find(t => t.name === "filter_products");

if (filterTool) {
  const abortCtrl = new AbortController();
  
  // 2. Execute the tool with structured arguments
  const rawResult = await document.modelContext.executeTool(
    filterTool,
    { category: "electronics", maxPrice: 10000, inStockOnly: true },
    { signal: abortCtrl.signal }
  );

  // Result is returned as a JSON-serialized string
  const parsed = JSON.parse(rawResult);
  console.log("Agent received result:", parsed);
}
```

---

## 4. Declarative Form Tools (HTML Synthesis)

WebMCP supports exposing semantic HTML `<form>` elements as tools without custom JavaScript boilerplate:

```html
<form
  action="/search"
  method="GET"
  toolname="search_flight"
  tooldescription="Search available flights by departure, destination, and departure date."
  toolautosubmit>

  <label for="from">From:</label>
  <input
    type="text"
    id="from"
    name="origin"
    toolparamdescription="3-letter IATA airport code for departure (e.g. JFK, LHR, DXB)"
    required>

  <label for="to">To:</label>
  <input
    type="text"
    id="to"
    name="destination"
    toolparamdescription="3-letter IATA airport code for arrival (e.g. SFO, CDG, HND)"
    required>

  <label for="date">Date:</label>
  <input
    type="date"
    id="date"
    name="departureDate"
    toolparamdescription="Departure date in YYYY-MM-DD format"
    required>

  <button type="submit">Search Flights</button>
</form>
```

### Declarative Directives & State
- `toolname`: Unique tool identifier.
- `tooldescription`: Purpose and intent for the LLM.
- `toolparamdescription`: Parameter-level schema description applied to form fields.
- `toolautosubmit`: When present, allows the browser/agent to submit the form autonomously. When omitted, the browser focuses the submit button and prompts the human user for confirmation.
- **CSS Pseudo-Classes**:
  - `:tool-form-active`: Matches form while tool execution is in progress.
  - `:tool-submit-active`: Matches the submit button when active.
- **`SubmitEvent` Extensions**:
  - `event.agentInvoked`: Boolean indicating if form was triggered by an agent.
  - `event.respondWith(Promise<any>)`: Overrides default navigation, sending structured JSON back to the agent without reloading the page.

---

## 5. Security, Permissions Policy & Origin Boundaries

### 5.1 The `tools` Permissions Policy
Access to `document.modelContext` is gated by the Permissions Policy feature `"tools"`.
- Default Allowlist: `'self'`.
- Top-level documents and same-origin iframes have access by default.
- Cross-origin iframes MUST be granted explicit permission:
  ```html
  <iframe src="https://agent-widget.example.com" allow="tools"></iframe>
  ```
- To disable WebMCP globally across a document:
  ```http
  Permissions-Policy: tools=()
  ```

### 5.2 Cross-Origin Isolation (`exposedTo` & `fromOrigins`)
By default, registered tools are isolated to the registering document and same-origin frames:
- **Sharing with specific origins**:
  ```javascript
  await document.modelContext.registerTool(tool, {
    exposedTo: ["https://trusted-partner.example.com"]
  });
  ```
- **Querying cross-origin tools**:
  ```javascript
  const partnerTools = await document.modelContext.getTools({
    fromOrigins: ["https://trusted-partner.example.com"]
  });
  ```

### 5.3 High-Stakes Invariants (Danger Zones)
1. **Never Trust Tool Arguments Blindly**: Always validate inputs against domain schemas (Zod/Valibot) inside `execute()` even if declared in `inputSchema`.
2. **Anti-CSRF / Anti-IDOR Enforcement**: Tool execution executes with the active document's credentials. Verify session state, tenant boundaries, and CSRF tokens for mutating actions.
3. **Financial / Payment Boundaries**: Enforce integer subunits (cents/micros), idempotency keys, and explicit user confirmation dialogs before invoking irreversible actions.
4. **Tool Annotations Honesty**: Mark `consequentialHint: true` for state-mutating actions (purchases, deletions) so agent frameworks enforce human-in-the-loop confirmation.

---

## 6. Testing, Polyfills & Browser Environment

### 6.1 Chromium Flags & Origin Trial
- **Chrome 149+**: Origin Trial available.
- **Local Dev Flag**: Launch Chrome or Edge with:
  `chrome://flags/#enable-webmcp-testing` (Enabled)
  or command line flag:
  `--enable-blink-features=WebMCP`

### 6.2 Unit Testing Mock / Test Harness
When running in Node.js or Vitest/Jest where `document.modelContext` is not native, use the canonical mock pattern:

```typescript
export class MockModelContext extends EventTarget {
  private tools = new Map<string, any>();

  async registerTool(tool: any, options: { signal?: AbortSignal } = {}) {
    if (!tool.name || !tool.description) {
      throw new DOMException("Invalid tool definition", "SyntaxError");
    }
    if (this.tools.has(tool.name)) {
      throw new DOMException(`Tool ${tool.name} already registered`, "InvalidStateError");
    }

    this.tools.set(tool.name, tool);
    if (options.signal) {
      options.signal.addEventListener("abort", () => {
        this.tools.delete(tool.name);
        this.dispatchEvent(new CustomEvent("toolchange"));
      });
    }
    this.dispatchEvent(new CustomEvent("toolchange"));
  }

  async getTools() {
    return Array.from(this.tools.values()).map(t => ({
      name: t.name,
      title: t.title,
      description: t.description,
      inputSchema: t.inputSchema,
      annotations: t.annotations,
      origin: window.location.origin,
      window: window
    }));
  }

  async executeTool(tool: any, input: any = {}, options: { signal?: AbortSignal } = {}) {
    const registered = this.tools.get(tool.name);
    if (!registered) throw new DOMException("Tool not found", "NotFoundError");
    const result = await registered.execute(input, { signal: options.signal || new AbortController().signal });
    return JSON.stringify(result);
  }
}
```

---

## 7. Guard Skill Orchestration & Verification

When authoring or updating WebMCP tools in production web applications:
- **`clean-code-guard`**: Verify single-responsibility tool design, schema clarity, and clean parameter naming.
- **`rtl-logical-guard`**: If WebMCP tool updates visible UI elements, ensure layout changes use CSS logical properties (`start`/`end`).
- **`test-guard`**: Ensure characterization unit tests exist for all `execute()` handlers with happy-path, boundary, and aborted signal scenarios.
