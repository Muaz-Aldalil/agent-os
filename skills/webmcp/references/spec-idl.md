# WebMCP Web IDL Specification Reference

Extracted and verified against the authoritative **W3C Web Machine Learning Community Group** Bikeshed specification (`index.bs`).

## 1. Document Partial Interface

```webidl
partial interface Document {
  [SecureContext, SameObject] readonly attribute ModelContext modelContext;
};
```

- **`[SecureContext]`**: Only exposed in cryptographic contexts (HTTPS or localhost).
- **`[SameObject]`**: Subsequent reads of `document.modelContext` return the identical object reference.

---

## 2. ModelContext Interface

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

### Methods
- **`registerTool(tool, options)`**:
  - Registers an in-page tool callable by agents.
  - Rejects if tool name is empty, description is empty, a tool with the same name is already registered, or `inputSchema` is malformed.
- **`getTools(options)`**:
  - Returns an array of `RegisteredTool` objects.
  - Defaults to same-origin tools in the frame tree.
- **`executeTool(tool, inputObject, options)`**:
  - Securely dispatches execution to the document owning the tool.
  - Returns a Promise resolving to a **JSON-serialized DOMString**.

### Events
- **`toolchange`**: Dispatched on `document.modelContext` when tools are registered, unregistered, or updated.
- **`toolactivated`**: Dispatched (`ToolActivatedEvent`) when a declarative tool begins processing.
- **`toolcancel`**: Dispatched (`ToolCancelEvent`) when an in-flight tool invocation is cancelled.

---

## 3. Dictionaries & Types

### 3.1 `ModelContextTool`
```webidl
dictionary ModelContextTool {
  required DOMString name;
  USVString title;
  required DOMString description;
  object inputSchema;
  required ToolExecuteCallback execute;
  ToolAnnotations annotations;
};
```

### 3.2 `ToolAnnotations`
```webidl
dictionary ToolAnnotations {
  boolean readOnlyHint = false;
  boolean untrustedContentHint = false;
  boolean consequentialHint = false;
  boolean debugging = false;
};
```

### 3.3 `ToolExecuteCallback`
```webidl
dictionary ToolExecuteCallbackOptions {
  required AbortSignal signal;
};

callback ToolExecuteCallback = Promise<any> (object inputObject, ToolExecuteCallbackOptions options);
```

### 3.4 Registration & Retrieval Options
```webidl
dictionary ModelContextRegisterToolOptions {
  sequence<USVString> exposedTo;
  AbortSignal signal;
};

dictionary ModelContextGetToolOptions {
  sequence<USVString> fromOrigins;
};

dictionary ModelContextExecuteToolOptions {
  AbortSignal signal;
};

dictionary RegisteredTool {
  required DOMString name;
  DOMString title;
  required DOMString description;
  object inputSchema;
  required Window window;
  required USVString origin;
  ToolAnnotations annotations;
};
```

---

## 4. Lifecycle Events

```webidl
[Exposed=Window, SecureContext]
interface ToolActivatedEvent : Event {
  constructor(DOMString type, optional ToolActivatedEventInit eventInitDict = {});
  readonly attribute DOMString toolName;
};

dictionary ToolActivatedEventInit : EventInit {
  DOMString toolName = "";
};

[Exposed=Window, SecureContext]
interface ToolCancelEvent : Event {
  constructor(DOMString type, optional ToolCancelEventInit eventInitDict = {});
  readonly attribute DOMString toolName;
};

dictionary ToolCancelEventInit : EventInit {
  DOMString toolName = "";
};
```
