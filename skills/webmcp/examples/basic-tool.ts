/**
 * Basic WebMCP Tool Registration with Dynamic Lifecycle & AbortSignal.
 *
 * Requirements:
 * - Chrome 149+ with Origin Trial or about:flags#enable-webmcp-testing
 * - Or npm package: webmcp-types
 */

/// <reference types="webmcp-types" />

export interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
}

const activeTodos: TodoItem[] = [];

/**
 * Registers an in-browser WebMCP tool to allow agents to add items to a todo list.
 * Returns an unregister function using AbortController.
 */
export async function registerTodoTool(): Promise<() => void> {
  if (!("modelContext" in document)) {
    console.warn("WebMCP (document.modelContext) is not supported in this browser context.");
    return () => {};
  }

  const controller = new AbortController();

  await document.modelContext.registerTool({
    name: "add_todo_item",
    title: "Add To-Do Item",
    description: "Adds a new task to the user's active in-page to-do list.",
    inputSchema: {
      type: "object",
      properties: {
        taskText: {
          type: "string",
          description: "Description of the task to add (e.g. 'Review pull request')"
        }
      },
      required: ["taskText"]
    },
    annotations: {
      readOnlyHint: false,
      consequentialHint: false,
      untrustedContentHint: false
    },
    async execute({ taskText }: { taskText: string }, { signal }) {
      if (signal.aborted) {
        throw new DOMException("Tool execution aborted by caller", "AbortError");
      }

      // Input sanitation and validation
      const sanitized = taskText?.trim();
      if (!sanitized) {
        return {
          success: false,
          error: "taskText cannot be empty."
        };
      }

      // Perform local state mutation
      const newItem: TodoItem = {
        id: crypto.randomUUID(),
        text: sanitized,
        completed: false
      };
      activeTodos.push(newItem);

      // Synchronize DOM UI
      renderTodoList(activeTodos);

      return {
        success: true,
        createdId: newItem.id,
        totalItems: activeTodos.length,
        message: `Successfully added '${newItem.text}' to active list.`
      };
    }
  }, {
    signal: controller.signal
  });

  console.log("WebMCP tool 'add_todo_item' registered successfully.");

  // Return teardown callback
  return () => {
    controller.abort();
    console.log("WebMCP tool 'add_todo_item' unregistered.");
  };
}

function renderTodoList(items: TodoItem[]) {
  const container = document.getElementById("todo-container");
  if (!container) return;

  container.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item.text;
    li.dataset.id = item.id;
    container.appendChild(li);
  }
}
