const SEARCH_HISTORY_KEY = 'search_history'
const MAX_HISTORY = 5

export function getSearchHistory(): string[] {
  try {
    return JSON.parse(localStorage.getItem(SEARCH_HISTORY_KEY) || '[]')
  } catch {
    return []
  }
}

export function addSearchHistory(keyword: string) {
  const history = getSearchHistory().filter((h) => h !== keyword)
  history.unshift(keyword)
  if (history.length > MAX_HISTORY) history.length = MAX_HISTORY
  localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history))
}

export function clearSearchHistory() {
  localStorage.removeItem(SEARCH_HISTORY_KEY)
}
