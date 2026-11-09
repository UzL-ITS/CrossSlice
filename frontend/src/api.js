async function request(url, options) {
  const res = await fetch(url, options)
  let data
  try {
    data = await res.json()
  } catch {
    throw new Error(`${res.status} ${res.statusText}`)
  }
  if (!res.ok || (data && data.error)) {
    throw new Error(data?.error || `${res.status} ${res.statusText}`)
  }
  return data
}

export const api = {
  state: () => request('/api/state'),
  // body: { id } (an existing node) | { name } | { name, file, line, kind } (a specific definition)
  expand: (body) =>
    request('/api/expand', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),
  search: (q) => request(`/api/search?q=${encodeURIComponent(q)}`),
  node: ({ id, name }) =>
    request(id != null ? `/api/node?id=${id}` : `/api/node?name=${encodeURIComponent(name)}`),
  update: () => request('/api/update', { method: 'POST' }),
  commits: (limit = 30) => request(`/api/commits?limit=${limit}`),
  commit: (rev) => request(`/api/commit?rev=${encodeURIComponent(rev || 'HEAD')}`),
}
