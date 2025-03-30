/**
 * MovieSeek Frontend Utilities
 */

/**
 * Constructs a TMDb image URL from a path
 * @param {string} path - The image path from TMDb API
 * @param {string} size - The size of the image (w500, original, etc)
 * @returns {string|null} - The complete image URL or null if path is invalid
 */
export const getTMDbImageUrl = (path, size = 'w500') => {
  if (!path) return null
  return `https://image.tmdb.org/t/p/${size}${path}`
}

/**
 * Format a large number with commas
 * @param {number} num - The number to format
 * @returns {string} - The formatted number
 */
export const formatNumber = (num) => {
  if (!num) return '0'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
} 