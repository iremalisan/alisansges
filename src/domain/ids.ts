/** Deterministic entity IDs for multi-entry collections. */

let sequence = 0;

export function resetIdSequence(next = 0): void {
  sequence = next;
}

export function createEntityId(prefix: string): string {
  sequence += 1;
  return `${prefix}-${sequence}`;
}

export function createFixedId(prefix: string, slug: string): string {
  return `${prefix}-${slug}`;
}
