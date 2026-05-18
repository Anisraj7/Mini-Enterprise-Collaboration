export function getPageItems(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.data)) return payload.data;
  return [];
}

export function getPageCount(payload) {
  return payload?.pages || payload?.total_pages || 1;
}
