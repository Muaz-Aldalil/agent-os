/**
 * Multi-Tool E-Commerce Product Filtering and Cart WebMCP Integration.
 * Demonstrates:
 * - Query tool (`search_catalog`) with readOnlyHint: true
 * - Action tool (`update_cart`) with consequentialHint: true and integer cents
 * - DOM synchronization and bidirectional state updates
 */

export interface Product {
  id: string;
  title: string;
  category: "electronics" | "books" | "apparel";
  priceCents: number;
  inStock: boolean;
}

const CATALOG: Product[] = [
  { id: "prod_1", title: "Wireless Noise-Canceling Headphones", category: "electronics", priceCents: 19900, inStock: true },
  { id: "prod_2", title: "Mechanical Keyboard (Cherry MX)", category: "electronics", priceCents: 12900, inStock: true },
  { id: "prod_3", title: "Organic Cotton Hoodie", category: "apparel", priceCents: 6500, inStock: false },
  { id: "prod_4", title: "Designing Data-Intensive Applications", category: "books", priceCents: 4500, inStock: true }
];

interface CartItem {
  productId: string;
  quantity: number;
}

let cart: CartItem[] = [];

export async function setupStoreWebMCPTools(abortSignal: AbortSignal): Promise<void> {
  if (!("modelContext" in document)) {
    return;
  }

  // Tool 1: Catalog Search (Read-only)
  await document.modelContext.registerTool({
    name: "search_catalog",
    title: "Search Catalog",
    description: "Searches available store inventory by keyword, category, and budget limits.",
    inputSchema: {
      type: "object",
      properties: {
        keyword: { type: "string", description: "Optional search text matching product title." },
        category: { type: "string", enum: ["electronics", "books", "apparel"], description: "Category filter." },
        maxPriceCents: { type: "integer", description: "Budget ceiling in integer cents (e.g. 15000 for $150.00)." },
        inStockOnly: { type: "boolean", default: true, description: "Whether to exclude out of stock items." }
      }
    },
    annotations: {
      readOnlyHint: true,
      consequentialHint: false
    },
    async execute(params: any) {
      let filtered = CATALOG;

      if (params.category) {
        filtered = filtered.filter(p => p.category === params.category);
      }
      if (params.maxPriceCents != null) {
        filtered = filtered.filter(p => p.priceCents <= params.maxPriceCents);
      }
      if (params.inStockOnly !== false) {
        filtered = filtered.filter(p => p.inStock);
      }
      if (params.keyword) {
        const kw = params.keyword.toLowerCase();
        filtered = filtered.filter(p => p.title.toLowerCase().includes(kw));
      }

      // Update visible grid in document
      renderProductGrid(filtered);

      return {
        matchedCount: filtered.length,
        products: filtered.map(p => ({
          id: p.id,
          title: p.title,
          priceFormatted: `$${(p.priceCents / 100).toFixed(2)}`,
          inStock: p.inStock
        }))
      };
    }
  }, { signal: abortSignal });

  // Tool 2: Add/Remove from Cart (Consequential action)
  await document.modelContext.registerTool({
    name: "update_cart",
    title: "Update Cart Quantity",
    description: "Adds, updates, or removes an item in the active shopping cart.",
    inputSchema: {
      type: "object",
      properties: {
        productId: { type: "string", description: "The product identifier." },
        quantity: { type: "integer", minimum: 0, maximum: 99, description: "Desired item quantity. 0 removes the item." }
      },
      required: ["productId", "quantity"]
    },
    annotations: {
      readOnlyHint: false,
      consequentialHint: true // Financial / ordering implication
    },
    async execute({ productId, quantity }: { productId: string; quantity: number }, { signal }) {
      if (signal.aborted) {
        throw new DOMException("Cart update cancelled", "AbortError");
      }

      const product = CATALOG.find(p => p.id === productId);
      if (!product) {
        return { success: false, error: `Product '${productId}' not found in catalog.` };
      }
      if (!product.inStock && quantity > 0) {
        return { success: false, error: `Product '${product.title}' is currently out of stock.` };
      }

      const existingIndex = cart.findIndex(c => c.productId === productId);
      if (quantity === 0) {
        if (existingIndex >= 0) cart.splice(existingIndex, 1);
      } else {
        if (existingIndex >= 0) {
          cart[existingIndex].quantity = quantity;
        } else {
          cart.push({ productId, quantity });
        }
      }

      // Re-calculate totals
      const totalCents = cart.reduce((acc, item) => {
        const p = CATALOG.find(prod => prod.id === item.productId);
        return acc + (p ? p.priceCents * item.quantity : 0);
      }, 0);

      renderCartUI(cart, totalCents);

      return {
        success: true,
        cartItemCount: cart.reduce((sum, i) => sum + i.quantity, 0),
        cartTotalFormatted: `$${(totalCents / 100).toFixed(2)}`,
        message: `Cart updated: ${quantity}x '${product.title}'`
      };
    }
  }, { signal: abortSignal });
}

function renderProductGrid(products: Product[]) {
  const el = document.getElementById("catalog-grid");
  if (el) {
    el.innerHTML = products.map(p => `
      <div class="product-card" data-id="${p.id}">
        <h4>${p.title}</h4>
        <p>$${(p.priceCents / 100).toFixed(2)}</p>
      </div>
    `).join("");
  }
}

function renderCartUI(items: CartItem[], totalCents: number) {
  const el = document.getElementById("cart-summary");
  if (el) {
    el.textContent = `Cart: ${items.length} items | Total: $${(totalCents / 100).toFixed(2)}`;
  }
}
