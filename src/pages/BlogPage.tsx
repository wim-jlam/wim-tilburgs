import React from 'react';
import { useTranslation } from 'react-i18next';
import BlogList from '@/components/blog/BlogList';

const BlogPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            {t('blog.title')}
          </h1>
          <p className="text-xl opacity-90 max-w-2xl mx-auto">
            {t('blog.subtitle')}
          </p>
        </div>
      </section>

      {/* Blog Content */}
      <section className="py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <BlogList showFilters={true} featuredFirst={true} />
        </div>
      </section>
    </div>
  );
};

export default BlogPage;