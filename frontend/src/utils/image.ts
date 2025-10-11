/**
 * Get the full image URL from a relative or absolute path
 * @param imagePath - The image path from the API
 * @returns Full image URL or placeholder
 */
export function getImageUrl(imagePath: string | null | undefined): string {
  const placeholder = 'https://placehold.co/600x400?text=No+Image'
  
  if (!imagePath) {
    return placeholder
  }
  
  // If it's already a full URL, return as is
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath
  }
  
  // Since nginx proxies /media/ to backend, use relative path
  // This works because nginx.conf has location /media/ proxy to backend
  const path = imagePath.startsWith('/') ? imagePath : `/${imagePath}`
  
  return path
}

/**
 * Get product image URL with fallback logic
 * @param product - Product object
 * @returns Full image URL
 */
export function getProductImageUrl(product: any): string {
  const placeholder = 'https://placehold.co/600x400?text=No+Image'
  
  // Check for direct image field
  if (product.image) {
    return getImageUrl(product.image)
  }
  
  // Check for images array
  if (product.images && product.images.length > 0) {
    const firstImage = product.images[0]
    return getImageUrl(firstImage.image_url || firstImage.image)
  }
  
  return placeholder
}

