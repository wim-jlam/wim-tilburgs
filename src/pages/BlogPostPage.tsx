import React from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const BlogPostPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-white py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
        <div className="text-center py-20 text-gray-500">
          =Ý Blog post: <code>{slug}</code>
          <br />
          <small className="text-sm">Individual blog post content komt hier</small>
        </div>
      </div>
    </div>
  );
};

export default BlogPostPage;