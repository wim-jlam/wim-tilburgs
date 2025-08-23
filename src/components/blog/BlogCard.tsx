import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { BlogPost, Language } from '@/types';
import { format } from 'date-fns';
import { nl, enUS } from 'date-fns/locale';

interface BlogCardProps {
  post: BlogPost;
  featured?: boolean;
  className?: string;
}

const BlogCard: React.FC<BlogCardProps> = ({ post, featured = false, className = '' }) => {
  const { t, i18n } = useTranslation();
  const currentLang = i18n.language as Language;
  const locale = currentLang === 'nl' ? nl : enUS;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return format(date, 'PPP', { locale });
  };

  const getExcerpt = (content: string, maxLength: number = 150) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength).trim() + '...';
  };

  const cardClasses = featured
    ? 'group bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-200'
    : 'group bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden border border-gray-100';

  return (
    <article className={`${cardClasses} ${className}`}>
      <Link to={`/blog/${post.slug}`} className="block">
        {/* Featured Image */}
        {post.featured_image && (
          <div className={`relative overflow-hidden ${featured ? 'h-64' : 'h-48'}`}>
            <img
              src={post.featured_image}
              alt={post.title[currentLang]}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            {/* Auto-translated badge */}
            {post.auto_translated && (
              <div className="absolute top-3 left-3">
                <span className="px-2 py-1 bg-blue-600/90 text-white text-xs rounded-full backdrop-blur-sm">
                  🤖 AI Translated
                </span>
              </div>
            )}
          </div>
        )}

        {/* Content */}
        <div className={`p-6 ${featured ? 'space-y-4' : 'space-y-3'}`}>
          {/* Meta Info */}
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-3">
              <span className="flex items-center space-x-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{formatDate(post.published_at || post.created_at)}</span>
              </span>
              <span className="text-gray-300">•</span>
              <span className="flex items-center space-x-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{post.read_time} min read</span>
              </span>
            </div>
            <div className="flex items-center space-x-1">
              <img
                src={post.author.avatar_url || '/api/placeholder/24/24'}
                alt={post.author.name}
                className="w-5 h-5 rounded-full"
              />
              <span className="text-gray-600">{post.author.name}</span>
            </div>
          </div>

          {/* Title */}
          <h3 className={`font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-200 ${
            featured ? 'text-2xl leading-tight' : 'text-xl'
          }`}>
            {post.title[currentLang]}
          </h3>

          {/* Excerpt */}
          <p className={`text-gray-600 leading-relaxed ${featured ? 'text-base' : 'text-sm'}`}>
            {getExcerpt(post.excerpt[currentLang], featured ? 200 : 120)}
          </p>

          {/* Tags */}
          {post.tags && post.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {post.tags.slice(0, featured ? 4 : 3).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full hover:bg-gray-200 transition-colors duration-200"
                >
                  #{tag}
                </span>
              ))}
              {post.tags.length > (featured ? 4 : 3) && (
                <span className="text-gray-400 text-xs">
                  +{post.tags.length - (featured ? 4 : 3)} more
                </span>
              )}
            </div>
          )}

          {/* Read More CTA */}
          <div className="pt-2">
            <span className="inline-flex items-center text-blue-600 font-medium text-sm group-hover:text-blue-700 transition-colors duration-200">
              {t('blog.readMore')}
              <svg
                className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform duration-200"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </span>
          </div>
        </div>
      </Link>
    </article>
  );
};

export default BlogCard;