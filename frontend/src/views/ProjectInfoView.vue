<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12 animate-fade-in-up">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
          Online Shop Project
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          A modern, scalable e-commerce platform built with Django REST Framework, featuring advanced caching strategies, 
          real-time task processing, and robust database transactions.
        </p>
      </div>

      <!-- Technology Stack -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-blue-500 to-purple-600 rounded-full mr-4"></span>
            Technology Stack
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="tech in technologies"
              :key="tech.name"
              class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105"
            >
              <div class="text-4xl mb-3">{{ tech.icon }}</div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ tech.name }}</h3>
              <p class="text-sm text-gray-700 dark:text-gray-300">{{ tech.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Backend Architecture -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-green-500 to-teal-600 rounded-full mr-4"></span>
            Backend Architecture
          </h2>
          
          <div class="space-y-6">
            <div
              v-for="feature in architecture"
              :key="feature.title"
              class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-600"
            >
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">{{ feature.title }}</h3>
              <p class="text-gray-700 dark:text-gray-300 mb-4">{{ feature.description }}</p>
              <ul v-if="feature.details && feature.details.length > 0" class="space-y-2">
                <li v-for="(detail, index) in feature.details" :key="index" class="flex items-start text-sm text-gray-600 dark:text-gray-400">
                  <span class="text-blue-500 mr-2">•</span>
                  <span>{{ detail }}</span>
                </li>
              </ul>
              <pre v-if="feature.code" class="mt-4 bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-xs"><code>{{ feature.code }}</code></pre>
            </div>
          </div>
        </div>
      </section>

      <!-- Caching Strategy -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-red-500 to-orange-600 rounded-full mr-4"></span>
            Advanced Caching Strategy
          </h2>
          
          <div class="space-y-6">
            <div class="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 rounded-xl p-6 border border-red-200 dark:border-red-800">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Cache Stampede Prevention</h3>
              <p class="text-gray-700 dark:text-gray-300 mb-4">
                Our implementation uses multiple strategies to prevent cache stampede (thundering herd problem):
              </p>
              <ul class="space-y-3 text-gray-700 dark:text-gray-300">
                <li class="flex items-start">
                  <span class="text-red-500 mr-2">✓</span>
                  <span><strong>Redis Distributed Locks:</strong> Only one process computes the value when cache expires, others wait for the result</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-500 mr-2">✓</span>
                  <span><strong>Probabilistic Early Expiration:</strong> Randomly expires cache entries slightly before actual expiration to spread regeneration</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-500 mr-2">✓</span>
                  <span><strong>Stale-While-Revalidate:</strong> Optionally serves stale cache while new data is being computed</span>
                </li>
                <li class="flex items-start">
                  <span class="text-red-500 mr-2">✓</span>
                  <span><strong>Cache Warming with Celery Beat:</strong> Proactively refreshes cache before expiration</span>
                </li>
              </ul>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
                <h4 class="font-bold text-lg text-gray-900 dark:text-white mb-3">Cache TTL Configuration</h4>
                <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                  <li>Product List: <strong>10 minutes</strong></li>
                  <li>Product Detail: <strong>15 minutes</strong></li>
                  <li>Category List: <strong>30 minutes</strong></li>
                  <li>Brand List: <strong>30 minutes</strong></li>
                  <li>Top Rated: <strong>15 minutes</strong></li>
                  <li>Discounted Products: <strong>10 minutes</strong></li>
                </ul>
              </div>

              <div class="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-800">
                <h4 class="font-bold text-lg text-gray-900 dark:text-white mb-3">Cache Warming Schedule</h4>
                <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                  <li>All Critical Caches: <strong>Every 5 minutes</strong></li>
                  <li>Product List: <strong>Every 3 minutes</strong></li>
                  <li>Top Products: <strong>Every 5 minutes</strong></li>
                  <li>Categories: <strong>Every 15 minutes</strong></li>
                  <li>Brands: <strong>Every 15 minutes</strong></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Database Transactions -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-yellow-500 to-amber-600 rounded-full mr-4"></span>
            Database Transactions & Concurrency Control
          </h2>
          
          <div class="space-y-6">
            <div class="bg-yellow-50 dark:bg-yellow-900/20 rounded-xl p-6 border border-yellow-200 dark:border-yellow-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Atomic Transactions</h3>
              <p class="text-gray-700 dark:text-gray-300 mb-4">
                We use Django's <code class="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">transaction.atomic()</code> 
                to ensure data consistency in critical operations:
              </p>
              <ul class="space-y-2 text-gray-700 dark:text-gray-300">
                <li class="flex items-start">
                  <span class="text-yellow-600 mr-2">•</span>
                  <span><strong>Cart Operations:</strong> Adding items with stock validation</span>
                </li>
                <li class="flex items-start">
                  <span class="text-yellow-600 mr-2">•</span>
                  <span><strong>Checkout Process:</strong> Order creation with inventory deduction</span>
                </li>
                <li class="flex items-start">
                  <span class="text-yellow-600 mr-2">•</span>
                  <span><strong>Stock Management:</strong> Prevents overselling with row-level locking</span>
                </li>
              </ul>
            </div>

            <div class="bg-green-50 dark:bg-green-900/20 rounded-xl p-6 border border-green-200 dark:border-green-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Row-Level Locking</h3>
              <p class="text-gray-700 dark:text-gray-300 mb-4">
                Using <code class="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">select_for_update()</code> 
                to prevent race conditions:
              </p>
              <pre class="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm"><code># Example: Cart item addition with stock check
with transaction.atomic():
    # Lock the product row for update
    product = Product.objects.select_for_update().get(id=product_id)
    
    # Check stock availability
    if product.quantity < quantity:
        return error_response
    
    # Safe to proceed with cart addition</code></pre>
            </div>
          </div>
        </div>
      </section>

      <!-- Celery & Celery Beat -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-indigo-500 to-blue-600 rounded-full mr-4"></span>
            Celery & Celery Beat
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-xl p-6 border border-indigo-200 dark:border-indigo-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Async Task Processing</h3>
              <ul class="space-y-2 text-gray-700 dark:text-gray-300">
                <li>✓ Email sending (OTP codes)</li>
                <li>✓ Background cache warming</li>
                <li>✓ Long-running operations</li>
                <li>✓ Non-blocking request handling</li>
              </ul>
            </div>

            <div class="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Scheduled Tasks (Celery Beat)</h3>
              <ul class="space-y-2 text-gray-700 dark:text-gray-300">
                <li>✓ Periodic cache warming</li>
                <li>✓ Prevent cache expiration</li>
                <li>✓ Maintain fresh data</li>
                <li>✓ Reduce server load</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Additional Features -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-pink-500 to-rose-600 rounded-full mr-4"></span>
            Additional Features & Tools
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div 
              v-for="feature in additionalFeatures"
              :key="feature.title"
              class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-600"
            >
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">{{ feature.title }}</h3>
              <p class="text-gray-700 dark:text-gray-300 text-sm">{{ feature.description }}</p>
              <ul v-if="feature.items" class="mt-3 space-y-1 text-sm text-gray-600 dark:text-gray-400">
                <li v-for="item in feature.items" :key="item">• {{ item }}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- API Documentation -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-teal-500 to-cyan-600 rounded-full mr-4"></span>
            API Documentation
          </h2>
          
          <div class="bg-teal-50 dark:bg-teal-900/20 rounded-xl p-6 border border-teal-200 dark:border-teal-800">
            <p class="text-gray-700 dark:text-gray-300 mb-4">
              Interactive API documentation powered by <strong>drf-spectacular</strong> (OpenAPI 3.0):
            </p>
            <ul class="space-y-2 text-gray-700 dark:text-gray-300">
              <li>✓ Swagger UI for interactive testing</li>
              <li>✓ JWT authentication support</li>
              <li>✓ Comprehensive endpoint documentation</li>
              <li>✓ Request/response schemas</li>
              <li>✓ Query parameter documentation</li>
            </ul>
            <div class="mt-4">
              <a 
                href="/api/schema/swagger-ui/" 
                target="_blank"
                class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-teal-500 to-cyan-600 text-white font-semibold rounded-lg hover:from-teal-600 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105"
              >
                View API Documentation
                <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Performance Optimizations -->
      <section class="mb-12 animate-fade-in-up">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <span class="w-1 h-8 bg-gradient-to-b from-violet-500 to-purple-600 rounded-full mr-4"></span>
            Performance Optimizations
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div 
              v-for="opt in optimizations"
              :key="opt.title"
              class="bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20 rounded-xl p-6 border border-violet-200 dark:border-violet-800"
            >
              <div class="text-3xl mb-3">{{ opt.icon }}</div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">{{ opt.title }}</h3>
              <p class="text-sm text-gray-700 dark:text-gray-300">{{ opt.description }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
const technologies = [
  {
    name: 'Django 4.2',
    description: 'High-level Python web framework for rapid development',
    icon: '🐍',
    color: 'from-green-500 to-emerald-600'
  },
  {
    name: 'Django REST Framework',
    description: 'Powerful toolkit for building Web APIs',
    icon: '🔌',
    color: 'from-red-500 to-pink-600'
  },
  {
    name: 'JWT Authentication',
    description: 'Secure token-based authentication with Simple JWT',
    icon: '🔐',
    color: 'from-blue-500 to-cyan-600'
  },
  {
    name: 'PostgreSQL',
    description: 'Advanced open-source relational database',
    icon: '🐘',
    color: 'from-indigo-500 to-blue-600'
  },
  {
    name: 'Redis',
    description: 'In-memory data structure store for caching',
    icon: '⚡',
    color: 'from-red-500 to-orange-600'
  },
  {
    name: 'Celery',
    description: 'Distributed task queue for async processing',
    icon: '🌾',
    color: 'from-green-500 to-teal-600'
  },
  {
    name: 'Celery Beat',
    description: 'Periodic task scheduler for cron-like jobs',
    icon: '⏰',
    color: 'from-yellow-500 to-amber-600'
  },
  {
    name: 'Django Redis',
    description: 'Redis cache backend for Django',
    icon: '💾',
    color: 'from-purple-500 to-pink-600'
  },
  {
    name: 'DRF Spectacular',
    description: 'OpenAPI 3.0 schema generation for DRF',
    icon: '📚',
    color: 'from-teal-500 to-cyan-600'
  }
]

const architecture = [
  {
    title: 'RESTful API Design',
    description: 'Clean, stateless API following REST principles with proper HTTP methods and status codes.',
    details: [
      'GET, POST, PUT, PATCH, DELETE methods',
      'Proper status codes (200, 201, 400, 401, 404, 500)',
      'JSON request/response format',
      'Pagination support for list endpoints'
    ],
    code: null
  },
  {
    title: 'Custom User Model',
    description: 'Extended Django user model with additional fields and role-based access control.',
    details: [
      'Custom User model extending AbstractBaseUser',
      'User types: Manager, Supervisor, Operator, Customer',
      'Automatic staff status based on user type',
      'Cart property for automatic cart creation'
    ],
    code: null
  },
  {
    title: 'Django Signals',
    description: 'Automatic cache invalidation when products, categories, brands, ratings, or comments change.',
    details: [
      'post_save and post_delete signals',
      'Automatic cache pattern invalidation',
      'Product, Category, Brand, Rating, Comment signals',
      'Prevents serving stale data'
    ],
    code: null
  },
  {
    title: 'Custom Middleware',
    description: 'Cart middleware for merging anonymous cart with user cart after login.',
    details: [
      'Automatic cart merging on authentication',
      'Cookie-based cart for anonymous users',
      'Seamless user experience',
      'Data consistency maintenance'
    ],
    code: null
  }
]

const additionalFeatures = [
  {
    title: 'Query Optimization',
    description: 'Efficient database queries using select_related and prefetch_related to minimize N+1 queries.',
    items: [
      'select_related for ForeignKey relationships',
      'prefetch_related for ManyToMany and reverse ForeignKey',
      'Annotate for aggregations',
      'Optimized queryset chains'
    ]
  },
  {
    title: 'Pagination',
    description: 'Custom pagination class with configurable page size and maximum limits.',
    items: [
      'PageNumberPagination implementation',
      'Configurable page_size query parameter',
      'Maximum page size limit (100)',
      'Default page size: 10 items'
    ]
  },
  {
    title: 'Filtering & Search',
    description: 'Advanced filtering using django-filter with support for multiple query parameters.',
    items: [
      'Product search by name, brand, category, details',
      'Category and brand filtering',
      'Sorting by name, price, rating',
      'Query parameter-based filtering'
    ]
  },
  {
    title: 'Image Handling',
    description: 'Pillow integration for image processing and storage with proper media file handling.',
    items: [
      'Product images and banner images',
      'Category images',
      'Media file uploads',
      'Image URL generation'
    ]
  },
  {
    title: 'Email Integration',
    description: 'SMTP email backend for sending OTP codes and notifications via Celery tasks.',
    items: [
      'OTP code delivery',
      'Async email sending',
      'Configurable SMTP settings',
      'Error handling and fallbacks'
    ]
  },
  {
    title: 'Discount System',
    description: 'Flexible discount code system with percentage-based discounts applied at checkout.',
    items: [
      'Discount code model',
      'Percentage-based discounts',
      'Cart-level discount application',
      'Order discount tracking'
    ]
  },
  {
    title: 'Rating & Comments',
    description: 'User-generated content with ratings (1-5 stars) and comments on products.',
    items: [
      'One rating per user per product',
      'Average rating calculation',
      'Product comments with author tracking',
      'Cache invalidation on updates'
    ]
  },
  {
    title: 'Order Management',
    description: 'Complete order processing with address snapshot, payment status, and order items.',
    items: [
      'Order creation with address snapshot',
      'Order items with price at purchase',
      'Payment and shipping status tracking',
      'User order history'
    ]
  }
]

const optimizations = [
  {
    title: 'Database Indexing',
    description: 'Strategic indexes on frequently queried fields like product names',
    icon: '📊'
  },
  {
    title: 'Connection Pooling',
    description: 'Redis connection pooling with max_connections and retry logic',
    icon: '🔗'
  },
  {
    title: 'Lazy Loading',
    description: 'Celery broker connection retry on startup for better reliability',
    icon: '⚙️'
  }
]
</script>


<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out;
}
</style>

