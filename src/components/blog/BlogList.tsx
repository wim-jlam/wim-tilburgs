import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { BlogPost, BlogFilters, Language, PaginatedResponse } from '@/types';
import BlogCard from './BlogCard';
import LoadingSpinner from '@/components/common/LoadingSpinner';

interface BlogListProps {
  initialPosts?: PaginatedResponse<BlogPost>;
  showFilters?: boolean;
  featuredFirst?: boolean;
  className?: string;
}

const BlogList: React.FC<BlogListProps> = ({
  initialPosts,
  showFilters = true,
  featuredFirst = true,
  className = ''
}) => {
  const { t, i18n } = useTranslation();
  const currentLang = i18n.language as Language;
  
  const [posts, setPosts] = useState<PaginatedResponse<BlogPost> | null>(initialPosts || null);
  const [loading, setLoading] = useState(!initialPosts);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<BlogFilters>({});
  const [searchQuery, setSearchQuery] = useState('');

  // Mock data for development
  useEffect(() => {
    if (!initialPosts) {
      // Simulate API call
      const mockPosts: PaginatedResponse<BlogPost> = {
        items: [
          {
            id: '1',
            slug: 'gpt5-diabetes-breakthrough',
            title: {
              nl: 'GPT-5 Doorbraak in Diabetes Onderzoek',
              en: 'GPT-5 Breakthrough in Diabetes Research'
            },
            content: {
              nl: 'Een revolutionaire ontdekking in AI-gestuurde diabeteszorg...',
              en: 'A revolutionary discovery in AI-driven diabetes care...'
            },
            excerpt: {
              nl: 'Ontdek hoe GPT-5 een nieuwe dimensie toevoegt aan diabetes onderzoek en behandeling.',
              en: 'Discover how GPT-5 adds a new dimension to diabetes research and treatment.'
            },
            author: {
              id: '1',
              name: 'Wim Tilburgs',
              avatar_url: '/api/placeholder/40/40'
            },
            featured_image: '/api/placeholder/600/400',
            tags: ['GPT-5', 'Diabetes', 'AI Research', 'Healthcare'],
            categories: ['AI Research'],
            seo: {
              description: {
                nl: 'GPT-5 diabetes onderzoek doorbraak',
                en: 'GPT-5 diabetes research breakthrough'
              },
              keywords: ['GPT-5', 'diabetes', 'AI', 'health']
            },
            published: true,
            auto_translated: false,
            created_at: '2025-08-20T10:00:00Z',
            updated_at: '2025-08-20T10:00:00Z',
            published_at: '2025-08-20T10:00:00Z',
            read_time: 8
          },
          {
            id: '2',
            slug: 'ai-health-future',
            title: {
              nl: 'De Toekomst van AI in de Gezondheidszorg',
              en: 'The Future of AI in Healthcare'
            },
            content: {
              nl: 'Hoe AI de gezondheidszorg revolutioneert...',
              en: 'How AI is revolutionizing healthcare...'
            },
            excerpt: {
              nl: 'Een blik op de toekomst van AI-gestuurde gezondheidszorg en wat dit betekent voor patiënten.',
              en: 'A look at the future of AI-driven healthcare and what it means for patients.'
            },
            author: {
              id: '1',
              name: 'Wim Tilburgs',
              avatar_url: '/api/placeholder/40/40'
            },
            featured_image: '/api/placeholder/600/400',
            tags: ['AI', 'Healthcare', 'Future', 'Innovation'],
            categories: ['Healthcare AI'],
            seo: {
              description: {
                nl: 'AI gezondheidszorg toekomst',
                en: 'AI healthcare future'
              },
              keywords: ['AI', 'healthcare', 'future', 'innovation']
            },
            published: true,
            auto_translated: true,
            created_at: '2025-08-18T14:30:00Z',
            updated_at: '2025-08-18T14:30:00Z',
            published_at: '2025-08-18T14:30:00Z',
            read_time: 5
          }
        ],
        total: 2,
        page: 1,
        per_page: 10,
        total_pages: 1
      };

      setTimeout(() => {
        setPosts(mockPosts);
        setLoading(false);
      }, 1000);
    }
  }, [initialPosts]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setFilters(prev => ({ ...prev, search: query }));
    // TODO: Implement API call
  };

  const handleFilterChange = (newFilters: Partial<BlogFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
    // TODO: Implement API call
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="lg" text={t('blog.loading')} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          {t('common.retry')}
        </button>
      </div>
    );
  }

  if (!posts || posts.items.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 mb-4">{t('blog.noResults')}</div>
        {filters.search && (
          <button
            onClick={() => {
              setFilters({});
              setSearchQuery('');
            }}
            className="text-blue-600 hover:text-blue-700 transition-colors"
          >
            Clear search
          </button>
        )}
      </div>
    );
  }

  const featuredPosts = posts.items.filter(post => post.featured_image && featuredFirst);
  const regularPosts = posts.items.filter(post => !post.featured_image || !featuredFirst);

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Search & Filters */}
      {showFilters && (
        <div className="bg-gray-50 rounded-xl p-6 space-y-4">
          <div className="relative">
            <input
              type="text"
              placeholder={t('blog.search')}
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg
              className="absolute left-3 top-3.5 h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>

          {/* Filter tags */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleFilterChange({ tag: undefined })}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                !filters.tag
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {t('blog.all')}
            </button>
            {['AI', 'Diabetes', 'Healthcare', 'Research'].map(tag => (
              <button
                key={tag}
                onClick={() => handleFilterChange({ tag })}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  filters.tag === tag
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                #{tag}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Featured Posts */}
      {featuredPosts.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">{t('blog.featured')}</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {featuredPosts.map(post => (
              <BlogCard key={post.id} post={post} featured={true} />
            ))}
          </div>
        </section>
      )}

      {/* Regular Posts */}
      <section>
        {featuredPosts.length > 0 && (
          <h2 className="text-2xl font-bold text-gray-900 mb-6">{t('blog.latest')}</h2>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {(featuredFirst ? regularPosts : posts.items).map(post => (
            <BlogCard key={post.id} post={post} />
          ))}
        </div>
      </section>

      {/* Pagination */}
      {posts.total_pages > 1 && (
        <div className="flex justify-center space-x-2 pt-8">
          {Array.from({ length: posts.total_pages }, (_, i) => i + 1).map(page => (
            <button
              key={page}
              onClick={() => {/* TODO: Implement pagination */}}
              className={`px-4 py-2 rounded-lg transition-colors ${
                page === posts.page
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {page}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default BlogList;